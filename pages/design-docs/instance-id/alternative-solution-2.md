---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

An alternative solution would be having a dedicated configuration (i.e.: `instanceId`)
used to identify the instance.

## <a id="implementation"> Implementation

### Setup

The `instanceId` could be added in the `gerrit.config` under the `gerrit` section.
It could be automatically initialised when not present at service startup,
similarly to how the `serverId` is generated today.

The id could be a UUIDv4 to avoid the need of a central authority for the generation
of a unique ID.

### Propagation

Propagation of the id in the events can be done as explained in
[Proposed solution](/design-docs/instance-id-solution.md) or
[Alternative Solution - 1](/design-docs/instance-id-alternative-solution-1.md).

## <a id="advantages"> Advantages

The advantages of this solution is that we will have a configuration which is
only responsibility of identify an instance.

We won't have to couple other parameters, for example the `instanceName`, to a
role they weren't necessarily created for.
