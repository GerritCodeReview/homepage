---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

An alternative solution would be using a plugin to sign the events.

## <a id="implementation"> Implementation

This is how we could achieve it:
* intercept all the Events before they get fired from the `postEvent` method in
`com.google.gerrit.server.events.EventBroker`
* create a new event type (i.e.: `SingnedEvent`) as a wrapper of the Event class,
containing the `instanceName` as an additional field
* all the plugins which need to know the origin of an Event will have to use the
`SignedEvent` class as a base class to extend Events from

This will sign all the events, but the replication one, which are fundamental in
a multi-master setup.

To sign the replication events the core plugin will need to be modified to expose
the `postEvent` method and allow to override it.

## <a id="limitations"> Limitations

A by-product of adding the `instanceName` in the core Events, as proposed in the
main solution, is that it will be easier to get important metrics, like the
replication lag, out of the box in multiple instance scenarios using the
replication plugin.

Adding the `instanceName` via a plugin will make those metrics more difficult to
gather.
