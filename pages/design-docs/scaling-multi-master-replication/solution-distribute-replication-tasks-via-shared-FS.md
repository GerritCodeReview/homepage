---
title: "Solution - Distribute Replication Tasks via a Shared Filesystem - Scaling Multi-Master Replication"
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Distribute Replication Tasks via a Shared Filesystem

## <a id="prerequisite"> Prerequisite

This solution is based on this change to the operational nature of the replication plugin:

https://gerrit-review.googlesource.com/c/plugins/replication/+/239212

If this approach is not taken, then this design will likely need to be revised.

## <a id="overview"> Overview

The solution is to coordinate the distribution of the replication tasks as evenly as possible across
all the nodes in the cluster via sharing the filesystem hosting the persisted replication tasks via
a shared filesystem such as NFS. The high level tasks that will be used to achieve this are:

### 1) Modifying the persisted task store so that it can be safely shared across multiple nodes via a
shared file system

### 2) Use a directory lock to ensure replication to the same URI does not occur concurrently in the
cluster

### 3) Distribute the tasks among masters by periodically adding every replication task from the
persisted store to the replication queue on every node

### 4) Improve task distribution with random delays

## <a id="detailed-design"> Detailed Design

### The Current Replication Mechanism

Overview of the ordered events that happen when a ref updates:

##### i) Gerrit updates a ref

##### ii) Gerrit fires a event

Currently when an action on the Gerrit server updates a ref, it fires a
gitReferenceUpdatedListener.Event which the replication plugin is listening for.

Example:

    Event Fired by Gerrit for -> (project="All-Projects", ref="ref/meta/config")

##### iii) The replication plugin receives that project/ref based event

The replication plugin receives the event to determine how to replicate the update.

##### iv) The event is split into URI based tasks

The replication plugin first splits the project/ref based event (update to a ref in a specific
project) into a series of replication tasks, one for each destination configured in the
replication.config file. Each new replication task which is split out represents a needed git push
to the URI which is the combination of the updated project and the destination URIish from the
replication config.

Example:

    url = git://destination-A:9417/${name}.git
      -> push git://destination-A:9417/All-Projects.git refs/meta/config
    url = git://destination-B:9417/${name}.git
      -> push git://destination-B:9417/All-Projects.git refs/meta/config
    url = git://destination-C:9417/${name}.git
      -> push git://destination-C:9417/All-Projects.git refs/meta/config
    url = git://destination-D:9417/${name}.git
      -> push git://destination-D:9417/All-Projects.git refs/meta/config
    url = git://destination-E:9417/${name}.git
      -> push git://destination-E:9417/All-Projects.git refs/meta/config

##### v) Persist the specific URI/ref based tasks to the filesystem

Each task is persisted in a json file named after the SHA1 of the json under
<site_dir>/data/replication/ref-updates/waiting

Example:

    <site_dir>/data/replication/ref-updates/waiting/a564cbd....json
    <site_dir>/data/replication/ref-updates/waiting/77adf32....json
    <site_dir>/data/replication/ref-updates/waiting/07fd222....json
    <site_dir>/data/replication/ref-updates/waiting/57bf2d2....json
    <site_dir>/data/replication/ref-updates/waiting/bbff33d....json

##### vi) Scheduled tasks to be run after a configurable replication delay

##### vii) A scheduled task is put into a thread pool managed by Gerrit

Gerrit manages the threadpool with a java ScheduledThreadPoolExecutor. The specific thread pool
depends on the replication configuration. Since there are a limited amount of threads, the tasks may
wait longer than the replication delay before executing.

##### viii) Consolidate pushes to the same URI

On scheduling the plugin attempts to consolidate the push with any existing pushes for the same
URI which may still be waiting to run.

Example:

    waiting
      -> push git://destination-E:9417/All-Projects.git refs/dashboards/mydash

    incoming
      -> push git://destination-E:9417/All-Projects.git refs/meta/config

    consolidated
      -> push git://destination-E:9417/All-Projects.git refs/dashboards/mydash refs/meta/config

##### ix) Push refs

When a slot is free in the approximate thread pool, all the ref updates for a single URI will be
pushed with a single git push

