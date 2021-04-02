---
title: "Design Doc - Events Compatibility - Use Cases"
permalink: design-docs/events-compatibility-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

Currently in Gerrit events are serialised using JSON format(e.g stream events or
web-hooks (events via HTTP)). This causes issues with serializing and deserializing
events across the Gerrit versions and also, at times, inside the same stable branch.
The reason why this happens is the lack of compatibility verification.
Lack of this functionality is limiting the ability to evolve the events structure
because every time the event structure is modified(field is renamed, deleted or type
is changed) it is breaking the contract and the event cannot be deserialized. For example
in Gerrit v3.3 a semantic variation for the stream events payload has broken the
"rebuild CI trigger" functionality. It has been worked around later in v3.3.1 with an
ad-hoc backward compatibility flag. Another downside of the current solution is the
verbosity of JSON format which can cause scalability issues for systems with a huge
load of pushes and remotes, because stream events are also used to broadcast replication
events that are used by the CI/CD systems.

# Use-cases

1. For a multiple primary nodes setup, [multi-site](https://gerrit.googlesource.com/plugins/multi-site/) or [HA](https://gerrit.googlesource.com/plugins/high-availability/),
where each Gerrit instance can broadcast events it is fundamental to be able to
serialize/deserialize events across different versions or releases.

Here some examples of uses cases:

* _Rolling upgrades:_ Even when the event contract was changed we should be able to
upgrade one primary node to the new version, perform testing and if all is well
switch traffic to the new node and upgrade the rest of them. During that process
nodes must be able to broadcast/consume events even if they use different event
structures. The biggest benefit is the ability to have zero downtime upgrades even
when the contract changes.

* _A/B testing:_ As a by-product of the rolling upgrades. Gerrit admin should be
able to switch part of the nodes to the new version, redirect part of the traffic
to the upgraded nodes and perform comparison.  During that process nodes must be
able to broadcast/deserialized events even if they use different structures.

2. CI Integration - Changing semantic for the event payload(e.g. field renaming)
should not break existing integrations with CI systems.

3. Third party code integration - Exposing events contract allows easy integration
of third party code with the Gerrit stream events.

4. Automatic code generation - Having events contract allows to generate code for
serialisation/deserialization so there is no need to code that functionality manually.

## <a id="acceptance-criteria"> Acceptance Criteria

* Gerrit exposes contract for each event type.
* Event contract allows evolution with both backward and forward compatibility.
* Gerrit produces events stream serialised with the new contract side-by-side with
existing JSON events (if requested) for compatibility reasons.
* The client (or the configuration) should select selects in which format events
should be generated.
* The format should be independent from the transport, allowing the same format to
be reused across different channels:
..* SSH stream events
..* Webhooks
..* Other pub-sub events broker (e.g. RabbitMQ, Kafka, Kinesis, GCloud, others)
