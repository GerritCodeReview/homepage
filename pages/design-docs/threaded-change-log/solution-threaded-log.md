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

### Phase 1: easy win - embrace new fields in backend and UI

1. Add `inReplyTo` and `unresolved` fields all the way down to
[ChangeMessage](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/entities/ChangeMessage.java)
entity including
[ReviewInput](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/extensions/api/changes/ReviewInput.java)
and
[ReviewResult](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/extensions/api/changes/ReviewResult.java).

2. Modify UI so that:
  * Reviewer can mark review feedback as one that needs to be resolved add
    possibility to display unresolved messages only (similar to code comments).
  * When `Change Log` message `REPLY` button is used original message id
    is provided to submitted entity (there is no longer a need to copy over
    original message body to reply dialog, yet it should be displayed for
    reference)
  * Messages are displayed linearly as they are now however new switch will
    be introduced to display them in groups. Still no threads but messages
    related with `inReplyTo` will be grouped and displayed again linearly.

    In the following example `inReplyTo` relation takes precedence over patch
    set upload (time `n+3`). For multiple replies to the same message the
    following criteria are assumed: direct reply (`id: 4`) is grouped with
    message that it replies to, for more replies to the same message (`id: 3`)
    grouping is based on time (`n+2` > `n+1`) however it has lower precedence
    than direct relation (`id: 3` is older than `id: 4` however `id: 4` is a
    reply to `id: 2` which is older than `id: 3` hence they stay grouped IOW
    `parent->child` relation is stronger).

    At current state there is no plan to highlight group. It was introduced
    in the following schema to better illustrate the concept. However, It
    may be considered later (it is not a subject of this document).

  ```
  +------------+
  | Change Log |
  +----+-------+
        |  +----------------------------------------+
        |  |                                  group |
        |  | +-----------------------------+        |
        +----+ id: 1, t: n                 |        |
        |  | +-----------------------------+        |
        |  |                                        |
        |  | +-----------------------------+        |
        +----+ id: 2, inReplyTo: 1, t: n+1 |        |
        |  | +-----------------------------+        |
        |  |                                        |
        |  | +-----------------------------+        |
        +----+ id: 4, inReplyTo: 2, t: n+4 |        |
        |  | +-----------------------------+        |
        |  |                                        |
        |  | +-----------------------------+        |
        +----+ id: 3, inReplyTo: 1, t: n+2 |        |
        |  | +-----------------------------+        |
        |  |                                        |
        |  +----------------------------------------+
        |
        |    +-----------------------------+
        +----+ uploaded PS#2, t: n+3       |
        |    +-----------------------------+
        |
        |    ...
       ...
  ```

### Phase 2: multiple responses and threads

1. Extend backend to handle draft reviews that can be eventually published
  altogether with single `REPLY` button action.

2. Replace linear groups of messages with threads, displayed as trees, that
  can have corresponding branches expanded or folded down.

## <a id="time-estimation"> Time Estimation

`Phase 1`: 1MW
`Phase 2`: 2MW