##### x) Move the persisted tasks for a URI to the running directory.

Example:

    <site_dir>/data/replication/ref-updates/waiting/bbff33d....json
      -> <site_dir>/data/replication/ref-updates/running/bbff33d....json

##### xi A) Push Fails

If this push fails, it may either be aborted, or a retry may be rescheduled for a later time
(moving the tasks back to the waiting directory).

##### xi C) Push Succeeds

On success, the persisted json file will be deleted from the filesystem.

##### Startup

Finally, on system startup, all the existing persisted tasks will be replayed with
the assumption that they are still outstanding.

### 1) Safely sharing the persisted task store

In order to make it safe to share the persisted task store across multiple nodes, two threads, even
on different nodes, may not write to the same file. This is currently possible on task creation
since the check for existence of a file followed by writing to it is racy. To avoid this race, first
write new files to a tempfile in another directory first, then move the tempfile into place. Using
another directory to write the file prevents the partially written file from appearing in listings.

Example:

    <site_dir>/data/replication/ref-updates/building/tmp001232asf.json
      -> <site_dir>/data/replication/ref-updates/waiting/a564cbd....json

To avoid resetting timestamps which will be used in step 3, do not overwrite already existing files
in the "waiting" directory.

### 2) Prevent Concurrent replication to the same URI

To prevent two threads, even on different nodes, from running the same task, introduce a URI based
filesystem "lock" that can only be acquired atomically by one thread, and only run tasks on the
thread which acquires the lock. URI based locking will be used instead of task level locking to
ensure that URI based "close in time" batching is still preserved as it would be with a single node.

Before running a task, acquire the URI lock by creating a directory with a uriKey (the key is the
SHA1 of the URI). If the directory can be created, then the lock will have been acquired and any
tasks for that URI should be run after moving the task file from the "waiting" directory into the
"running" directory of the URI. If no such tasks exist anymore, assume the tasks were completed by
another node and unlock the URI by deleting the directory. If the directory cannot be created,
assume the URI is already being replicated to by another node.

If the tasks are assumed to be already, or are currently being, replicated to by another node, skip
replicating to the URI without altering the persistence of the tasks.

On startup after moving running tasks back to the waiting directory, delete the URI lock directory
for each previously running task.

Example:

  Lock dir:

    <site_dir>/data/replication/ref-updates/running/23baf46.../   (SHA1 of URI)

  Two ref updates for the same URI:

    <site_dir>/data/replication/ref-updates/waiting/a564cbd....json
      -> <site_dir>/data/replication/ref-updates/running/23baf46.../a564cbd....json

    <site_dir>/data/replication/ref-updates/waiting/052b7ca....json
      -> <site_dir>/data/replication/ref-updates/running/23baf46.../052b7ca....json


### 3) Periodically add all persisted tasks to the replication queue

On each node, run a repeating distribution task which reads all the persisted tasks from the
"waiting" directory and adds them to the replication queue. The repeating interval of this
distribution task will be known as the "distribution interval". This interval should be less than
the replication delay, a good default for the interval is likely around 10s. Use the timestamp of
the oldest persisted task file for the same URI as the time basis to add the replication delay to
when scheduling the time to run each task.

This distribution task should result in an approximate unified view on each node of the entire set
of outstanding replication tasks in the cluster. Tasks will progress "upward" on each node
independently as other replication tasks complete on the node. As tasks become runnable on each
node, if the task has already been run by another node, or is currently running by another node, it
should silently "drop" out of the replication queue on the non running nodes.

An optional improvement to improve the visibility of outstanding tasks would be to remove tasks from
the queue which are no longer backed by tasks in the "waiting" directory even before they reach the
runnable state on each node.

### 4) Add random delays to scheduling tasks on each node

Lastly, to get good task distribution across the cluster, particularly when one or more nodes in the
cluster might be mostly idle, add a small random delay to the scheduled start time of each task
when inserting it into the queue. A good upper bound on this delay is likely around the same as the
distribution interval.

### <a id="scalability"> Scalability

#### Task Distribution to the nodes with available resources

