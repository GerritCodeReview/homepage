---
title: ""
permalink: design-docs/instance-id-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Glossary

* `Event`: any class implementing the [com.google.gerrit.server.events.Event](https://github.com/GerritCodeReview/gerrit/blob/a53523971c2ba0e35cbf7254e28bbbc31241f752/java/com/google/gerrit/server/events/Event.java)
abstract class
* `Instance`: a running instance of Gerrit (a single JVM process)
* `Master`: Gerrit master
* `Replica`: Gerrit replica (or slave)
* `Topic`: a broker topic, i.e.: a stream of Events of the same category (`index`, `cache`, etc)

# Problem: Where is an Event coming from?

In a multi-master setup, high-availability or multi-site, events are broadcasted
among all the master instances belonging to the same cluster and share the same
repositories.

Currently, as a plugin developer, I cannot determine from which instances events
are coming from.

Each plugin implements its own strategy to understand the source of an event and
therefore we end up duplicating development effort.

Gerrit should provide a way of adding information to events that can help consumers
identify the initial source of the event.

# Background

Given a multi-master, single or multi-site, Gerrit setup, it is not possible to
determine, from which instance in the cluster an event has been produced.

Events don’t keep track of the instance they were generated from, they only carry
information about their type and creation time.

In case of multi-master setup the events need to be broadcasted to all the
instances of the cluster.

This is fundamental to notify other instances on the activities happening on
the master and allow them to align.

Currently any plugin uses its own way of deducing the origin of an event.

Examples can be found in the `high-availability` and the `multi-site` plugin.
The former, for instance, flags the in flight Events as "forwarded" in the thread local storage.
The latter, adds the origin in an "envelope" wrapping the original Event.

Considering that multi-master setups are a common and fundamental Gerrit usage,
inferring of the event origin shouldn't be delegated to external plugins.

# Use-case

  *AS* A Gerrit plugin developer
  *GIVEN* A Gerrit cluster with instances `G1` and `G2`
  *WHEN* `G1` produces an Event `E1`
  *THEN* I want to know `E1` was produced by `G1`

# By-product

Being able to determine the source of an event will simplify development of plugins
dealing with events. Here some examples of cases this additional information can
be used for:

* _Avoid loops:_ in a multi-site setup events are broadcasted to topics. Each
instance produces and consumes from the same topic. Events end up being consumed
and processed multiple times.
* _Priority routing_: prioritise consumption from a particular instance when the
replication queues are loaded
* _Troubleshooting_: exposing which instance is serving a request
* _Preventing events duplication_: when listening to events through plugins
(e.g. Slack integration) a single event would be consumed by all the instances,
causing duplication of notifications (e.g. Slack would be notified by each instance
with the same message).
