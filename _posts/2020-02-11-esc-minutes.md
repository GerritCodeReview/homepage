---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-02-11-esc-minutes.html
summary: "Minutes from the ESC meeting held on February 11th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, February 11, 2020

### Attendees

David Pursehouse, Luca Milanesio, Alice Kober-Sotzek, Patrick Hiesel, Ben Rohlfs

### Place/Date/Duration

Online, February 11, 12:45 - 13:30 CEST

### Next meeting

The next meeting will be held on February 25, 12:30 CEST.

## Minutes

### Gerrit News Page

Alice's summary of the new "preview/apply fix" feature did not make it
into the last issue, and will instead go into the next one which is due
to be published at the end of March.

No other news items were disussed during this meeting. As usual, we invite
the community to propose any items that they think would be interesting.

### Gerrit Roadmap

We reviewed the current status of the roadmap, and decided to remove some
items:

- Replacing the guava cache with caffeine was already implemented and
backported to 2.16.x, so no longer needs to be in the roadmap.

- The plugin working group is not a core gerrit feature and thus doesn't
need to be included in the roadmap.

### Non-core plugin releases

We followed up on this issue that had been discussed in a previous meeting.

Luca summarized that the problem is that there is no clearly defined
repository where plugin artifacts can be downloaded. Regular build artifacts
are available from CI but they are not immutable and change frequently.

Luca proposed to introduce a process whereby the plugin owner can apply a
tag on the plugin project, and CI will then generate a release which is
deployed to a Google Cloud Bucket. The exact details of this process
still need to be discussed.

### Concerns about polygerrit build reproducibility

Recently a dependency of the polygerrit build disappeared, which caused
build failures. See [issue 40011914](https://issues.gerritcodereview.com/issues/40011914)
for details.

The polygerrit build has recently switched from Bower to NPM which should
prevent this kind of problem from happening in future, but we need to also
make sure that older releases are still buildable.

### Direct migration from 2.14 to 2.16

David brought attention to [issue 40010119](https://issues.gerritcodereview.com/issues/40010119).
Direct migration from 2.14 to 2.16 does not work, and this has been raised
by users on the mailing list. So far the solution provided is only to do the
migration with an intermediate step on 2.15.

We did not have time to discuss it in detail, but David asked the ESC members
to have a look at it and think about whether this can be solved to allow a
direct migration.

### Review of open design documents

We ran out of time and did not review open designs.

### Review of issues on the ESC component

There were no issues requiring action from the ESC.
