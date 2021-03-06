---
title: "Use Cases - Scaling Multi-Master Replication"
permalink: design-docs/scaling-multi-master-replication-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Introduction

Today Gerrit can scale most operations horizontally by adding more nodes. We can handle more git
fetches by adding more slaves nodes. Those with multi-master setups can handle more git pushes, more
WUI traffic, and more queries... by adding more master nodes. We are currently at the limit of how
many destinations a single one of our masters can support. We believe that if we made replication
more efficient so that it could handle more destinations on a single node, that we would eventually
run into new destination limits as our system grows. We want to future proof the replication plugin
so that it too can scale by adding more nodes and can handle a whole class of bottlenecks, real
bottlenecks that exist today which are described later in this doc, and future bottlenecks that no
one has run into yet. With this in mind, this use case is framed in a way that the ability to add
more nodes is not seen as a solution, but rather as a need, just like the need to support other
resource increases such as disk or memory, can be seen as a need. This need flows from the need to
make it possible for admins to scale replication without being dependent on future software changes
in case new bottlenecks arise later, even after the Gerrit project may have become defunct and is no
longer maintained.

# Use-case

We want to be able to support more replication destinations with the same quality as our existing
destinations. We are at the limit of how many destinations a single master can support, and adding
more masters to the same site does not increase this limit, instead adding more masters slightly
decreases the number of destinations that we can support with the same quality.

## Example: ##

We currently have a replication config that looks somewhat like this:

    [remote "A"]
      url = git://destination-A:9417/${name}.git
      threads = 8
      ...
    [remote "B"]
      url = git://destination-B:9417/${name}.git
      threads = 8
      ...
    [remote "C"]
      url = git://destination-D:9417/${name}.git
      threads = 8
      ...
    [remote "D"]
      url = git://destination-D:9417/${name}.git
      threads = 8
      ...
    [remote "E"]
      url = git://destination-E:9417/${name}.git
      threads = 8
      ...

Which works out to a total of 5 destinations at 9 threads each for a total of 40 threads.

We want to be able to support at least 2, and possibly around 10, extra destinations with similar
blocks with similar thread counts. Doing so would increase the CPU and memory usage beyond what a
single server has available and adding more masters will not currently relieve this increase in
resource usage.

Ideally if we had two nodes in our cluster with similar CPU and memory configs, we should be able
to somehow configure the equivalent of another 5 replication groups each with 8 threads and another
destination and still keep the CPU and memory utilization per node equitable to the original config
above so that we do not increase the latencies to the existing replication destinations. To keep our
CPU utilization per node equitable, this means that we should be able to do this without either node
in the cluster running more than the 40 threads (the current max). And to keep our memory
utilization per node equitable, we probably want to be able to do so without either node running
more than 5 concurrent replication tasks of problematic projects at a time. Yet, we also want to not
restrict the threads per destinations per cluster more than currently, i.e. each destination will
still need at least 8 threads available in the cluster to it. And we also would like the cluster to
be able to replicate to all 10 destinations at a time (i.e. we do not want to be restricted to 5
concurrent destinations).

## <a id="acceptance-criteria"> Acceptance Criteria

Gerrit admins should be able to add more replication destinations by adding more master nodes, to
the same site using a shared filesystem such as NFS to access the git repos, without compromising
the existing replication quality (latency, WAN, CPU, memory, and disk IO) of the existing
replication destinations. The limit on the number of replication destinations supported by the
replication plugin imposed by CPU, and/or memory on the master nodes, should scale approximately
linearly with the number of homogeneous Gerrit master nodes in the site master cluster.

It need not be possible to add destinations to a running service without interruption, but being
able to do so would be a great bonus for any solution.

## <a id="background"> Background

### What do we mean by replication "quality"? ###

We consider the replication quality of a destination to have two related dimensions that we care
about. The primary dimension generally tends to be the latency of each replication push. This is
the most important dimension since this dimension is visible to end-users and it affects end-users'
abilities to take advantage of replication. The secondary dimension is the resource utilization of
each destination, this affects admins mostly since increasing this utilization generally requires
scaling the destination to avoid affecting the primary dimension and end-users.

### How do resource limits affect replication quality? ###

There are many limits that affect the latency of replication. The master node specific resource
limits are generally CPU and memory, these are the limits that we hope to overcome by adding more
master nodes. Other master resource limits such as disk I/O and LAN capacity tend to be cluster
limits and are not node specific since they tend to be shared by the cluster.  We expect that to be
able to support more replication destinations, that the shared master cluster limits may need to be
scaled by the Gerrit admins linearly with the amount of destinations added independently of changing
the design of the replication plugin. Lastly, we will categorize some resource limits as destination
specific limits and these are limits that we do not want to have to alter to support adding more
destinations.

#### CPU ####

The amount of CPU available to a task directly impacts the latency of any replication task. Adding
more replication destinations to a node increases the CPU needs of that node. If the number of CPUs
available is currently limiting the number of destinations that can be replicated to, then adding
more replication destinations will increase the latency to each of the existing destinations.

