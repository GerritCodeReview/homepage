---
title: ""
permalink: design-docs/alternative-solution-2.html
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

This would create dependency among plugins, which is a complicated pattern.

Linking of the plugins into the /lib directory would be complex, since we will have
to make sure the base plugin is loaded *before* the dependant one.

Also, a different JSON payload for the stream events, depending if you have or
not the plugin to enrich them, will be generated.

## <a id="use-case-fulfilment"> Use case fulfilment

Same consideration as in the proposed [solution](/design-docs/instance-id-solution.md).
The difference will be the fieldname (i.e.: `instanceName` instead of `instanceId`).
