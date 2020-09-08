---
title: ""
sidebar: gerritdoc_sidebar
permalink: design-docs/reworked-event-system-background.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/reworked-event-system
---

# Background

## Current system/approach

Gerrit has a concept called "extension points", which allows plugins and the
more limited extensions (see
[Gerrit's documentation](https://gerrit-review.googlesource.com/Documentation/dev-plugins.html)
for the distinction between the two) to hook in additional logic or react to
specific actions/events. Those extension points are represented by annotated
interfaces, for which plugins and extensions may provide implementations.

Gerrit has several extension points to listen to "Gerrit events" which
are triggered on various actions (e.g. change is merged; vote of a label is
changed). Invoking the extension points typically happens after the actions were
successfully executed and isn't guaranteed. The same mechanism is also used to
send out
[SSH events](https://gerrit-review.googlesource.com/Documentation/cmd-stream-events.html)
(also referred to as stream events).

The extension points for "Gerrit events" are arranged in two dependent layers.
The first one is available to both plugins and extensions and the second one
only to plugins. This requires all transferred data to be copied to classes
available to extensions.

![Structure of current event system](/images/design-docs/reworked-event-system/current-event-system-structure.png)

The first layer generally consists of individual extension points for each event
type. It also contains a bunch of extension points (e.g. HeadUpdatedListener,
ChangeIndexedListener) for "Gerrit events" which aren't sent out via SSH and
hence never delegated to the second layer.

![First layer of current event system](/images/design-docs/reworked-event-system/current-first-layer.png)

The second layer consists of two extension points (one with visibility
restriction, the other without) which handle events arranged in a hierarchy.

![Second layer of current event system](/images/design-docs/reworked-event-system/current-second-layer.png)

Plugins also have the possibility to send generic "events" (= predefined type
with payload encoded as string) to themselves or each other via a dedicated
service.

![Current service for custom plugin events](/images/design-docs/reworked-event-system/current-service-for-custom-plugin-events.png)

## <a id="current-stream-events"> Current stream events
* Assignee Changed
* Change Abandoned
* Change Merged
* Change Restored
* Comment Added
* (Dropped Output) (SSH only)
* Hashtags Changed
* Project Created
* Patchset Created
* Ref Updated
* Reviewer Added
* Reviewer Deleted
* Topic Changed
* Work in Progress State Changed
* Private State Changed
* Vote Deleted

## <a id="current-issues"> Issues with the current approach
* Confusing structure.
* Innermost events available to extensions.
  * Limitations on used (Java) types.
  * Unnecessary copying of a lot of data.
  * No "internal" events possible.
* Different approach for innermost events (-> listener) vs. stream events
  (-> event hierarchy)
* Confusing events.
  * Missing events (e.g. no VoteAddedEvent)
  * Sometimes aggregate actions ("Hashtags Changed"), sometimes singular actions
    ("Reviewer Added").
  * Sometimes aggregate states, sometimes single states. (e.g. "Work in Progess
    State Changed" vs. "Change Abandoned"/"Change Merged")
* Incomplete privacy/security story.

### Some additional details

#### Confusing structure
It's counter-intuitive that the current mechanism first sends a lot of details
to both extensions and plugins before sending a chunk of it only to plugins
again.

In addition, plugin developers might be confused by the seemingly duplicate
extension points. On the other hand, extension developers might not even know
about some of the extension points of the first layer as those are undocumented.

Another source for confusion could be the different approach chosen for the two
layers: the first layer introduces a dedicated extension point for each type
whereas the second layer organizes the types in a hierarchy and passes them
through one extension point.

#### Inefficient data copying
The current mechanism copies and populates a lot of data, which is not necessary
for every receiver of an internal/external event. Hence, that's very
inefficient. This could get even worse in the future if further fields are added
to the widely used data objects wrapped in the events due to a completely
unrelated reason. All in all, it's safer if the mechanism is minimal and it's
code and dependencies are controllable.

#### Incomplete privacy/security story
Not every external event channel allows to filter events to the receiver taking
Gerrit visibility rules into account. If not done properly or at all, this can
represent a security or privacy leak (e.g. commit message of a private change
or of changes in a restricted repository is readable to everybody; spreading
email addresses of users who shouldn't be publicly visible). Event channels
which don't support this additional filtering will need to be used with extreme
care (e.g. limiting the access to such event channels only to very trusted
systems).

## <a id="related-issues"> Related issues
The following issues are topics on their own and hence aren't discussed in the
proposed solution.

#### No atomicity
The current event system doesn't ensure that events are sent out exactly when
an action was successful in Gerrit (-> atomicity). Instead,
Gerrit sends events on a best effort basis. If the corresponding action
failed, Gerrit won't send out an event.

Ideally, we should improve this in the future. When we do so, we should consider
that events are currently only sent out after other important
Gerrit-specific operations/mutations have finished (like indexing a change).
If we sent out the events already with the Git reference updates in NoteDb,
receivers might observe an inconsistent Gerrit state (e.g. change was created but can’t
be found via an index query).

#### Eventual consistency
In some setups (e.g. multi-master), Gerrit instances are spread over several
machines. Data from one machine is automatically propagated to other machines,
albeit with a non-avoidable delay.

With external events, this scenario becomes more critical as receivers of
external events expect to reliably be able to fetch the corresponding data from
Gerrit as soon as they get an event. At the moment, such receivers need to use a
repeated fetch strategy with exponential backoff.

If we wanted to solve this, we'd need to add a mechanism which allows
consistency-on-demand.