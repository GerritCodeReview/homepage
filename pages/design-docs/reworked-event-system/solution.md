---
title: ""
sidebar: gerritdoc_sidebar
permalink: design-docs/reworked-event-system-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/reworked-event-system
---

# Solution

## <a id="overview"> Overview

The new event system will be inspired by the existing SSH events but completely
reworked to only sent out the minimally necessary data in a better structured
way for efficiency, privacy, and consistency reasons.

Gerrit's internal mechanism for events will be reworked into two clear,
consistent layers: The first layer will be available only to Gerrit core and
plugins while the second layer of events/triggers will also be available to
Gerrit extensions. The transferred objects will be improved as well, with
efficiency and simplicity in mind. Plugins and extensions will need to migrate
their code to this new approach.

![Structure of new event system](/images/design-docs/reworked-event-system/new-event-system-structure.png)

The various existing extension points will be consolidated into one extension
point (= one type of listener) per layer. The various triggers will be
represented by different events which are organized in a hierarchy and passed to
the extension point as parameter. Events in the second layer which are supposed
to be sent out to external systems will be marked by a dedicated interface
(e.g. ExternalEvent).

![New event hierarchy](/images/design-docs/reworked-event-system/new-event-hierarchy.png)

Sending out SSH events will be moved to a plugin. There will be two variants of
the plugin: one which sends out SSH events as they currently are regarding
structure of events and data (for backwards compatibility) and another plugin
which will adopt the new, optimized design of the events.

## <a id="detailed-design"> Detailed Design

### Custom event bus
The described design effectively represents a custom event bus. It benefits from
features already implemented for the extension point mechanism in Gerrit, which
are among others: dedicated trace context for each plugin implementing the
extension point; metrics on latency; handling of exceptions raised in plugins.

To avoid errors related to using the two event extension points with different
settings e.g. regarding exception handling, we'll add two services which
delegate events to their corresponding extension point.

![New services for event firing](/images/design-docs/reworked-event-system/new-services-for-event-firing.png)

