---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

An alternative solution would be using a plugin to label the events.

## <a id="implementation"> Implementation

This is how we could achieve it:
* intercept all the Events before they get fired from the `postEvent` method in
`com.google.gerrit.server.events.EventBroker`
* create a new event type (i.e.: `EventEnvelope`) as a wrapper of the Event class,
containing the `instanceName` as an additional field
* all the plugins which need to know the origin of an Event will have to use the
`EventEnvelope` class as a base class to extend Events from

This will label all the events, but the replication one, which are fundamental in
a multi-master setup.

To label the replication events the core plugin will need to be modified to expose
the `postEvent` method and allow to override it.

## <a id="limitations"> Limitations

A by-product of adding the `instanceName` in the core Events, as proposed in the
main solution, is that it will be easier to get important metrics, like the
replication lag, out of the box in multiple instance scenarios using the
replication plugin.

Adding the `instanceName` via a plugin will make those metrics more difficult to
gather.

Since the consumption of the EventEnvelope would be plugin-specific, another major
drawback will the more difficult integration with 3rd party systems (e.g. CI systems).
