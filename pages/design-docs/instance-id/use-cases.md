---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Glossary

* `Event`: any class implementing the [com.google.gerrit.server.events.Event](https://github.com/GerritCodeReview/gerrit/blob/a53523971c2ba0e35cbf7254e28bbbc31241f752/java/com/google/gerrit/server/events/Event.java)
abstract class
* `Instance`: a running instance of Gerrit
* `Master`: Gerrit master
* `Replica`: Gerrit replica (or slave)
* `Topic`: a broker topic, i.e.: a stream of Events of the same category (`index`, `cache`, etc)

# Problem: Where is an Event coming from?

In a multi-master setup, high-availability or multi-site, events are broadcasted
to all the instances belonging to the same cluster and share the same repositories.

However, currently, each plugin implements its own strategy to understand which
instance in the cluster generated an Event.

Gerrit should provide a way of adding information to events that can help consumers
identify the initial source of the event (see why this is important in the
[Use-cases](#Use-cases) paragraph).

# Background

Given a multi-master, single or multi-site, Gerrit setup, it is not possible to
determine, from which instance in the cluster an Event has been produced.

Events don’t keep track of the instance they were generated from, they only carry
information about their type and creation time.

In case of multi-master setup the events need to be broadcasted to all the
instances of the cluster.

This is fundamental to notify the replica instances on the activities happening on
the master and allow them to align. For example, indexes are not shared among instances.
To align them, `index` events from the master are broadcasted to the replicas,
notifying them an indexing action is required.

Currently any plugin uses its own way of deducing the origin of an Event.

Examples can be found in the `high-availability` and the `multi-site` plugin.
The former, for instance, flags the in flight Events as "forwarded" in the thread local storage.
The latter, adds the origin in an "envelope" wrapping the original Event.

Considering that multi-master setups are a common and fundamental use cases,
delegating the inferring of the Event origin to external plugins will lead to an
overall inconsistent architectures.

# Use-cases

* _Avoid loops:_ in a multi-site setup events are broadcasted to topics. Each
instance produces and consumes from the same topic. Events end up being consumed
and processed multiple times.

For example, let's analyse the following case: _index propagation in a multi-site
setup, where nodes are propagating reindexing events using a pub/sub message broker_

In this situation, assuming we have two instances, this is what will happen:
* Instance A: create change C1
* Instance A: index change C1
* Instance A: send `index C1 event` E1 to `index topic`
* Instance A: consumes index events E1 (it doesn't know it initially produced it)
* Instance B: consumes index events E1

Instance A ends up indexing twice the same change C1. This applies to all the
broadcasted events.

* _Priority routing_: prioritise consumption from a particular instance when the
replication queues are loaded
* _Troubleshooting_: exposing which instance is serving a request
* _Preventing events duplication_: when listening to events through plugins
(e.g. Slack integration) a single event would be consumed by all the instances,
causing duplication of notifications (e.g. Slack would be notified by each instance
with the same message).

# Acceptance Criteria

* Event source labelling

  *GIVEN* A Gerrit cluster with instances `G1` and `G2`
  *WHEN* `G1` produces an Event `E1`
  *THEN* `G1` and `G2` can understand `E1` was produced by `G1`
