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

TBD

## <a id="time-estimation"> Time Estimation

TBD
