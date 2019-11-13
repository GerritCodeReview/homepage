---
title: "Design Doc - Threaded Change Log - Use Cases"
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="primary"> Primary Use Cases

* user is able to follow multiple change discussions without a need
  to parse individual entries in `Change Log`.

## <a id="secondary"> Secondary Use Cases

* user replies could be extended with `unresolved` bit and eventually
  some rules could be added around it

## <a id="acceptance-criteria"> Acceptance Criteria

Single change discussion topic with multiple replies is not separated
by irrelevant `Change Log` entries (rebase, etc.).

## <a id="background"> Background

Change discussion (contributed with `Reply`) is currently hard to
follow especially when there are multiple replies/topics. Replies
are interrupted by messages to different topics, rebases, patch set
uploads, etc. It requires an extra effort to parse `Change Log`
entries in order to reason the current state of discussion. What is
more it has to be repeated every time when new reply gets added.

In the same time threads are part of file and inline comments...
