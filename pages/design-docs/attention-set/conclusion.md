---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

## <a id="use-cases"> Use cases

The attention-set feature described in
[Design Doc - Attention Set - Use Cases](/design-docs/attention-set-use-cases.html)
is an innovative functionality for the future of Gerrit Code Review because of the following
characteristics:

1. Define in a transparent way who is expected to take the next action on a change.
2. Allows assignment of responsibility to reviewers.
3. Optimize the prioritization of work of the reviewer with a clearer UI.

## <a id="use-cases"> Solution space

Two solutions were proposed:

1. A from-scratch implementation next to 'assignee' in core by Ben Rohlfs (I11578a4c)
2. An implementation based on iterative expansion of 'assignee' and with the option to
   be extended by plugins by Martin Fick (I6d56c0ea)

## <a id="use-cases"> Arguments

Ben’s solution satisfies the use-cases and defines a user-experience and workflow in Gerrit
core. There is one exception in that an author wants to know when reviewers will take action.
This is satisfied by the "Snoozing" feature currently listed as deferred
enhacement. However, there is a strong desire to get this implemented in the
first iteration.
Between the two solutions it is the more detailed one and includes UI mocks. The
user-interface proposed looks clean and well-thought out. His solution suggests implementing
the feature in one-go with iterations on the UI. The solution would be a separate feature to
‘assignee’. There is a concern about maintainability and user-confusion around this fact.
Desire for more granular states (strict attention, loose attention) was expressed in the
review but is not currently addressed.

In the first part, Martin’s solution presents an alternative by setting up rules on top of
the existing ‘assignee’ feature. This iteration does not satisfy all use-cases for the
plurality of actions (by the virtue of having a single 'assignee') and features
related to snoozing. There is a concern for reviews becoming sequential instead of parallel
increasing review time.
The second part of the proposal talks about iterating on ‘assignee’ to allow multiple
assignees at the same time which is a shift in strategy. This part has some overlap with
Ben’s proposal but differs in where the rules for modifying the attention set reside.
Martin’s proposal here can be extended by plugins, while Ben’s is favoring rules to sit in
Gerrit core with not current plan to be extended (though, there seems to be no
technical reason why this would not be possible).
The proposal is vague as to how some use cases are addressed but since it’s of iterative
nature it should receive the benefit of doubt.

In their end state, there is a difference in that with Ben's solution, 'assignee' continues
to be a supported feature in Gerrit - though off by default - while in Martin's solution
'assignee' and 'attention set' are the same feature. As the use-case doc outlines, there
is a large overlap between 'assignee' and 'attention set'.

There are technical reasons to prefer an implementation in one-go to an iterative
implementation. Most proposed iterations require upgrading the change index - one of the
tasks that administrators of large Gerrit instances struggle with upon upgrading their
instance. NoteDb format changes that need schema migrations that require re-writing change
meta refs being the other.

The main differences between the proposals occur across the following dimensions:
1. Keeping assignee vs. not keeping assignee
   There is a preference to not keep assignee for maintainability and UX reasons. (favoring
   Martin’s proposal)
2. Being a singular assignment vs having multiple people’s attention
   There is a preference to have multiple people’s attention to not force reviews to occur
   in sequence. (in the end state, both proposals are the same here)
3. Iterating on an existing feature vs. creating a new one and deprecating the exsting
   'Assignee' and 'Attention set' are close, but not the same. There is a preference to
   start fresh with 'Attention set' instead of adding to an existing concept
   iteratively and break APIs (potentially multiple times) and going through
   hops to explain the new intention behind existing, but changed functionality.
   (favoring Ben’s proposal)
4. Promise on timeline and implementation
   There is a preference to approve a proposal with a promise to implement and a timeline
   for that implementation. (favoring Ben’s proposal)

## <a id="use-cases"> Decision

We will therefore go with Ben's proposal. We will incorporate Martin's idea of ending up with
just a single feature instead of two largely overlapping ones by asking Ben to amend his
proposal to put forward a viable migration plan for migrating remaining use cases from
'assignee' to attention set. The sparring partner for this migration is Axis as the original
implementer and one of the few currently known users of the assignee feature where the
use-case would not be captured 100% by ‘attention set’.

## <a id="solution-design"> Implementation Remarks

This section gives brief feedback on the chosen design. Its intention is to highlight areas
that need thought during implementation to ensure the success of the feature.

The user-interface proposed looks clean and good enough as a first iteration of the new
attention set functionality. It is not expected to be perfect for everyone at the beginning
but can be later on refined in subsequent releases of Gerrit beyond v3.2. The success of
the adoption of the attention set will also be measured on how the interface will be able
to evolve based on user feedback.

The workflow proposed looks reasonable and will allow common-sense defaults that will guide
new users on what is expected from them.

The implementation would need further details on how the whole feature is going to be
designed in terms of API, plugin extensions and scalability in multi-site deployments.
Also, the migration of existing storage (e.g. how do we bootstrap attention set for existing
changes) would need to be assessed and managed properly during the design and implementation
phase.

Extensions and integrations with other plugins (e.g. owners, reviewers) would need to be
at least designed and defined in the Plugin API interface. However, having an attention
set hook is not a formal requirement.

## <a id="implementation-plan"> Implementation Plan

Ben Rohlfs (Google) is driving the implementation, which is expected to
involve other Google engineers and potentially contributors from other organisations.
The first planned release of the attention-set is Gerrit v3.2 (Apr/May 2020).
