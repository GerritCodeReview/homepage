---
title: ""
permalink: design-docs/solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

The proposed solution would be having a dedicated configuration (i.e.: `instanceId`)
used to identify the instance.

## <a id="implementation"> Implementation

### Setup

The `instanceId` could be added in the `gerrit.config` under the `gerrit` section.
It could be automatically initialised when not present at service startup,
similarly to how the `serverId` is generated today.

The id could be a UUIDv4 to avoid the need of a central authority for the generation
of a unique ID.

### Propagation

Each event will need to be labelled with the `instanceId` it has been
generated from.
The `com.google.gerrit.server.events.Event` will need to be modified to accommodate
the new parameter.

### Exposing the identifier

Gerrit will have to expose the local `instanceId` so plugins can use it.
his can be done with a new @InstanceId annotation.

# Current consumers compatibility

## Gerrit Jenkins Trigger Plugin

The addition of an `instanceId` in the Events won’t affect the Gerrit Jenkins
Trigger Plugin, since the DTO used is really lax and decoupled from Gerrit.
Additional fields added to the Event will just be ignored.

## Other plugins

I used [this query](https://cs.bazel.build/search?q=r%3Aplugin++com.google.gerrit.server.events.Event&num=200)
and [this other one](https://github.com/search?l=Java&q=org%3AGerritForge+%22events.Event%22+NOT+Test&type=Code)
to assess the plugins that might be impacted by the change of the
`com.google.gerrit.server.events.Event`.

Plugins that would need adaptation with this change will be the
_multi-site_ and the _events-broker_ since they will have to start using the core
`instanceId` instead of the multi-site definition of `instanceId`.

The _events-log_ plugin, used for example by the Gerrit Jenkins Trigger Plugin,
might also need extra work to store the extra field in the database.
A database schema migration will also be needed.

The _high-availability_ won't need to be modified, but there will be the chance
of simplifying it and make it more resilient, since it won't have to store the
forwarded events in the thread local storage anymore.

## <a id="use-case-fulfilment"> Use case fulfilment

This solution would satisfy the [use cases](/design-docs/instance-id-use-cases.md)
presented in the description of the problem.

Having the `instanceId` will allow to inspect the event payload to understand its origin.

Let's analyse the by-products:

* _Avoid loops:_ events with the same `instanceId` of the consuming instance
can be filtered out, avoiding creation of loops. Plugins like the `high-availability`
can be simplified avoiding to store in memory the forwarded events to keep track
of the origin.
* _Priority routing_: logic can be implemented around `instanceId` of an event to
decide which one to consume first depending on its origin.
Discoverability of the other instances in the cluster is not part of this work.
* _Troubleshooting_: `instanceId` can be dumped in log if needed. This is already possible
only the extra field will be present as well.
* _Preventing events duplication_: if we take the case of the Slack plugin, notifications
can be sent only from the instance producing the event
(i.e.: `instanceId` of the event == `instanceId` of the Gerrit instance). This will
prevent multiple notifications.
This scenario is the dual of the first one, _Avoid loops_.
In this case instance producing an event wants to perform some operations when
consuming it, in the other case we just want a no-ops.
