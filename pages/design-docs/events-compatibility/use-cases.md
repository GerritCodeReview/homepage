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
A good example of the situation when changing the contract cause an issue with the
rolling upgrade was a change in the serialization of the project field name in the
StreamEvent class([Change](https://gerrit-review.googlesource.com/c/gerrit/+/79952))
from an object
`"project": { "name" : "project-name" }` to a string `"project":"project-name"`.
After this change events generated on Gerrit v3.1 could not be deserialised on Gerrit
v3.0. This completely blocked the rolling upgrade. To fix that situation [custom
type adapter](https://bugs.chromium.org/p/gerrit/issues/detail?id=13825) had to be introduced in high-availability
and multi-site plugins in v3.0 with the logic copied from Gerrit Core v3.1. Then we had to rollback this
code in both plugins in v3.1. This approach contains several issues:
..* requires a lot of copy&paste and custom logic to handle serialisation/deserialisation
..* requires extra release of high-availability and multi-site plugins for previous
stable version
..* rolling upgrade are more complicated because first we have to upgrade plugins to
the version with the code which can handle two contracts and then start upgrade.

* _A/B testing:_ As a by-product of the rolling upgrades. Gerrit admin should be
able to switch part of the nodes to the new version, redirect part of the traffic
to the upgraded nodes and perform comparison.  During that process nodes must be
able to broadcast/deserialized events even if they use different structures.

2. CI Integration - Changing semantic for the event payload(e.g. field renaming)
should not break existing integrations with CI systems.

3. Third party code integration - Exposing events contract allows easy integration
of third party code with the Gerrit stream events. We already have some external projects/libraries
which could benefit from that. For example [gerrit-rest-java-client](https://github.com/uwolfer/gerrit-rest-java-client) - [this](https://github.com/uwolfer/gerrit-rest-java-client/tree/master/src/main/java/com/google/gerrit/extensions/common) package contains the code which is a copy and paste
of the Gerrit core code. Another example is [gerrit-events](https://github.com/sonyxperiadev/gerrit-events) - [package](https://github.com/sonyxperiadev/gerrit-events/tree/master/src/main/java/com/sonymobile/tools/gerrit/gerritevents/dto/events) with all the Gerrit stream events rewritten.
The main problem with those two projects is that every change in the events structure
needs to be manually updated in those project. With the contract exposed by Gerrit
third party code can generate events classes from the contract. Another benefit is
that code generation can be done for many programming languages not just for Java.

4. Automatic code generation - Having events contract allows to generate code for
serialisation/deserialization so there is no need to code that functionality manually.
With the automatic code generation for serialisation/deserialisation issues like [this](https://bugs.chromium.org/p/gerrit/issues/detail?id=12315) could be easily avoided because there would be no need to repeat
serialisation/deserialisation logic in different parts of the system. Also we would not have to
implement all the logic manually. Even if some parts of the code could not use
serialisation/deserialisation from Gerrit core generated code will cover the same functionality.



## <a id="acceptance-criteria"> Acceptance Criteria

* Gerrit exposes contract for each event type.
* Event contract allows evolution with both backward and forward compatibility.
* Gerrit produces events stream serialised with the new contract side-by-side with
existing JSON events (if requested) for compatibility reasons.
* The client (or the configuration) should select in which format events
should be generated.
* The format should be independent from the transport, allowing the same format to
be reused across different channels:
..* SSH stream events
..* Webhooks
..* Other pub-sub events broker (e.g. RabbitMQ, Kafka, Kinesis, GCloud, others)
