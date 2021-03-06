---
title: ""
permalink: design-docs/instance-id-alternative-solution-1.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

Gerrit has already a [parameter](https://gerrit-documentation.storage.googleapis.com/Documentation/3.1.4/config-gerrit.html#gerrit.instanceName)
to define an identifier for the instances. This could be included in the events
generated by the different nodes.

## <a id="implementation"> Implementation

### Setup

The `instanceName` is currently set in the `gerrit.config`. It defaults to the
full hostname if not set in `gerrit.instanceName`.

### Propagation

Propagation of the id in the events can be done as explained in
[Proposed solution](/design-docs/instance-id-solution.html) or
[Alternative Solution - 2](/design-docs/instance-id-alternative-solution-2.html).

## <a id="limitations"> Limitations

`instanceName` is not used to uniquely identify an instance in a cluster.

For example, it is, available to the email templating system.

Using it would couple the presentation logic to something more backend specific
as identifying an instance in a cluster.
Also, it could not necessarily be relevant for the end users receiving it in
their inbox.

## <a id="use-case-fulfilment"> Use case fulfilment

Same consideration as in the proposed [solution](/design-docs/instance-id-solution.html)
