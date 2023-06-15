---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-09-17-esc-minutes.html
summary: "Minutes from the ESC meeting held on September 17th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, September 17, 2019

### Attendees

David Pursehouse, Alice Kober-Sotzek, Luca Milanesio, Ben Rohlfs

### Place/Date/Duration

Online, September 17, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on October 1, 12:30 CEST.

## Minutes

### Gerrit News Page

The next issue of the project news is due to be published on September 27th.

David has uploaded a [draft](https://gerrit-review.googlesource.com/c/homepage/+/237600)
with brief items about the user summit in Gothenburg, plans for releasing
Gerrit 3.1, and the [new code of conduct](https://gerrit-review.googlesource.com/c/homepage/+/236152).
It's not necessary to include a lot of information since we already have
separate posts which are linked. We expect that there will also be a separate
post announcing the code of conduct once it's submitted.

Further items can be added later. The post will not appear on the homepage
until September 27th and only after it gets moved to the `_posts` folder.

### Plans for support of Bazel 1.0

Work has been ongoing, driven mainly by David Ostrovsky, to make sure that core
Gerrit and the plugins are still buildable with recent Bazel versions on stable-2.14
and later. The plan is to continue this activity on stable-2.14 and stable-2.15
only until Bazel 1.0 is released, and then we will only make Bazel specific changes
on stable-2.16 and later.

### Review of open design documents and clarification of the design-driven process

We briefly discussed, but did not review in detail, the design documents
for [sub-checks](https://gerrit-review.googlesource.com/c/homepage/+/235693)
and [permission tests](https://gerrit-review.googlesource.com/c/homepage/+/235929).

Alice pointed out that design documents are not mandatory for plugins, but in
this case it was written to make collaboration easier.

Alice will follow up with Gal Paikin, the author of the permission tests design,
about that review.

We discussed whether the ESC should always be involved in the review of
design documents. The conclusion was that it's not always necessary; it depends
on the proposed feature and whether there are concerns/questions raised in the
review that require escalation. However, it was proposed that at least one
member of the ESC should be involved in the review to ensure that it progresses
and does not get stale.

It was also suggested that we should encourage people to send an email to the
project mailing list when a new design is uploaded, however this should not be
a mandatory step. We should also be careful to keep the discussion of the
design in the review on Gerrit rather than in the mail thread.

Ben will propose updates to the design process documentation. This is tracked
in [issue 11533](https://bugs.chromium.org/p/gerrit/issues/detail?id=11533)

### Consolidation of mock framework for tests

We currently use easymock in core tests, and provide mockito for plugins. It was
proposed in [issue 5057](https://bugs.chromium.org/p/gerrit/issues/detail?id=5057)
to consolidate to a single mock framework.

Everyone agreed that it would be better to switch to mockito. David has already
looked into this, and will continue with it.

We will aim to make the transition from easymock to mockito in Gerrit 3.1.

### Support for Java 11

David Ostrovsky has been driving the effort to support Java 11.

We will define Java 11 support as experimental and release Gerrit 3.1 with
Java 8.

We will continue with the effort to support Java 11, and will build on CI
with both Java 8 and Java 11, to help with verification of Java 11.

We will consider dropping Java 8 in a later release when Gerrit is
stable on Java 11 and there is wider adoption of Java 11 in the community.

### Support for the checks plugin in Gerrit 3.0

In [issue 11489](https://bugs.chromium.org/p/gerrit/issues/detail?id=11489) it
was reported that the checks plugin does not build against Gerrit 3.0.

According to comments from Edwin on that issue, and from Alice in the meeting,
to build the plugin on 3.0 will require core changes to be backported from
master. This will take some effort, and we would rather not do it. We will
instead aim to get the plugin working with the upcoming 3.1 release. Alice will
create issues in monorail to track remaining features that are needed on
the plugin.

We also discussed whether or not the checks plugin should be promoted to a
core plugin with the 3.1 release.
See [issue 11534](https://bugs.chromium.org/p/gerrit/issues/detail?id=11534).

### Support for git protocol v2

There is a series of changes pending to re-add support for git protocol v2,
but it has stalled. See [change 227901](https://gerrit-review.googlesource.com/c/gerrit/+/227901)
and its ancestors.

We would like to get v2 support into Gerrit 3.1, but the changes need to be
reviewed by Googlers. Alice will follow up on this.

The series of changes also includes support for building JGit from source,
which we discussed in the previous meeting.

### Global ref database

[Change 237177](https://gerrit-review.googlesource.com/c/gerrit/+/237177) adds
support for a global ref database that can be used by plugins. During the
review Marco Miller requested that the change be moved to master and a design
document be written.

Luca will follow up with Marcin Czech, the change author, and bring it to the
next ESC meeting.
See [issue 11465](https://bugs.chromium.org/p/gerrit/issues/detail?id=11465).

### Requests from retrospective

Two issues were raised against ESC during the project retrospective at the
recent user summit.

* [Issue 11437](https://bugs.chromium.org/p/gerrit/issues/detail?id=11437):
Track ESC work items in the issue tracker

  We agreed that it's not clear how to contact ESC members, and we should
  improve this.

  Generally the ESC work items are small and are tracked in the minutes,
  so we're not sure if it's useful to track them in the issue tracker,
  however we have created an
  [ESC component](https://issues.gerritcodereview.com/issues?q=status:open%20componentid:1371029)
  that can be used to raise issues to ESC members' attention. When this
  component is added to an issue all ESC members are automatically CC'd.

  We will also create a mailing list. This will align us with the way
  that the community managers are working. We will update the community
  documentation accordingly.

  Progress on this can be followed in
  [issue 11437](https://bugs.chromium.org/p/gerrit/issues/detail?id=11437).

* [Issue 11436](https://bugs.chromium.org/p/gerrit/issues/detail?id=11436):
Create an open roadmap for Gerrit 3.1 and beyond.

  We agree that a roadmap is needed, and we already identified some features
  that should be on the roadmap for 3.1, but we ran out of time to discuss it
  in detail during this meeting.

  We will come back to this in the next meeting, with the aim of presenting
  a roadmap during the upcoming user summit in November.
