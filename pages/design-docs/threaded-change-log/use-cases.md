---
title: "Design Doc - Threaded Change Log - Use Cases"
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="primary"> Primary Use Cases

* user is able to follow multiple change discussions without a need
  to parse individual entries in `Change Log`; The idea is to add
  reference between the original message and one that is a reply to it.

## <a id="secondary"> Secondary Use Cases

* user replies (when one selects `REPLY` in `Change Log` single message
  scope) could be extended with `unresolved` bit and eventually
  some rules could be added around it.
  This will apply only to the messages that are issued through the
  change `REPLY` button e.g.: *reviewer* finds that given change has
  unit tests missing and adds that information as message to the review
  score marking an extra *unresolved* bit. Depending on the case change
  owner either uploads new patch set with unit tests (also replies
  `DONE` which marks the thread as *resolved*) or replies to the
  reviewer that it will be done as a follow-up change eventually
  adding (again with message `REPLY` button) response with the change
  number that addresses the issue in question (again marking the thread
  as *resolved*). To sum it up it will be the reviewer's discretion
  to mark given review message as the one that needs a resolution.

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