##### Example: #####

If we add a new destination to the config above with a block like this:

    [remote "F"]
      url = git://destination-F:9417/${name}.git
      threads = 8

The total possible replication threads now becomes 40 + 8 = 48. If our replication is CPU bound we
would expect out latencies per existing destination to increase by 20%. On our servers with 24 real
cores and hyperthreading, we likely are only CPU bound during bursts when our replication threads
compete with other master operations and adding more destinations will make those bursts bigger.

#### Memory ####

Like the number of CPUs on a node, the amount of memory available to each node also imposes a limit
on how many replication tasks of a certain size can be executed concurrently on each node. However,
unlike with CPU limits, exceeding the memory limit of a node by adding more concurrent replication
tasks to the node will result in operational failures as opposed to increasing the latency to the
existing destinations.

##### Example: #####

For a somewhat oversimplified model, suppose that we have a big-project which takes 10GB of memory
to replicate it to one destination and that for each extra concurrent thread replicating it, the
server will use another 10GB of memory. Now if we suppose that our server has 50GB of memory
available to the replication process, we can see that by adding remote "F" mentioned above, that we
could now potentially be running 6 replication tasks on big-project (one on each of destinations
A-F) and thus we will need 6 * 10GB = 60GB of memory on our server. Since 60GB is greater than 50GB,
we will likely run out of memory. We have at least one project that can only be cloned 4 times
concurrently without our servers with 196GB of heap and 243GB RAM running out of memory! This means
that with even just 5 destinations we are at risk of running out of memory.

Of course, every project uses some memory, not just the largest one, so assuming that we have other
projects on our server, our simplified example above would actually be subject to additional memory
utilization from them potentially replicating at the same time. Our replication needs to be able to
handle replicating our projects where the top 10 largest repos are approximately sized: 90, 74, 71,
59, 45, 41, 38, 35, 33, 31 GBs in packs. We also need to be able to handle replicating our projects
with many refs where the top 10 projects with the most refs have around: 773, 651, 417, 393, 256,
236, 228, 221, 192, 174 K refs. It is likely that the projects with the most refs are seeing the
most ref updates, so bursty replication behavior by those projects is more likely to lead to out of
memory errors. Calculating the actual memory utilization with more than one project becomes
complicated quite rapidly, but we hope to have at least given the reader a glimpse how replicating
to multiple large projects simultaneously can run into memory limits, and we will not delve deeper
on this here.

#### Destination Resources ####

Destination specific limits tend to be destination WAN limits, CPU and memory limits on the
destination receiving node(s), and disk I/O. These limits can be hit by the git-daemon (typically)
nodes receiving the JGit pushes from the Gerrit masters. The disk I/O of the receiving cluster may
be a shared limit within the destination.

### Why does the current replication design not scale with the number of master nodes? ###

1) Only the node on which a ref-update event occurs will service the replication tasks, and thus
every replication destination, associated with that event.

2) Only the node on which a ref-update event occurs is aware of the event and so batching of close
 in time update events may be reduced when there are more master nodes in the cluster.

3) There are additional problems related to managing the potential losses of replication tasks
when servers shutdown that are incurred when using a multi-master setup compared to using a single
master setup, and these problems tend to get worse with each master node added to the cluster. We do
not consider solving these issues essential to scaling to more nodes, but any solution to the first
two problems that also benefits this problem will be seen as having an advantage over otherwise
relatively equivalent designs.

#### Why is "startup replication" worse with more master nodes? ####

Using "startup replication" to manage the potential losses of replication tasks when servers
shutdown delays recovering the lost replication tasks until a nodes starts up. Since with HA
cluster setups, nodes are often allowed to stay down for longer periods of time than with single
master installations, the recovery time for lost replication tasks will likely increase.

Additionally the overall number of "startup replication" tasks will increase since there will be
more starts in the cluster than with a single master installation. This will increase resource
utilization overall at the master installation and for each destination.

#### Why is "persisted replication tasks" worse with more master nodes? ####

Using per node persisted replication tasks (the only currently supported persistence approach) will
delay recovering the lost replication tasks until the same node starts up. Since with HA cluster
setups, nodes are often allowed to stay down for longer periods, the specific node with the record
of the overdue replication tasks may stay down longer and extend the recovery time of the tasks
compared to single master installations.

Additionally, using persisted replication tasks to manage incomplete replication on server shutdown
assumes replication tasks can be persisted before the server shuts down. With more servers there is
a greater chance that some tasks never get persisted (unclean shutdowns, bugs...) and get dropped,
ultimately leading to potentially very long replication latencies for those tasks.

##### Why is per node stores the only supported persistence mode currently? #####

Currently each node needs its own persisted replication task file store. The persisted replication
tasks cannot be shared because new task files are written directly to the file store which means
they could be only partially written when read by another node on startup, and because nodes can
delete outstanding tasks written by other nodes which could result in losing track of outstanding
tasks from the persistent store.
