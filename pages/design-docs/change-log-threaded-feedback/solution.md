---
title: "Design Doc - Change Log: Threaded Feedback - Solution"
permalink: design-docs/change-log-threaded-feedback-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Threaded Change Messages

## <a id="overview"> Overview

When user replies to the review message (using `REPLY` button in
`Change Log` entry) original message content is used as a source of
the new message however relation between them is not captured and
as a result harder to follow.

Solution would be to distinguish between the human feedback that is stored as
comment-like entity (and can be displayed in threads) and notarial part
(automatically generated descriptions like _Uploaded patch set X_, etc.) that
is presented linearly in `Change Log`.

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
  comment.

UI will be responsible to present `Change Log` notarial part of feedback
linearly, similarly to what is being presented now. Feedback parts will be
mentioned in `Change Log` e.g.
```
+------------------------------------------------
|
| User Name
| Patch Set 4:
| (2 comments)
|
+------------------------------------------------
|
| PS 4: The 1st feedback that requires resolution
| PS 4: The 2nd feedback that requires resolution
|
| a/file/path
|   Line 10: This is a line comment
|
+------------------------------------------------
```
and display in threads in `Comment Threads` tab (tab rules of showing
`Only unresolved thread`, etc. applied).

### <a id="scalability"> Scalability

No scalability impact is expected:
* *notarial part* is going to be stored as it was before
* *feedback part* is going to be stored the same way as we do for _comments_
  and _robotcomments_: to be decided if existing `/meta` ref should be used and
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
   and feedback part which practically means that they will be seen as
   notarial.

   Existing submit rules need to be revised and modified in case it is
   necessary (e.g. `all comments resolved` is the one to be updated). It has to
   be assured that file comments and feedback comments are displayed and
   handled properly in `Comment Threads` tab with/without filters applied.

1. Modify UI so that:
   * `Resolved` flag is visible and Reviewer can mark review feedback as one
     that needs to be resolved (default) or mark it as resolved (for
     appreciation).
   * There is no longer the `REPLY` button in `Change Log` next to the notarial
     entry related to review's feedback as it wouldn't allow to answer multiple
     threads. Instead reply should be performed in the `Comment Threads` tab
     (one could use link(s) presented in front of the message body - `PS 4` in
     the example above) in the same manner it is done for file comments now.
   * Multiple draft replies are published through general review feedback
     dialog (the same way as inline comments are published).
   * `Change Log` tab messages ordering is not impacted by this change.

## <a id="time-estimation"> Time Estimation

Backend: 2MW

UI: 1MW?
