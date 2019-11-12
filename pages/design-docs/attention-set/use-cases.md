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
*   As a user I want to see if and why a certain change needs or does not need my or someone else’s
    attention.
*   As a user, if I think that a change needs attention by a user, then I want that user and
    everyone else to think the same.
*   As a user I want to be able to explicitly change the state of who is currently responsible for
    taking action.
*   As an owner or co-author I want to make sure that my reviews are making good progress. When I am
    in doubt about that, I want to know if and when my reviewers are going to review my change.
*   As a user I want to be notified by email if (and often only if) my attention is required.

## <a id="secondary">Secondary Use Cases

*   As a user I want to be assisted with changing the responsibility for taking action as much as
    possible, e.g. I should not have to pass the responsibility from me to the owner when I am
    publishing comments.
*   As a change owner I want to set expectations about what I want from each reviewer.
*   As a reviewer I want to set expectations about when I will be able to review a change (being out
    of office, being in a different time zone, or being otherwise busy).
*   As a user I don't want to be responsible for taking action when I am waiting for reviewers to
    comment or when I am waiting for the author to resolve comments.
*   As a user I want to snooze the responsibility for taking action when ...
    *   ... I am waiting for tests or other checks to finish.
    *   ... I am waiting for the parent or some other change to be merged, reviewed, or released.
    *   ... I am out of office.
*   As a developer I want to change the responsibility for taking action using an API.

## <a id="non-goals">Non-Goals

Finding and adding reviewers is a separate use case, but it is overlapping. So while this design
does not aim to improve it directly, it should also not make it worse and should integrate well with
potential improvements to it.

Knowing whether it is my turn to act on a change is very much tied to a real-time notification
system, because you want to know as soon as possible, when the state of a change changes such action
is required from your side. Gerrit currently sends notifications to users by email. While sending
less spammy email notifications may be a nice-to-have side effect, the goal of this design is not to
fix or improve email notifications in general.

## <a id="acceptance">Acceptance Criteria

Generally the acceptance criterion is that all primary use cases are addressed well and ideally also
many secondary use cases are covered. Mapping the use cases to how Gerrit works this can be
translated to:

*   Changes requiring action must be prominently called out on the dashboard.
*   The change page must have a clear indication at the top (e.g. in the change metadata) from whom
    action is required. This must be presented in the same way for all users looking at that page.
*   Both on the dashboard and the change page there must be a discoverable UI element for manually
    modifying the state of whose action is required.

## <a id="background">Background

At a high level, the code review workflow has the aim of moving a change through the review process
to enable submitting it to the code base after getting the necessary approvals. As this may take
anywhere from a few hours to days, being able to understand which state this process is in and who
should take which action next is paramount to be able to track progress. As mentioned above, it is
the latter part that we aim to improve with this proposal.

Google’s internal code review system Critique launched an "Attention Set" feature in 2015 to address
similar problems with the code review workflow as described [here](#status-quo). It was extremely
well received and has become a vital part of the code review system. Critique’s current design of
the attention set and its known shortcomings are influencing this design proposal.

Gerrit already has two features that partially help with understanding whose turn it is: Assignee
and Reviewed.

The assignee is one user that is singled out as being responsible for taking action on
a change. It can and must be set and changed manually from the change page (or by using the REST
API). This feature is often used to express urgency or priority when reviews are not moving forward.

The “Reviewed” flag is a way for every user to mark a patchset as reviewed (only visibile to
themselves), which will be reflected in normal/bold font rendering on the dashboard. Uploading a
new patchset will set the state to "unreviewed" for all reviewers. A secondary change action on the
change page allows the user to change its state (https://imgur.com/4JaOWSb).

## <a id="status-quo">Status Quo

What are the problems with the status quo apart from some use cases not being addressed at all?

*   The Assignee feature is in a good position to address most use cases, but has shortcomings:
    *   It is designed to address a separate use case where reviews are not moving forward and the
        owner wants to single out one person to resolve this blockage with some urgency. The feature
        is not meant to be used on every change as a "normal" attention token.
    *   You have to manually set and unset assignee. The most common case where this is annoying is
        when you publish comments: You have to manually unassign yourself in a separate action after
        publishing comments.
    *   Only one user can be assigned, i.e. assigning multiple reviewers is not possible.
    *   Is not editable in the reply dialog, i.e. you cannot send a comment and unassign yourself in
        one go.
    *   It requires additional prime UI space in change metadata instead of for example rendering
        the assigned reviewer in a different way.
    *   The problems listed above lead to some users/teams ignoring the assignee value or actively
        asking others to not use it, e.g. on gerrit-review.googlesource.com. And there is no config
        option to turn the assignee feature off.
*   The Reviewed feature has shortcomings:
    *   The option to change the reviewed state is fairly hidden and a lot of users do not even know
        that “mark reviewed” exists or relates to bolding on the dashboard. Consequently, it is a
        rarely used feature of the Gerrit UI.
    *   The state changes to “not reviewed” on apparently random events (e.g. a new patch set was
        uploaded). By itself the occurrence of a random event is not well suited to translate into
        "action required". If "unreviewed" is meant to mean "action required", then Assignee and
        Reviewed would be competing with each other, and they would need to be reconciled.
    *   The reviewed state is strictly personal and not visible to other users, e.g. the owner
        cannot see which reviewers made progress and have marked the change as reviewed.
    *   The owner of a change cannot use the feature. Own changes are never bold on the dashboard.
*   Email messages are spammy:
    *   Currently, authors, reviewers and cc’ed users get an email for every change message, which
        includes newly uploaded patchsets, CI results and other auto-generated messages. Research
        found that users have trouble identifying relevant messages.
    *   Nevertheless, users also report that they rely on this channel as it provides a “natural
        queue” of things to work on.
