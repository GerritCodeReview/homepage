---
title: "Use Cases - Scaling Multi-Master Replication"
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use-case

We want to be able to support more replication destinations with the same quality as our existing
destinations. We are at the limit of how many destinations a single master can support, and adding
more masters does not increase this limit, instead adding more masters slightly decreases the
number of destinations that we can support with the same quality.

## <a id="acceptance-criteria"> Acceptance Criteria

Gerrit admins should be able to add more replication destinations by adding more master nodes
without compromising the existing replication quality (latency, WAN, CPU, memory, and disk IO) of
the existing replication destinations. The limit on the number of replication destinations
supported by the replication plugin imposed by CPU, and/or memory on the master nodes, should scale
approximately linearly with the number of homogeneous Gerrit master nodes in the master cluster.

## <a id="background"> Background

#### What do we mean by replication "quality" ####

We consider the replication quality of a destination to have two related dimensions that we care
about. The primary dimension generally tends to be the latency of each replication push. This is
most the important dimension since this dimension is visible to end users and it affects end users'
abilities to take advantage of replication. The secondary dimension is the resource utilization of
each destination, this affects admins mostly since increasing this utilization generally requires
scaling the destination to avoid affecting the primary dimension and end users.

#### How do resource limits affect replication quality? ####

There are many limits that affect the latency of replication. The master node specific resource
limits are generally CPU and memory, these are the limits that we hope to overcome by adding more
master nodes. Other master resource limits such as disk I/O tend to be cluster limits and are not
node specific since they tend to be shared by the cluster.  We expect that to be able to support
more replication destinations, that the shared master cluster limits may need to be scaled by the
Gerrit admins independently of changing the design of the replication plugin. Lastly, we will
categorize some resource limits as destination specific limits and these are limits that we do not
want to have to alter to support adding more destinations.

The amount of CPU available to a task directly impacts the latency of any replication task. Adding
more replication destinations to a node increases the CPU needs of that node. Since replication
tends to be a single threaded operation, the number of parallel replication tasks supported by a
node is limited by the number of CPUs available to the node. If the number of CPUs available is
currently limiting the number of destinations that can be replicated to, then adding more
replication destinations will increase the latency to each of the existing destinations.

Like the number of CPUs on a node, the amount of memory available to each node also imposes a limit
on how many replication tasks of a certain size that can be executed concurrently on each node.
However, unlike with CPU limits, exceeding the memory limit of a node by adding more concurrent
replication tasks to the node will result in operational failures as opposed to increasing the
latency to the existing destinations.

Destination specific limits tend to be destination WAN limits, CPU and memory limits on the
destination receiving node(s), and disk I/O. These limits can be hit by the git-daemon
(typically) nodes receiving the JGit pushes from the Gerrit masters. The disk I/O of the receiving
cluster may be a shared limit within the destination.

#### Why does the current replication design not scale with the number of master nodes? ####

1) Only the node on which a ref-update event occurs will service the replication tasks, and thus
every replication destination, associated with that event.

2) Only the node on which a ref-update event occurs is aware of the event and so batching of close
 in time update events may be reduced when there are more master nodes in the cluster.

3) There are additional problems related to managing the potential losses of replication tasks
when servers shutdown that are incurred when using a multi-master setup compared to using a single
master setup, and these problems tend to get worse with each master node added to the cluster. We do
 not consider solving these issues essential to scaling to more nodes, but any solution to the
first two problems that also benefits this problem will be seen as having an advantage over
otherwise relatively equivalent designs.

Why is "startup replication" worse with more master nodes?

Using "startup replication" to manage the potential losses of replication tasks when servers
shutdown delays recovering the lost replication tasks until a nodes starts up. Since with HA
cluster setups, nodes are often allowed to stay down for longer periods of time than with single
master installations, the recovery time for lost replication tasks will likely increase.

Additionally the overall number of "startup replication" tasks will increase since there will be
more starts in the cluster than with a single master installation. This will increase resource
utilization overall at the master installation and for each destination.

Why is "persisted replication tasks" worse with more master nodes?

Since the persisted replication tasks cannot be shared across nodes to manage the potential losses
of replication tasks when servers shutdown, each node needs its own persisted replication tasks
record. Using per node persisted replication tasks will delay recovering the lost replication tasks
 until the same node starts up. Since with HA cluster setups, nodes are often allowed to stay down
for longer periods, the specific node with the record of the overdue replication tasks may stay
down longer and extend the recovery time of the tasks compared to single master installations.

Additionally, using persisted replication tasks to manage incomplete replication on server shutdown
assumes replication tasks can be persisted before the server shuts down. With more servers there is
a greater chance that some tasks never get persisted (unclean shutdowns, bugs...) and get dropped,
ultimately leading to potentially very long replication latencies for those tasks.

#### <a id="questions"> Questions
