---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-06-02-esc-minutes.html
summary: "Minutes from the ESC meeting held on June 2nd"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, June 2, 2020

### Attendees

David Pursehouse, Ben Rohlfs, Alice Kober-Sotzek, Patrick Hiesel, Luca Milanesio

### Place/Date/Duration

Online, June 2, 09:30 - 10:30 CEST

### Next meeting

The next meeting will be held on July 7, 12:30 CEST.

## Minutes

### Project News

The latest news post was due to be published at the end of May. David forgot about
it and only published it this week. It hasn't been announced yet; we can still add
items to it if there are any.

Ben will follow up internally at Google to add information about recent frontend
changes.

### Gerrit v3.2 release

We had a brief retrospective about the recent 3.2 release. Everyone agreed that
it went well.

David mentioned that there were not as many blocking issues found. There were
a couple of issues found in the replication plugin, thanks to the e2e tests that
were run by the GerritForge Team.

Alice asked if the E2E tests could be run automatically for validation.
Even though it is posssible and not very expensive, it would add too much delay
to the CI validation as it takes around 15 mins to create a brand-new production
stack. However, it could be done on a regular basis on the stable branches
when a commit is merged. The feedback could be then posted back post-merge
with a new checker or label.

### EOL for 2.16

With the release of 3.2, our EOL policy means that 2.16 is now EOL. However in the
[release plan for 3.2](https://www.gerritcodereview.com/2020-04-22-gerrit-3.2-release-plan.html)
we mentioned that there will be exceptions for fixes related to the notedb migration.

We agreed that we need to specify a time limit on this.

TODO: more details on the discussion and what was agreed

### Follow-up on pending Library-Compliance votes

David asked the Google team to have another look at the pending library upgrades
that require the Library-Compliance vote.

* [Junit 4.13](https://gerrit-review.googlesource.com/c/gerrit/+/250096)

  Alice confirmed that this is being worked on internally at Google, but is not
  likely to be done within this quarter.

* [Caffeine](https://gerrit-review.googlesource.com/c/gerrit/+/251113)

  Youssef is working on this. Alice will follow up on the progress.

* [gson](https://gerrit-review.googlesource.com/c/gerrit/+/239953)

  Gal has looked into it, but it has turned out to be more difficult
  than expected.

David pointed out that none of the upgrades are critical. The Caffeine
upgrade will align with what is used in the latest version of ErrorProne,
and the JUnit upgrade is nice to have because it will allow us to remove
our custom implementation of `assertThrows`. There's nothing specific that
we need in gson; the upgrade is just to keep up-to-date with the latest
release.

### Review of open design documents

* [Auth backend](https://gerrit-review.googlesource.com/c/homepage/+/246449)

  No progress here. David will follow up with Jacek about when this can
  be resumed.

* [Deletion of groups](https://gerrit-review.googlesource.com/c/homepage/+/246928)

  David has updated the document to address feedback from Matthias and this
  is now ready for review again. Alice will have another look at it.

* [Subchecks](https://gerrit-review.googlesource.com/q/topic:subchecks+project:homepage)

  Alice hasn't had time to follow up yet.


### Review of issues on the ESC component

We reviewed the open issue. There were no issues that require immediate attention.
