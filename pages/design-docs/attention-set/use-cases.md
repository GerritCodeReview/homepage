---
title: "Design Doc - Attention Set - Use Cases"
sidebar: gerritdoc_sidebar
permalink: design-doc-attention-set-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/attention-set
---

# Attention Set - Use Cases

## <a id="summary">Summary

Code Review is a turn-based workflow going back and forth between a change owner and reviewers.
Knowing who should be acting on a change next is thus a core part of this workflow. Not knowing
whose turn it is has been identified by research as a reason for several time-consuming behaviors,
such as adding more reviewers than necessary, checking the dashboard and bolded changes repeatedly
or abandoning the dashboard completely. Gerrit’s support for managing this part of the workflow is
substantially lacking, see [below](#status-quo).

## <a id="primary">Primary Use Cases

*   As a user I want to know at a glance which changes need my attention.
*   As an owner or co-author I want to make sure that my reviews are making good progress. When I am
    in doubt about that, I want to know if and when my reviewers are going to review my change.
*   As a user I want to be notified by email (or other means) if (and often only if) my attention is
    required.

## <a id="secondary">Secondary Use Cases

*   As a user I want to understand why a change needs or does not need my or someone else’s
    attention.
*   As a user I want to understand when and why the responsibility for taking action changes from
    one user to another.
*   As a user I want to be able to explicitly change the state of who is currently responsible for
    taking action.
*   As a user I want the responsibility for taking action being changed automatically as much as
    possible.
*   As as a change owner I want to set expectations about what I want from each reviewer.
*   As a reviewer I want to set expectations about when I will be able to review a change (being out
    of office or otherwise busy).
*   As a change owner or reviewer I want to set conditions about when the responsibility for taking
    action should change:
    *   wait for tests or other checks to finish
    *   wait for the parent or some other change to be merged, reviewed, released
    *   snooze while submission is in progress
    *   wait for a reviewer to be assigned
    *   snooze until an event or a fixed time (being ooo or otherwise busy)
    *   staged review: wait for a review from someone else (e.g. a shadowed reviewer), then assign
        another reviewer (e.g. a shadowing reviewer, or someone with +2 powers)
*   As a developer I want to change the responsibility for taking action using an API.
*   As a developer I want to implement new rules and conditions for changing the responsibility for
    taking action.
*   As an admin I want to set a default of rules and conditions about when the responsibility for
    taking action is passed back and forth.
*   As a user or researcher or product manager I want to get stats about code review latency and
    efficiency (e.g. for driving product decisions or for adhering to review SLAs):
    *   How long did the review take overall?
    *   Who was waiting for whom to take action for what amount of time?
    *   How long was the review progress stalled, because of external events such as reviewers being
        on vacation or tests running in the background?

## <a id="non-goals">Non-Goals

Finding and adding reviewers is a separate use case, but it is overlapping. So while this design
does not aim to improve it directly, it should also not make it worse and should integrate well with
potential improvements to it.

## <a id="acceptance">Acceptance Criteria

A solution is implemented (frontend and backend) and rolled out on master along with a release and
migration strategy for the 3.2 release. Rest APIs are in place and documented. Configuration options
and plugin endpoints are well defined and documented.

## <a id="background">Background

At a high level, the code review workflow has the aim of moving a change through the review process
to be able to submit it to the code base after getting the necessary approvals. As this may take
anywhere from a few hours to days, being able to understand which state this process is in and who
should be doing something next is paramount to be able to track progress. As mentioned above, it is
the latter part that we aim to improve with this proposal.

Google’s internal code review system Critique had similar problems (see [below](#status-quo)) with
the code review workflow as Gerrit and launched an “Attention Set” feature in 2015. It was extremely
well received and has become a vital part of the code review system. Critique’s current design of
the attention set and its known shortcomings are influencing this design proposal.

Gerrit already has two features that partially help with understanding whose turn it is: Assignee
and Reviewed. The assignee is one user that is singled out as being responsible for taking action on
a change. It can and must be set and changed manually from the change page (or by using the REST
API). The “Reviewed” flag is a way for every user to mark a patchset as reviewed, which will be
reflected in normal/bold font rendering on the dashboard. Uploading a new patchset will set the
state to "unreviewed" for all reviewers. A secondary change action on the change page allows the
user to change its state (https://imgur.com/4JaOWSb).

## <a id="status-quo">Status Quo

What are the problems with the status quo apart from some use cases not being addressed at all?

*   The Assignee and Reviewed features are competing with each other:
    *   Both features were made for clarifying the questions “What do I have to work on?” and “Whose
        turn is it?”, but they are not integrated with each other.
    *   Other users’ expectations are kept implicit. Is my reviewer expecting me to set them as
        assignee or will this rather annoy them? Does my reviewer pay attention to changes being
        bold (i.e. “unreviewed”) on the dashboard? Maybe both, maybe neither.
    *   If you have just reviewed a patchset and sent comments, then you are still assigned, if you
        don’t do anything, which in 99% of the cases is not what you want and creates an
        inconsistent state.
    *   You can change assignee and reviewed state directly, but as they are completely independent
        they won’t impact each other.
*   The Assignee feature has shortcomings:
    *   You have to manually set and unset assignee.
    *   Only one user can be assigned, i.e. assigning multiple reviewers is not possible.
    *   Is not editable in the reply dialog, i.e. you cannot send a comment and unassign yourself in
        one go.
    *   It requires additional prime UI space in change metadata instead of for example rendering
        the assigned reviewer in a different way.
*   The Reviewed feature has shortcomings:
    *   The option to change the reviewed state is fairly hidden and a lot users do not even know
        that “mark reviewed” exists or relates to bolding on the dashboard. Consequently, it is a
        little used feature of the Gerrit UI.
    *   The reviewed state is strictly personal and not visible to other users, e.g. the owner
        cannot see which reviewers have marked the change as reviewed.
    *   The owner of a change cannot use the feature. Own changes are never bold on the dashboard.
    *   The state changes to “not reviewed” as soon as a new patch set is uploaded, even if the
        owner has not responded to any comments.
*   Email messages are spammy:
    *   Currently, authors, reviewers and cc’ed users get an email for every change message, which
        includes newly uploaded patchsets, CI results and other auto-generated messages. Research
        found that users have trouble identifying relevant messages.
    *   Nevertheless, users also report that they rely on this channel as it provides a “natural
        queue” of things to work on.
