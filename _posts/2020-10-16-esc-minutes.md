---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-10-16-esc-minutes.html
summary: "Minutes from the ESC meeting held on October 13th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, October 13, 2020

### Attendees

Ben Rohlfs, Saša Zivkov, Patrick Hiesel, Luca Milanesio

### Place/Date/Duration

Online, October 13, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on November 3, 11:00 CET.

## Minutes

### ESC Issues Review

General review of the [open issues](https://bugs.chromium.org/p/gerrit/issues/list?q=component%3AESC%20&can=2)
assigned to the ESC.

Saša raised the [improvement](https://gerrit-review.googlesource.com/c/homepage/+/284297)
of the Gerrit Code Review support page by making some links more prevalent:

- The repo-discuss mailing list
- The issue tracker

### GerritForge Activities for Gerrit v3.3

Luca provided an overview of what GerritForge is focusing on for
Gerrit v3.3:

1. Fix of Gerrit pluggable persistent caches and introduction of
   the cache-chroniclemap high-performance non-blocking implementation.

2. Adoption of the aws-gerrit infrastructure project for testing
   Gerrit v3.3 end-to-end, with a real production-like setup, including
   also the Gatling-Gerrit test framework for load testing and client
   metrics collection.

3. Extension of the high-availability plugin to allow active-active
   concurrent read-write access to all nodes.

4. Testing of Gerrit with large mono-repos, using the aws-gerrit and
   Gatling tests for implementing a data-driven approach to improving
   performance and stability.

### Status of Gerrit v3.3 release plan

Luca reported the status of the release plan execution, which is on track
so far. The first RC0 was partially blocked by a JGit issue, which has been
now resolved in RC1 by Matthias.

Ben mentioned the intention to make the attention-set feature enabled by
default very soon, before the release of v3.3.

### Review of Open Design Proposals

The open designs do not need further involvement at the moment from the ESC.
Luca mentioned the intention to take over from Alice the management
of the Gerrit events redesign initiative. Patrick will be the counterpart
from Google.

### Roadmap

Nothing new to introduce in the current roadmap. Once Gerrit v3.3 will
be released; the roadmap can get refreshed with what's next for the
v3.4 release in Spring 2021.

### ESC Handovers

Alice is moving to a different project inside Google, handing over her ESC
seat to Han-Wen. David is stepping down because of personal reasons; Saša has
been elected to take his place, based on a recent poll amongst the
non-Google maintainers.