The basis of good task distribution to the nodes with available resources in the cluster should
depend on ensuring that the replication delay is longer than the distribution interval and good
clock synchronization across the nodes. If these factors are well satisfied, then it can be expected
that as each node gets a free thread, that it will execute any task ready to execute, resulting in
the nodes with the most free resources running the most tasks. This should lead to a desirable "most
available resources" based distribution.

#### Task consolidation across the cluster

Task consolidation will be impacted by the length of the distribution interval, by the length of
random scheduling delays inserted, and by the replication delay. Reducing the distribution interval
and/or increasing the random scheduling delays or the replication delay should reduce this impact
since, as with single node systems, the longer tasks sit in the queue on each node, the more
opportunities there are for consolidation to occur.

#### CPU

Once tasks can be shared across multiple masters, it will be possible to share any extra load that
new destinations will put on masters across the cluster. It should then be possible to lower the
dedicated thread count to each destination by the proportion of newly added threads from any
additional nodes added and still keep the same service to each destination. For example, if there
are 8 threads per destination with a single node, lowering the thread count to 4 per destination
when a second node is added, should still leave 8 threads available in the cluster for each
destination. This thread count lowering has the additional benefit that it frees up extra CPU on
each node for new destinations. So if there were originally 5 destinations with 8 threads each, for
a total of 40 threads of CPU, now with only 4 threads per destination, the destination count could
be doubled to 10 and there should still be enough CPU for all of them on each node.

#### Memory

Unfortunately even ideal distribution of persisted events across the cluster does not strictly
prevent the memory exhaustion problems that are possible within an individual node which are
accentuated when adding more destinations. However good distribution, particularly with tasks for
the same event, does statistically reduce the chances of memory exhaustion since it becomes less
likely that all the tasks for any particularly big project will get executed at the same time on
the same node.

In the long run, a true QOS solution will likely be needed to guarantee that memory exhaustion is
not possible by running too many concurrent combinations of big projects, but good distribution
will on average allow a cluster to scale to handle more destinations memory-wise by adding more
master nodes.

#### Replicate-All

The replicate-all command tends to result in a significant backlog of replication tasks. As with
other workloads with backlogs, these should get well distributed to the nodes to where the resources
are available. So an individual replicate-all will scale better on the masters in clusters with more
nodes, but the impact to the destinations will remain the same.

However, if startup replication were to be used, or if replicate-all were to be switched to "on
cluster startup" and "on node shutdown" which would be more appropriate with more than one master,
the impact to destinations will increase proportionally with the amount of nodes added. It is
possible to mitigate this somewhat during maintenance operations such as upgrades where many nodes
need to be restarted, by restarting the nodes closer together to benefit from the cluster's ability
to perform task deduplication.

## <a id="alternatives-considered"> Alternatives Considered

### Task storage alternatives

Since the current filesystem based storage exists and can be enhanced fairly easily to satisfy the
desired use case as a polling based sharing solution, the extra expense of other sharing solutions
does not currently seem worth considering.

### Task distribution alternatives

This solution uses polling for task distribution, an event based solution could be used instead to
reduce distribution delays. However since the distribution delay introduced by this polling
solution is intended to be less than the replication delay, there is not a lot to be gained by
using an event based solution. The biggest advantage of the event based solution would likely be to
decrease the chance of missed "close in time" deduplication of tasks. An event system could easily
be added ontop of the current polling to get this added benefit if desired.

### Task scheduling alternatives

The current solution will work ontop and around the Gerrit executor, in a way that some may
possibly see as klunky, or not very clean. Since the java ScheduledThreadPoolExecutor has some
strong constraints that make it hard to override, to integrate a distributed queue more cleanly with
Gerrit would likely mean replacing the java ScheduledThreadPoolExecutor entirely. Doing so would
require modifying gerrit core which seems unnecessary to achieve good enough scheduling to scale
replication. Even if one were willing to modify Gerrit core, it would be very difficult to replace
the ScheduledThreadPoolExecutor inside Gerrit without having to re-implement most of the likely
very complicated scheduling logic that it already implements. However, this could likely still be
done after this current proposed solution is implemented without much loss of work from the current
solution.

