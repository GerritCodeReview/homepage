---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-05-07-esc-minutes.html
summary: "Minutes from the ESC meeting held on May 5th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, May 5, 2020

### Attendees

David Pursehouse, Ben Rohlfs, Alice Kober-Sotzek, Patrick Hiesel, Luca Milanesio

### Place/Date/Duration

Online, May 5, 12:30 - 13:30 CEST

The ESC meetings will take place once a month from now on.

### Next meeting

The next meeting will be held on June 2, 09:30 CEST.

## Minutes

### Additional lint checks in CI

With regards to the support of the latest version of error prone, David Ostrovsky made some
work and progressed the activity. Currently waiting for the Bazel Team to review and accept
his [GitHub PR #11271](https://github.com/bazelbuild/bazel/pull/11271).


### Reviewers promotion as Gerrit core plugin

Sven Selberg is taking some of the work to adress the issues raised on the reviewers plugin
to make it suitable for promotion.
From a popularity perspective, the reviewers plugin is already the most used plugin
of its type, amongst the general shortlist of the top 100 plugins for Gerrit.

### Gerrit v3.2 release

There is a continuous progress on the features in development for v3.2.

The [multi-master scalability of the replication plugin](https://www.gerritcodereview.com/design-docs/scaling-multi-master-replication.html)
is close to completion. There is a concern on the test coverage and real-life production
use of the functionality. It will be flagged as experimental because of lack of production use
and feedback.

The support for global ref-db in the high-availability plugin has been agreed with Marco Miller:
the implementation will be done on the high-availability plugin master branch and, if finished on time,
released at the same time as Gerrit v3.2 but flagged as experimental.

Ben Rohlfs agreed to start validating PolyGerrit in v3.2 and master using Chrome 80. Existing stable
releases will be continued to be validated against the older version of Chrome, because of the issues
found with WCT tests on Chrome 80. A specific note will be included in the release notes.

### Next joint meeting ESC and CM

Marco Miller has agreed to organize a remote joint meeting between the ESC and CM, because of the
cancellation of the Spring 2020 hackathon due to COVID-19.

### Introduction of Quality Gates in the contribution process

Luca Milanesio raised the issue that some changes merged in the past have created issues in released
version of Gerrit. We do not currently document or enforce a quality gate for reviewing and approving
changes.

Ben Rohlfs pointed out that we have already a quality criteria to nominate maintainers and we assume they
are good enough for the job of reviewing and approving changes. A further complication in the process
is not needed.

There is consensus on Ben's position: the current contribution process will remain as it is today.

### Review of open design documents

* [Instance ID / name propagation in events](https://gerrit-review.googlesource.com/c/homepage/+/257972)

  The design has been analyzed by Patrick Hiesel and provided a positive feedback
  to move forward, as long as the instance-id is optional and not required / populated for single-master
  setups. There are no objections to the decision: the design is approved.


### Review of issues on the ESC component

* [Issue 40009013 - A better way to prevent spam, or report spammers](https://issues.gerritcodereview.com/issues/40009013)

  A few months ago, gerrit-review introduced a group for adding accounts that have restricted permissions.
  David Pursehouse raised the issue that having restricted permissions is not enough as the spammers
  would still be able to login and operate on gerrit-review.

  Patrick Hiesel proposed to disable the spammers' accounts with a REST-API
  authorized to the Gerrit maintainers and Ben Rohlfs proposed to add button on the Gerrit
  UI should a suitable API be available in the backend.

* [Issue 40011333 - Schedule of the ESC/CM joint meeting](https://issues.gerritcodereview.com/issues/40011333)

  It was supposed to happen during the next forthcoming Gerrit Hackathon in
  April/May 2020, now cancelled because of Covid-19. A follow-up discussion
  needs to happen with the CMs to understand how this can be
  coordinated remotely with all the different time-zones to cover.

There were no other issues that have updates or require attention.


