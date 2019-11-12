---
title: "Design Doc - Attention Set - Solution 1 - Workflow"
sidebar: gerritdoc_sidebar
permalink: design-doc-attention-set-solution-1-workflow.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/attention-set
---

# Solution 1 - Workflow

*Please read [Use Cases](use-cases.md) before this doc.*

## <a id="overview">Overview

We propose to extend the “Assignee” feature into an “Attention Set” and propose to drop the
[Reviewed](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#mark-as-reviewed)
feature and its associated
[bolding of change-list items](https://gerrit-review.googlesource.com/Documentation/dev-stars.html#reviewed-star).

*Being in the attention set and being assigned is synonymous in this doc. In this doc "Owner"
generally refers to "owner, committer or uploader".*

The attention set is a feature that every user must use and obey. It is not optional and can neither
be used just for some changes but not others.

A user in the attention set is required and expected to take action on a change, i.e. it is their
turn. More specifically:

*   As a reviewer you can ignore all changes that you are not assigned to.
*   As a reviewer you have to act, if you are assigned to a change. That action can be removing
    yourself from the attention set.
*   As an owner I can rely on reviewers to take timely action, if they are assigned.

We are establishing the attention set as a first class citizen of the review process by building a
[User Interface](solution-1-user-interface.md) that emphasizes its importance and allows users to
see "at a glance" whose turn it is on both the dashboard and the change pages.

We directly address the 4 shortcomings of the current "Assignee" feature as were listed in
[Use Cases](use-cases.md):

*   **You have to manually set the assignee:** We define some simple [defaults](#defaults) for how
    the attention set should change for a few common actions. The user can easily override these
    defaults and tweak assignments manually at any time. 
*   **Only one user can be assigned:** We allow multiple users to be assigned at the same time.
*   **Is not editable in the reply dialog:** We add a section that shows how the
    [defaults](#defaults) will change the attention set. And the user can interact with that section
    to override the defaults within the reply dialog.
*   **It requires additional prime UI space:** We remove the "assignee" row from the change
    metadata, but instead highlight users in the attention set with a prepended arrow style icon,
    see [User Interface](solution-1-user-interface.md).

Only owner, reviewers and CCs can be in the attention set.

Email notifications to reviewers will only be sent when they are added to the attention set, or when
they are removed from the review. Emails about new patch sets will be not be sent to reviewers anymore.

## <a id="defaults">Defaults

In order to help the user, we propose to apply useful default modifications to the attention set
when standard review events happen. Each of the following defaults can be overridden when executing
the action in the user interface:

*   When reviewers are added they are added to the attention set.
*   When a change is submitted all users are removed from the attention set.
*   Publishing a change message (with or without comments or votes) will remove the publishing user
    from the attention set.
    *   When a *reviewer* publishes a change message add the owner to the attention set.
    *   When the *owner* (or committer or uploader) publishes a change message add all reviewers to
        the attention set. (If the uploader is the publisher, then also the owner is added to the
        attention set.)

The above defaults are also applied when using the API. For example if the reviewers-by-blame plugin
adds a reviewer, then that reviewer is also added to the attention set.

The upload of a new patchset by itself is **not** associated with a default change of the attention
set.

These simple defaults are not expected to do the right thing in 100% of the cases, just maybe 90%.
The owner of a change is still expected to manage the attention set individually and make sure that
it reflects their expectations.

There are some special cases to be considered:

*   Work in Progress (WIP): When a change leaves WIP state with reviewers, then all reviewers are
    added to the attention set. When a change enters WIP state, then the attention set is cleared.
    While a change is in WIP state the defaults above for adding users to the attention set are not
    applied.
*   Merged and Private Changes: Will be handled with the same defaults as normal changes.

## <a id="expectations">Expectations

*This is an optional additional enhancement of the proposal. The above can be implemented with or
without it. Actually you could argue that it has nothing to do with the attention set.* :-)

*At the moment we are not planning to include "Expectations" in v1 of the Attention Set.*

We propose to associate every reviewer with an expectation message, which simply is "please review
my change" by default, but can be changed by the owner or the reviewer to something like "please
approve ownership once code review is completed" or "please vote on library compliance".

## <a id="snoozing">Snoozing

*This is an optional additional enhancement of the proposal. The above can be implemented with or
without it.*

The attention set proposal above assumes that at any point in time it is either the owner's or the
reviewers' turn to act on a change. But often a user may wait for some event to happen, so they
would like to unassign themselves until this event happens, and only then act on the code review.
Some example scenarios taken from [Use Cases](use-cases.md):

*   snooze for a fixed time (being out of office or otherwise busy)
*   wait for tests or other checks to finish
*   as an owner on a "ready to submit" change wait for the parent or some other change to be merged,
    reviewed, released
*   staged review: wait for a review from someone else (e.g. a shadowed reviewer), then assign
    another reviewer (e.g. a shadowing reviewer, or someone with +2 powers)

We propose to allow a snoozing condition to be associated with a user that is currently not in the
attention set.

## <a id="alternatives-considered">Alternatives Considered

Instead of replacing the current assignee feature we could implement the attention set
separately and either allow hosts to use one of the two features or even both at the same time.
Having both as core features would be confusing for new Gerrit users, because they are both
concerned with who is expected to take action. It would be an option though to keep the current
"assignee" feature alive, but turn it off by default, and allow hosts to optionally just use
the "assignee" instead of the "attention set".

The solution could have a configuration for forcing the attention set to be of at most size 1. That
would make it more similar to the current assignee feature. However, in the majority of the cases
the owner is the user that adds people to the attention set. So keeping only one user in the
attention set should work fine, even if Gerrit does not enforce it.

## <a id="pros-and-cons">Pros and Cons

TBD (suggestions welcome)

## <a id="implementation">Implementation Plan and Time Estimation

Will be implemented by Google and be ready for the 3.2 release.
