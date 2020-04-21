---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-04-21-esc-minutes.html
summary: "Minutes from the ESC meeting held on April 21st"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, April 21, 2020

### Attendees

David Pursehouse, Ben Rohlfs, Alice Kober-Sotzek, Patrick Hiesel, Luca Milanesio

### Place/Date/Duration

Online, April 21, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on May 5, 12:30 CEST.

## Minutes

### Gerrit News Page

Some new features and improvements can be included in the next forthcoming Gerrit project news:
- Cherry-pick of topics
- Gerrit display of account names
- Performance improvements thanks to the groups' external cache

As usual, we invite the community to propose any items that they think would
be interesting.

### Additional lint checks in CI

Bazel v3 doesn't include the new version of errorprone, which would
allow enabling more static analysis to the build and validation process of
incoming Gerrit changes. David Pursehouse will continue the research with David
Ostrovsky for understanding how use a more recent version of errorprone and
include in our Bazel build.

### ElasticSearch Support

ElasticSearch has been flagged experimental for many releases. Marco Miller
(Community Manager) has agreed to prepare and circulate a survey for
understanding the current use of ElasticSearch and its desired version to be
supported (https://bugs.chromium.org/p/gerrit/issues/detail?id=11938). Once the
survey would be completed, the ESC can insert the ElasticSearch support in the
Gerrit roadmap, with details of which version to consider and where the official
readiness for production lies in the current or future Gerrit releases.

### Reviewers promotion as Gerrit core plugin

The most recent statistics of the reviewers plugin statistics have been
published on Google docs
(https://docs.google.com/spreadsheets/d/1nhKWXz4Ar32P3iJfJO0tH9uhScxIYt1Ybnk33K4yUu0/edit?usp=sharing).
The contributions have only considered the non-trivial commits and do not want
to define a qualitative analysis of the contributions made by different people
(e.g. Dave Borowitz were just adaptations, reformatting and refactoring rather
than the design of new functionalities). By looking at the fit for the reviewers
plugin with the core Gerrit use-cases, it looks the functionality makes sense
and suits the needs of automatically adding and suggesting reviewers. The
current implementation and user-journeys need some refinement (e.g. The
automatic addition of reviewers need to take into consideration the special case
of WIP and Private changes). From the look&feel perspective, there are minor
issues with padding and the style can be improved. However, the issues are not a
blocker and can be fixed easily afterwards. The code looks small and properly
covered by integration tests. There are some Thread.sleep() as a means of
synchronization in the tests, therefore suboptimal but it is not a blocker and
can be possibly fixed (Issue raised as
https://bugs.chromium.org/p/gerrit/issues/detail?id=12610). Overall there are no
blockers in making the reviewers a Gerrit core plugin. However, the final
decision is postponed to when the issues raised will be resolved.

### Gerrit v3.2 release

It has been discussed and finalized the release plan of Gerrit v3.2. A separate
news item will provide all the details and dates.

### Review of open design documents

* [Instance ID / name propagation in events](https://gerrit-review.googlesource.com/c/homepage/+/257972)

  More feedback is needed for the instance id proposal. The proposed change is
  very small, (almost a one-liner) so, if the design would get approval, it
  could be tentatively included in Gerrit v3.2.

There aren't major follow-ups or news on the other design proposals.

### Review of the Roadmap

With Gerrit v3.2 approaching some of the items currently on the roadmap are most
liketly to be postponed to v3.3:

- Group deletion and auth backend
- Performance improvements on H2 storage for persistent caches
- Performance improvements for large mono-repos
- Migration to Polymer 3 (typescript and HTML imports removal)

Once the Gerrit v3.2-RC0 will be cut, the updated roadmap will be published to
the Gerrit home page.

### Review of issues on the ESC component

* [Issue 11637 - Process to remove a core plugin](http://bugs.chromium.org/p/gerrit/issues/detail?id=11637)

  The issue is currently assigned to the ESC, however a follow-up with the CMs
  is needed to understand the possible involvement that we can have.

* [Issue 11632 - Schedule of the ESC/CM joint meeting](http://bugs.chromium.org/p/gerrit/issues/detail?id=11632)

  It was supposed to happen during the next forthcoming Gerrit Hackathon in
  April/May 2020, now cancelled because of Covid-19. A follow-up discussion
  needs to happen with the CMs to understand how can this be
  coordinated remotely with all the different time-zones to cover.

* [Issue 11534: Checks plugin as a core plugin](http://bugs.chromium.org/p/gerrit/issues/detail?id=11534)

  The discussion has not started yet, the focus will be possibly postponed to
  Gerrit v3.3.

There were no other issues that have updates or require attention.


