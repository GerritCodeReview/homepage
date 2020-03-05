---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

Given a multi-master, single or multi-site, Gerrit setup, it is not possible to
determine, from which instance in the cluster an Event has been produced.

Events don’t keep track of the instance they were generated from, they only carry
information about their type and creation time.

In case of multi-master setup the `index`, `cache`, `projectList` and `stream`
events need to be broadcasted to all the instances of the cluster.

This is fundamental to notify the replica nodes on the activities happening on the
master and allow them to align. For example, indexes are not shared among instances.
To align them, `index` events from the master are broadcasted to the replicas,
notifying them an indexing action is required.

Currently any plugin that needs to understand the origin of an Event is using
a hack to determine it.

Examples can be found in the `high-availability` and the `multi-site` plugin,
where, the in flight Events, are flagged as "forwarded" in the thread local storage.

Considering that multi-master setups are a common and fundamental use case,
delegating the resolution of the issue to external plugins, via fragile workarounds,
will lead to an overall inconsistent architectures.

Other plugins integrating with third party tools, like, for example, the
[slack-integration](https://gerrit.googlesource.com/plugins/slack-integration/)
one, end up triggering notification from each instance of the cluster,
making them too verbose to be used in a multi-master installation.

## `serverId` Vs `instanceName`: Cluster and Instance unique identifier

In the Gerrit configuration it is possible to specify two different identifiers:
`serverId`: the identifier of the server a Git repository belongs to
`instanceName`: a human-readable identifier for a Gerrit instance

### `serverId`

The `serverId` is used as a signature of the review metadata associated to a change.
Normally, only Git repositories belonging to the same Gerrit Server can read the
metadata associated with it.

If you have two Gerrit masters, A and B, that do not have the same `serverid`, but
share the same repositories (either via NFS or replication), the reviews created
on node A, are not visible to node B, and vice-versa.

For this reason, whenever in a multi-master setup, the `serverId` of the nodes
belonging to the cluster must be the same.

### `instanceName`

The `instanceName` is made available to the mailing template engine, hence it can
be used in the emails’ content as a human-readable identification of the Gerrit
instance.

## The missing Event source field

In a multi-master setup, high-availability or multi-site, the events are broadcasted
to all the instances that belong to the same cluster and share the same repositories.

However, currently, it not possible to understand which instance in the cluster
generated an Event. Making the `instanceName`, or another unique identifier of
the Gerrit instance, available in the Event could solve this problem.

# Use-cases

In a multi-master setup, [multi-site](https://gerrit.googlesource.com/plugins/multi-site/)
or [high-availability](https://gerrit.googlesource.com/plugins/high-availability/),
where each Gerrit instance can broadcast Events, it is fundamental to understand
where an event has been generated.

Here some uses cases:

* _Avoid loops:_ in a multi-site setup events are broadcasted to topics. Each
instance produces and consumes from the same topic. Having the `instanceName`,
or another instance id, in the events generated would help to avoid consuming
events generated from the same instance, and going into an infinite loop of events.
Currently high-availability and multi-site plugin use an hack to determine it, by
flagging the in-flight Event as "forwarded" in the thread local storage
* _Priority routing_: prioritise consumption from a particular instance when the
replication queues are loaded
* _Troubleshooting_: exposing which instance is serving a request
* _Preventing events duplication_: when listening to events through plugins
(e.g. Slack integration) a single event would be consumed by all the plugins on
the cluster, causing duplication of notifications (e.g. Slack would repeat the same
message a number of times equal to the number of nodes).
`instanceName` would allow plugins to avoid that behaviour.

# Acceptance Criteria

* Event source labelling

  *GIVEN* A Gerrit master with instance id `A`
  *WHEN* An Event is produced
  *THEN* The Event will be labelled as produced by "instance `A`"

* Event consumption

  *GIVEN* A Gerrit Events consumer
  *WHEN* An Event without the instance of origin is consumed
  *THEN* The Gerrit Events consumer will have to consume it anyway
