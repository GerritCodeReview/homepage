---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

Given a multi-master, single or multi-site, Gerrit setup, it is not possible to
determine, from which node an Event has been produced.
Events don’t keep track of node they were generated from, they only carry
information about their type and creation time.

## `serverId` Vs `instanceName`: Cluster and Instance unique identifier

In the Gerrit configuration it is possible to specify two different identifiers:
`serverId`: the identifier of the cluster a Gerrit node belongs to
`instanceName`: a short identifier for a Gerrit instance

### `serverId`

The `serverId` is used as a signature of the review metadata associated to a change.
Normally, only nodes belonging to the same cluster can read the metadata associated
within the same cluster.

Let’s take the example of two Gerrit masters, A and B, sharing the same repositories
(either via NFS or replication) with different `serverId`s. The reviews created
on node A, are not visible to node B, and vice-versa.

For this reason, whenever in a multi-master setup, the `serverId` of the nodes
belonging to the cluster must be the same.

### `instanceName`

The `instanceName` is made available to the mailing template engine, hence it can
be used in the emails’ content.

## The missing Event source field

In a multi-master setup, High Availability or multi-site, the events are broadcasted
to all the instances.

However, currently, it not possible to understand which instance in the cluster
generated an Event. Making the `instanceName` available in the Event could solve
this problem.

# Use-cases

In a multi-master setup, [multi-site](https://gerrit.googlesource.com/plugins/multi-site/)
or [HA](https://gerrit.googlesource.com/plugins/high-availability/),
where each Gerrit instance can broadcast Events, it is fundamental to understand
where an event has been generated.

Here some uses cases:

* _Avoid loops:_ in a multi-site setup events are broadcasted to topics. Each
instance produces and consumes from the same topic. Having the `instanceName` in
the events generated would help to avoid consuming events generated from the same instance.
* _Metrics_: measure the lag between the production and consumption of an Event
* _Smart routing_: prioritise consumption from a particular instance when the
replication queues are loaded
* _Debugging_: exposing which instance is serving a request
* _Preventing events duplication_: when listening to events through plugins
(e.g. Slack integration) a single event would be consumed by all the plugins on
the cluster, causing duplication of notifications (e.g. Slack would repeat the same
message a number of times equal to the number of nodes).
`instanceName` would allow plugins to avoid that behaviour.

## <a id="acceptance-criteria"> Acceptance Criteria

* Each instance will have to add the `instanceName` to each event generated
* Event consumers will need to be backward compatible and able to consume Events
even without `instanceName`
