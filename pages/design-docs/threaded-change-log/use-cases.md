---
title: "Design Doc - Threaded Change Log - Use Cases"
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="definitions"> Definitions

* *change message*: extra information (text message) that is given
  by reviewer as a part of his review feedback (when change's `REPLY`
  button is pressed); It may be encouraging or just polite (and as such
  doesn't require any further steps from the owner) but very often
  it is a question, request for an explanation or for the follow up work.
  Later is often followed by the owner's reply contributed by the message's
  scoped `REPLY` button. May also be a beginning of the conversation with
  broader audience (replies from more reviewers).

## <a id="primary"> Primary Use Cases

* user is able to follow multiple change discussions without a need
  to parse individual entries in `Change Log`

## <a id="secondary"> Secondary Use Cases

* owner/reviewer is able to answer multiple `change messages` (question
  or concern) from reviewers in a single round (similar way that `DRAFT`
  comments are added to the code)
* both reviewer's feedback (`change message`) and owner's replies
  (when one selects `REPLY` in `Change Log` single message scope) could
  be extended with `unresolved` bit and eventually more rules could be
  added around it. However it will be in reviewers discretion to mark
  a change message as one that requires resolution (to be discussed if
  it that should be by default or not).

  Example:
  *reviewer* finds that given change has unit tests missing and adds that
  information as message to the review score marking an extra *unresolved* bit.
  Depending on the case change owner either uploads new patch set with unit
  tests (also replies `DONE` which marks the thread as *resolved*) or replies
  to the reviewer that it will be done as a follow-up change eventually
  adding (again with message `REPLY` button) response with the change
  number that addresses the issue in question (again marking the thread
  as *resolved*).

  General purpose `change log` messages like new new PS creation or robot
  comments are not a subject of resolution.

## <a id="acceptance-criteria"> Acceptance Criteria

Single change discussion topic with multiple replies is not separated
by irrelevant `Change Log` entries (rebase, etc.).

## <a id="background"> Background

Change discussion (contributed with `REPLY`) is currently hard to
follow especially when there are multiple replies/topics. Replies
are interrupted by messages to different topics, rebases, patch set
uploads, etc. It requires an extra effort to parse `Change Log`
entries in order to reason the current state of discussion. What is
more it has to be repeated every time when new reply gets added.

In the same time threads are part of file and inline comments...
