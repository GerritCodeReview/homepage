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

Both `inReplyTo` and `unresolved` have to be added to
[ChangeMessage](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/entities/ChangeMessage.java)
entity and its store/read flow.
UI will be responsible to present `Change Log` messages so that one
could choose between threaded (proposed) and linear (as it is now)
views. Both views could be additionally narrowed with `Only unresolved`
option.

### <a id="scalability"> Scalability

Change detail payload will be increased for all messages in terms of
`unresolved` bit and optionally for `inReplyTo` (the latter only when used).

## <a id="alternatives-considered"> Alternatives Considered

Building message threads by analysis of change message content. That seems
to be substantial computational effort (to be performed on client side)
and is not guaranteed to deliver stable/valid results.

## <a id="pros-and-cons"> Pros and Cons

* clear indication of messages relation that can be effectively used
  in `Change Log` UI to present data to user

## <a id="implementation-plan"> Implementation Plan

1. Add `inReplyTo` and `unresolved` fields all the way down to
  [ChangeMessage](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/entities/ChangeMessage.java)
  entity including
  [ReviewInput](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/extensions/api/changes/ReviewInput.java)
  and
  [ReviewResult](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/extensions/api/changes/ReviewResult.java).

  Extend corresponding endpoints to accept draft and publish message
  reply/replies.

2. Modify UI so that:
  * Reviewer can mark review feedback as one that needs to be resolved.
    By default current state is preserved and feedback doesn't require any
    resolution. Feedback with `unresolved` flag added (regardless of its state)
    is additionally displayed in thread on `Comment Threads` tab.
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

Backend: 1MW

UI: 1MW