### Memory limit alternatives

#### 1) Setting very restrictive limits

One stopgap measure to avoid memory exhaustion, which does not allow scaling the supported site
proportionally with the amount of nodes, but does allow it to scale beyond what a single node can
handle is to drastically reduce the thread counts per destination on each node, and to combine
destinations within threadpools with lower thread counts than destination counts. In the original
examples, this can be achieved by keeping the total concurrent per project count to 5 (the original
limit) per node.  This requires adding 15 more nodes for a total of 16 nodes each configured like
this:

    [remote "All"]
      url = git://destination-A:9417/${name}.git
      url = git://destination-B:9417/${name}.git
      url = git://destination-C:9417/${name}.git
      url = git://destination-D:9417/${name}.git
      url = git://destination-E:9417/${name}.git
      url = git://destination-F:9417/${name}.git
      url = git://destination-G:9417/${name}.git
      url = git://destination-H:9417/${name}.git
      url = git://destination-I:9417/${name}.git
      url = git://destination-J:9417/${name}.git
      threads = 5

This give a total of 16 * 5 = 80 threads which should allow 8 threads per destination total. This
solution does not make very good use of the available resources on each node, and every destination
is vulnerable to starvation by the others (they don't actually have their own thread pools anymore).

#### 2) Distributing destinations across nodes non-homogeneously

One, even more restricting approach, is to use non homogeneous configurations on each node. The
simple idea is to keep the original node as is and to add the new destinations to the second node:

Node 2:

    [remote "F"]
      url = git://destination-F:9417/${name}.git
      threads = 8
      ...
    [remote "G"]
      url = git://destination-G:9417/${name}.git
      threads = 8
      ...
    [remote "H"]
      url = git://destination-H:9417/${name}.git
      threads = 8
      ...
    [remote "I"]
      url = git://destination-I:9417/${name}.git
      threads = 8
      ...
    [remote "J"]
      url = git://destination-J:9417/${name}.git
      threads = 8
      ...

This solution is harder to administer and it suffers from the loss of HA with respect to
replication destinations.

#### 3) Implementing per project QOS limits.

Such a solution is complicated, but it may be implemented as an add-on to the current solution.

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Simple to implement
2. Leverages existing infrastructure (persisted events)
3. Does not require external coordination
4. Self scaling and balancing

Cons:

1. Replication delay may be slightly increased
2. Memory exhaustion is still possible
3. No global view of running tasks in show-queue output
4. Completed tasks may linger in show-queue output


## <a id="implementation-plan"> Implementation Plan

The following will is a list of changes expected to be independently implementable in the order
listed below.

### 1) Use a temporary directory to create new task files.

Write new tasks to a tempfile in another directory, then move the tempfile into the 'waiting'
directory without overwriting already existing files.

### 2) Acquire URI Lock before running replication to a URI

Before running a task, acquire the URI lock by creating a directory with a uriKey in the 'running'
directory. If the directory can be created, then run all the tasks for that URI after moving the
task files from the "waiting" directory into the lock directory of the URI.

On startup after moving running tasks back to the waiting directory, delete the URI lock directory
for each previously running task.

### 3) Create a periodic distributor

Run a distributor regularly in its own single threaded threadpool at an interval of
replication.distributionInterval where the default is 0 (disabled). On each interval, read each
persistent task from the 'waiting' directory and schedule it to run.

### 4) Adjust replication delays to account for distribution

When scheduling any task (not just from the distributor), consider the replicationDelay to be the
maximum of either remote.NAME.replicationDelay and replication.distributionInterval.

### 5) Use file timestamps when scheduling tasks

Modify the distributor's operation to schedule tasks to run a minimum of
remote.NAME.replicationDelay after the timestamp of the oldest persisted task for the same URI in
the persistent store.

### 6) Adjust replication delays to add some randomness

Add a property named replication.randomDelay which will get added when scheduling any task. Default
the value to 1 second.

## <a id="time-estimation"> Time Estimation

1-6 can each be prototyped in around 1-3 hours each, and likely can be completed and uploaded and
tested in no more than a week each.
