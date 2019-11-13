---
title: "Design Doc - Threaded Change Log - Solution"
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Threaded Change Messages

## <a id="overview"> Overview

When user replies to the review message (using `REPLY` button in
`Change Log` entry) original message content is used as a source of
the new message however relation between them is not captured.

Solution would be to store the reference to the message that reply
refers to. In terms of `unresolved` bit it should be also added
to the change message body.

## <a id="detailed-design"> Detailed Design

User's feedback will be divided into two parts:
* *notarial part* that contains automatically generated description of performed
  action (e.g. _Uploaded patch set 6._, _Patch Set 6: Code-Review+1_, etc.)
  that is still going to be stored in
  [ChangeMessage](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/entities/ChangeMessage.java)
  (no changes here);
* *feedback part* - written by the reviewer; it will be stored as
  [Comment](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/entities/Comment.java)
  entity with a reference to patch set and optionally reference to a different
  comment (when `Change Log` entry `REPLY` button was used to create it)

UI will be responsible to present `Change Log` notarial part of feedback
linearly, similarly to what is being presented now. Feedback parts will be
visible in `Comment Threads` tab (tab rules of showing
`Only unresolved thread`, etc. applied).

### <a id="scalability"> Scalability

No scalability impact is expected:
* *notarial part* is going to be stored as it was before
* *feedback part* is going to be stored the same way as we do for _comments_
  and _robocomments_: to be decided if existing `/meta` ref should be used and
  [RevisionNoteData](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/server/notedb/RevisionNoteData.java)
  entity extended with list of dedicated type (could be `Comment` descendant
  but considering review feedback it would be more likely dedicated entity)
  or different (e.g. `/feedback`) ref should be introduced and new NoteDB entity
  created.

## <a id="alternatives-considered"> Alternatives Considered

Building message threads by analysis of change message content. That seems
to be substantial computational effort (to be performed on client side)
and is not guaranteed to deliver stable/valid results.

## <a id="pros-and-cons"> Pros and Cons

* clear indication of user's review comments relation that can be effectively
  used in `Comment Threads` UI to present data to user

## <a id="implementation-plan"> Implementation Plan

1. Rework general `REPLY` dialog so that notarial part is stored in
  [ChangeMessage](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/entities/ChangeMessage.java)
  entity and feedback part is stored in
  [Comment](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/entities/Comment.java)
  entity.

  Extend corresponding endpoint to publish `Change Message` and `Comment` at
  once.

  There is no plan to migrate existing messages to split them into notarial
  and feedback part which practically means that they will be seen as notarial.

  Existing review rules need to be revised and modified in case it is necessary
  e.g. `all comments resolved` is the one to be updated, but there might be
  more down the road.

2. Modify UI so that:
  * Reviewer can mark review feedback as one that needs to be resolved.
    By default current state is preserved and feedback doesn't require any
    resolution.
  * When `Change Log` message `REPLY` button is used it doesn't result in
    general review feedback dialog being opened. Small dialog like the one for
    inline comment is opened. `SAVE` action results in reply being stored as
    draft.

    Original message id is provided to submitted entity (there is no longer
    a need to copy over original message body to reply dialog, yet it should
    be displayed for reference).
  * Multiple draft replies are published through general review feedback dialog
    (the same way as inline comments are published).
  * `Change Log` tab messages ordering is not impacted by this change.

## <a id="time-estimation"> Time Estimation

Backend: 2MW

UI: 1MW?
