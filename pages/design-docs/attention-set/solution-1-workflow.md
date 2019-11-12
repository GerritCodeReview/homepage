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

We propose to establish an “Attention Set” per change that at each point in time contains the users
that are expected to take action on a change.

*Being in the attention set and being assigned is synonymous in this doc. In this doc "owner"
generally refers to "owner or uploader".*

Being in the attention set is a state that every user must understand and act on. The expectations
and obligations are the same for all users on all changes on all hosts. So as an owner for example
you can rely on reviewers to take action, if they are in the attention set.

A user in the attention set is required and expected to take action on a change, i.e. it is their
turn. More specifically:

*   As a reviewer you shouldn't have to concern yourself with changes that you are not assigned to.
*   As a reviewer you are expected to act, if you are assigned to a change. (That action can be
    removing yourself from the attention set.)
*   As an owner I can expect reviewers to take timely action, if they are assigned.

We are establishing the attention set as a first class citizen of the review process by building a
[User Interface](solution-1-user-interface.md) that emphasizes its importance and allows users to
see "at a glance" whose turn it is on both the dashboard and the change pages.

We define some simple [defaults](#defaults) for how the attention set should change for a few common
actions. In the reply dialog users will have fine grained control over attention set changes.

Only owner, uploader, reviewers and CCs can be in the attention set.

Email notifications about uploaded patch sets will not be sent anymore (only to the owner, if
someone else uploads a patchset). Reviewers will get emails when they are added to the attention
set, or when they are removed from the review.

We propose to drop the
[Reviewed](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#mark-as-reviewed)
feature and its associated
[bolding of change-list items](https://gerrit-review.googlesource.com/Documentation/dev-stars.html#reviewed-star).

We propose to keep the "Assignee" feature around, but new releases would have it turned off by
default, because for most hosts the overlap with the attention set is too big, and they don't have
a need for the urgency aspects of Assignee. OTOH hosts that make good use of the feature should be
able to keep using it.

## <a id="defaults">Defaults

In order to help the user, we propose to apply useful default modifications to the attention set
when standard review events happen. Each of the following defaults can be overridden when executing
the action in the user interface:

*   When reviewers are added they are added to the attention set.
*   When someone other than the owner uploads a patchset the owner is added to the attention set.
*   When a change is submitted or abandoned all users are removed from the attention set.
*   Replying (commenting, voting or just writing a change message) will remove the publishing user
    from the attention set.
    *   When a *reviewer* replies add the owner to the attention set. Refinements:
        *   For each comment thread that the reviewer replies to also add all participants of that
            thread to the attention set.
    *   When the *owner* replies add all reviewers to the attention set. Refinements:
        *   When the *uploader* replies also add the owner to the attention set.

The above defaults are also applied when using the API (but can also be overriden). For example if
the reviewers-by-blame plugin adds a reviewer, then that reviewer is also added to the attention
set.

The upload of a new patchset by itself is **not** associated with a default change of the attention
set. The owner may want to upload intermediate states or want to wait for CI systems before passing
back the attention to reviewers.   

These simple defaults are not expected to do the right thing in 100% of the cases, just maybe 90%.
The owner of a change is still expected to manage the attention set individually and make sure that
it reflects their expectations.

There are some special cases to be considered:

*   Work in Progress (WIP): When a change leaves WIP state with reviewers, then all reviewers are
    added to the attention set. When a change enters WIP state, then the attention set is cleared.
    While a change is in WIP state the defaults above for adding users to the attention set are not
    applied.
*   Merged and Private Changes: Will be handled with the same defaults as normal changes.

## <a id="expectations">Deferred Enhancement: Expectations

*This is an optional additional enhancement of the proposal. The above can be implemented with or
without it. Actually you could argue that it has nothing to do with the attention set.* :-)

*At the moment we are not planning to include "Expectations" in v1 of the Attention Set.*

We propose to associate every reviewer with an expectation message, which simply is "please review
my change" by default, but can be changed by the owner or the reviewer to something like "please
approve ownership once code review is completed" or "please vote on library compliance".

## <a id="snoozing">Deferred Enhancement: Snoozing/Pausing

*This is an optional additional enhancement of the proposal. The above can be implemented with or
without it.*

*At the moment we are not planning to include "Snoozing/Pausing" in v1 of the Attention Set.*

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

## <a id="implementation">Implementation Plan and Time Estimation

Will be implemented by Google and be ready for the 3.2 release.