What the extension point mechanism doesn't involve compared to other
implementations of an event bus (e.g. Guava's EventBus) is built-in filtering of
events. Hence, receivers of events have to do the filtering on their own.

### Exception handling
All extension points related to events (with the exception of LifecycleListener
and inter-plugin events) currently swallow exceptions (including runtime
exceptions and errors) and only log them. This behavior is caused by the
exception handling for all extension points: If no checked exceptions are
specified, all unchecked exceptions are swallowed but if at least one checked
exception is specified, all unchecked exceptions are propagated. Swallowing all
unchecked exceptions in the former case is likely an oversight, which we'll
correct. As a consequence, we won't have to add special treatment for the
consolidated extension points.

### Events
#### Internal events
Events will be arranged in a hierarchy and any non-leaf elements will be
represented by interfaces (e.g. InternalEvent; ChangeEvent). Internal events
may contain sensitive content without further consideration as those events
remain within the boundaries of the server. They may also refer to internal
types as those events are only visible to Gerrit core and plugins. However,
such internal types should not represent rich objects (-> just internal
identifiers).

#### Application wide events
Application wide events are similar to internal events. The major difference is
that they may only refer to types available in Gerrit's extensions API. The data
sent as payload should be less than for internal events. To allow an efficient
implementation (e.g. by using adapters), events will be represented solely by
interfaces, which are arranged in a hierarchy.

#### External events
The current design of external events is suboptimal due to various
reasons. We should revise the format for the events completely.

Target improvements:
* Consistent API.
* Minimal payload.
* Avoidance of private/user content (or minimization if not possible otherwise).
* Good choice of identifiers for changes, patchsets, ... .
* Clearer naming.
* Ease of use.
* Reduced risk of user errors.

Open aspects:
* Whether to use events per individual or aggregated states.
* Which exact identifier to use for changes, patchsets, accounts, ... .
* Which identifier to use for the server account if it occurs on an event.
* Whether to provide a URL to the Gerrit server in the events (e.g. for related
  lookups).
* Whether to use separate events for change messages and comments.

#### Custom plugin events
The dedicated service for generic plugin events will be replaced by a dedicated
generic plugin event with string fields which can be passed to the extension
point for internal events. This mechanism allows plugins to send custom events
to other parts of themselves or to communicate beyond plugin boundaries. As
previously, this feature will only be available to plugins and not extensions.

### Facilitating external events
Sending out events to services outside of Gerrit is a common use case and hence
will be facilitated. As the used protocol, transport line, and format of the
events may differ from case to case, plugins need to cover those parts. Gerrit
core will only mark an opinionated set of events sent via the application wide
extension point with a dedicated interface e.g. ExternalEvent.

Plugins and extensions are free to take those external events and translate them
to whichever format and content for external events they want to send out. If
necessary, they can enrich the data by retrieving further details via regular
Gerrit APIs.

![New structure for sending external events](/images/design-docs/reworked-event-system/new-structure-for-sending-external-events.png)

### Push-then-pull approach
Transmitted data on all levels (internal events; application wide events; SSH or
other external events) will be reduced and especially kept to a minimum for
external events. To allow easy retrieval, events are guaranteed to use
appropriate identifiers for resources. Receivers of events will need to use
Gerrit APIs available to them (e.g. REST API, Java API, or low-level mechanisms)
to retrieve details which aren't included in events.

Other generators of external events (e.g. SSH event generator) are responsible
for the details they sent out when reacting to Gerrit events. The data sent
along the application wide events should be taken as guidance, though.

### Disregard of user scope
Events on all levels will be sent no matter who the current user of the
triggering action is. Furthermore, the offered extension points won't have a
mechanism to only receive events which are visible for a specific user as this
is a very rare use case. Receivers who need this (e.g. SSH event generator) have
to do the filtering themselves.

### Removed features of the existing approach
The existing mechanism acquired a lot of bells and whistles over the years which
introduce unnecessary complexity and inefficiency. Most of those aren't even
used in Gerrit core or core plugins. If possible, we won't migrate them over to
the new approach. That's open for discussion, though, and not written in stone.

Summary of known implications for users of the existing approach:
* There won't be a mechanism to filter events regarding user visibility. We
  might consider to offer a common class to which filtering can be delegated to
  keep the offered extension points clean and focused. (Known use case: SSH
  events)
* Events only contain a minimal set of data, which should also stay minimal in
  the future. Events will contain appropriate identifiers for resources so that
  receivers of events can easily retrieve further details if necessary. In some
  cases, this will require more lookups than currently but overall reduce the
  amount of data which is unnecessarily looked up and copied.
* Custom event types can't be registered for automatic
  serialization/deserialization for e.g. SSH events anymore. Instead, their
  content has to be encoded into the string fields of the generic plugin event.
  We might also consider to offer a dedicated generic event to differentiate
  between other inter-plugin communication.
* Notification settings won't be sent along with internal events. If this
  feature is still required by the community, we will either send dedicated
  events for notifiable actions or add the notification settings to some events
  (but not to all as the current approach does).
* The event dispatcher right before the second layer won't be interchangeable
  by plugins anymore. If the community really needs this, we'll consider to make
  the event converter in the new design pluggable.
* We won't support event types in Gerrit core which aren't used by at least the
  core plugins. Users of extension points like UsageDataPublishedListener will
  have to switch to the generic plugin event.

Further discrepancies discovered during the implementation will be handled on a
case-by-case basis while trying to keep the new extension points as clean and
simple as possible.

## <a id="alternatives-considered"> Alternatives Considered

### Using multiple extension points per layer
Instead of one extension point with an event hierarchy, we could introduce a
dedicated extension point per event type. Thus, implementing listeners wouldn't
need to filter for the desired event type on their own. On the other hand,
events couldn't be grouped into categories anymore, which reduces clarity and
also wouldn't allow to easily filter on these categories anymore. Arranging the
extension points itself into a hierarchy would remove the flexibility when
implementing them.

Another risk of multiple listeners is that their API could (and very likely
would) differ very much. With just one extension point, it's easier to achieve
consistency. Furthermore, one extension point rather gives the notion of an
event bus, even if it is a custom one.

### Having only one layer
It would be possible to combine both layers or rather leave one of them out. One
option would be to make the resulting events only visible to Gerrit core and
plugins. Doing so would break extensions which currently rely on the existing
mechanism without offering them an alternative. Hence, we decided against this
approach.

Another option would be to only offer application wide events. This would have
another drawback: We couldn't adapt events easily to our needs and still ensure
simplicity and efficiency in the future as we would be bound by our stability
guarantees for the extensions API. In addition, if we ever considered to
decouple different parts of Gerrit core by using events, we probably wouldn't
want to expose such events in a public, long-term API.

### Using Guava's EventBus
When using an event bus in Java, Guava's EventBus implementation is typically
the natural choice.

#### How to make EventBus properly work with Gerrit?
Instead of the proposed two extension points for the first and second layer,
we would use Guava's EventBus. Since Guava is already a Gerrit dependency, we
wouldn't even add a new one. That event bus would be available to both Gerrit
plugins and extensions. The two layers would be distinguished by two different
event hierarchies, of which only the second one would be visible to extensions
(exactly as in the design above). Because of this, we could use the same
instance of an EventBus for both layers and still have extensions only react to
the second.

To simplify registration to the EventBus and avoid errors related to it, we
would add auto-registration to our top-most Guice module for any class which is
handled by Guice. Handlers of events would only need to ensure that they are
spun up by Guice by e.g. declaring to be a singleton.

Instead of the trace context and latency metrics for each individual plugin, we
would only open one such context for each triggered event. To be able to do so,
we wouldn't use Guava's EventBus directly but hide it via an adapter behind our
own interface. This would also help to ensure that only plugins but not
extensions can use the event bus to post their own events.

By default, Guava's EventBus is configured to swallow (and log) any exceptions
which are thrown by the receiver of an event. We would add a handler which
always propagates unchecked exceptions.

#### Reasons to use Guava's EventBus
* Use of a refined, vetted event system.
* Less future maintenance burden due to less custom code.
* Built-in filtering on event types (and supertypes).
* Automatic registration with the event bus (see suggestion to support this
  above).
* Official move to an event system, hinting that an event based architecture is
  a valid option for future improvements (e.g. to decouple unrelated parts of
  the application).
* Always react gracefully to exceptions thrown by receivers of events and
  possibly do so on a per-event, per-context basis.

#### Reasons not to use Guava's EventBus
* Loss of per-plugin trace context and latency metrics.
* Unnecessary creation of the catch-all trace context if there aren't any
  receivers for an event.
* Additional entry point into plugins and extensions. We would have to remember
  to port any customizations for extension points also to the event bus
  mechanism.
* How to listen to events would be an additional, magic mechanism which plugin
  developers need to know.
* Special setup for plugin classloaders and interaction with extension points
  has already been in use and is working as far as we know. Using a classloader
  hierarchy with a single instance of Guava's EventBus would need to be tested
  for implications.
* More traffic on one bus. Compared to the two extension points for the two
  layers, all of the traffic goes through one wire.
* If we need to keep more of the specialties of the current event system, it's
  easier to support them via the extension points.

#### Considered sub-alternatives

##### One instance of EventBus per layer
To reduce traffic and enforce a better separation, we could use two separate
instances of EventBus: one for the first layer, another one for the second
layer. However, this could introduce developer confusion if an event was posted
on the wrong instance and listened to on the other one. It would also complicate
the suggested mechanism for automatic registration with the event bus as we
would need to explicitly identify which classes are provided by extensions.

##### Use EventBus for first layer, an extension point for second layer
Using the EventBus only for the first layer would give us a bit more flexibility
in the future as we wouldn't need to care about possibly breaking extensions at
those times. This would allow us to polish the integration of an EventBus in
Gerrit until we are satisfied with it before we possibly open it for extensions
at a later point in time. We might also decide to never open the EventBus to
extensions in order to keep a clear separation between internal-only and
application wide events.

This approach would introduce inconsistencies regarding event systems inside of
Gerrit, which could lead to developer confusion. Furthermore, we could possibly
remain a long time in this intermediate state as major releases for Gerrit don't
occur regularly (and we try to not break extensions on minor releases) or we
simply would forget about it.

### Custom plugin event types
Plugins use child classloaders which are separated from each other and are also
organized in separate Guice contexts. Hence, introducing and using new plugin
event types isn't as trivial as written currently in Gerrit's documentation and
might only work in some specific situations. To avoid future issues, we should
stop mentioning that possibility in Gerrit's documentation and actively
encourage the use of a generic plugin event.

### Backup plan for exception handling
If we decide that the previously described inconsistencies regarding exception
handling on extension points aren't an oversight, we will need special treatment
for lifecycle events. Unfortunately, the current mechanism doesn't allow to
specify exception handling based on the type of data/event passed. Hence, we
would need to further improve the current mechanism by e.g. adding a new type of
unchecked exception which is always re-thrown for any extension point no matter
what the specific settings are. Thus, users of extension points would always
have the option to signal a critical issue if they need to. Current
LifecycleListeners would have to switch to this new approach.

## <a id="security-considerations"> Security Considerations
### Interaction with private changes
Special considerations have to be made regarding private changes, which are
meant to be used for sensitive changes (e.g. security fixes) and thus need extra
care. Due to a security issue, private changes are currently disabled for most
of our hosts. However, we intend to fix the issues and eventually enable them
again. Those considerations will also be useful for another planned feature
which allows visibility restrictions per Git branch.
   
By sending out external events, receivers of such events could potentially
collect data about Gerrit changes which aren't visible to them in Gerrit.
Filtering the events per user isn't an option as the receivers aren't known at
the time the external event is generated (except if SSH channels with
authentication are used, which doesn't apply to all external events). The only
option we have is to rely on the push-then-pull approach and enforce visibility
checks when a receiver pulls additional data from Gerrit. Hence, we will take
extra care when considering which details to include in external events.

## <a id="privacy-considerations"> Privacy Considerations
In general, we'll try to keep user content (e.g. a commit message or a comment)
out of external events. If we find out that we can't follow that policy, we'll
reconsider possible implications. For further considerations, see the section
about security.

## <a id="testing-plan"> Testing Plan
Gerrit currently doesn't have any tests which ensure that events are sent for
their triggering actions. We will add tests for all internal and application
wide events.

## <a id="implementation-plan"> Implementation Plan

Nobody is driving this design at the moment. We are just providing it for
future reference/use.