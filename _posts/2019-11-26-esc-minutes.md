---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-11-26-esc-minutes.html
summary: "Minutes from the ESC meeting held on November 26th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, November 26, 2019

### Attendees

David Pursehouse, Luca Milanesio, Alice Kober-Sotzek, Ben Rohlfs

### Place/Date/Duration

Online, November 26, 12:30 - 13:20 CEST

### Next meeting

The next meeting will be held on December 10, 12:30 CEST.

## Minutes

### Gerrit News Page

The next issue of the project news is due to be published at the end
of this week, November 29.

There were no new items proposed during this meeting. David has already
[uploaded a change](https://gerrit-review.googlesource.com/c/homepage/+/246812)
adding items about the new project roadmap, the recent hackathon
and user summit, and the release of 3.1.0. The update includes links to
some changes that are not published yet; if those are not completed before
the end of the week, the post will be amended to remove the links, so that
it can be published on time.

After publishing this issue of the news, David will create a new
draft for the next one which is tentatively planned for the end of
January 2020.

### Gerrit Roadmap

Alice has uploaded the
[initial version of the project roadmap](https://gerrit-review.googlesource.com/c/homepage/+/246712)
for review. Since this is based on the roadmap that we have already
agreed on during previous ESC meetings, we don't need to do a detailed
review of the contents. We will review and fix nits, and publish it
within the next day. Any further amendments can then be done in follow-up
changes.

### Review of open design documents

We briefly went over the
[open design documents](https://gerrit-review.googlesource.com/q/project:homepage+status:open+dir:pages/design-docs/).

* [Attention Set](https://gerrit-review.googlesource.com/c/homepage/+/245069):

  Ben has uploaded a new version which includes many adjustments based on
  feedback received so far, both in the review comments and face-to-face
  during the recent hackathon. He will reach out to those that had concerns
  to make sure they have been addressed.

* [Threaded change log](https://gerrit-review.googlesource.com/c/homepage/+/245316):

  Ben has reviewed the initial design and has asked the author to proceed
  with adding the implementation details. We will revisit this again later.

* [Pluggable authentication backend](https://gerrit-review.googlesource.com/c/homepage/+/246449):

  Edwin has reserved time to review the design within the next week. We will
  follow up later.

* [Global ref database](https://gerrit-review.googlesource.com/c/homepage/+/237980):

  It's not clear if this really belongs in Gerrit or should be part of JGit.
  Luca suggested to abandon the proposal and instead start a discussion with
  the JGit committers.

* [Subchecks](https://gerrit-review.googlesource.com/c/homepage/+/235693):

  Alice is handling this; no action needed right now.

* [Permission tests](https://gerrit-review.googlesource.com/c/homepage/+/235929):

  Alice will follow up with Han-Wen and Gal to check the status of this.

### Hackathon and User Summit retrospective

Everyone agreed that the hackathon and summit were very well organized.

Luca received feedback from no-shows that the timing was not convenient, being
in the week before the Thanksgiving holiday in the USA. Also having the summit
on a weekend may mean it attracts enthusiasts, but many people might not want
to attend a "work event" on the weekend. We will consider scheduling the next
summit a bit earlier in the year, around October, and during the week instead
of the weekend.

We also discussed how we can better advertise the summit to get a wider range
of attendees. So far it seems that the audience mostly consists of developers
and admins, but not end users.

### Review of issues on the ESC component

We briefly went over the issues that have been added to the
[ESC component](https://issues.gerritcodereview.com/issues?q=status:open%20componentid:1371029)
on the issue tracker.

[Issue 40011458 - Clarify future of change identifiers](https://issues.gerritcodereview.com/issues/40011458)
was due to be discussed face-to-face during the user summit, but we're not
sure if that happened. Ben has asked Patrick to confirm.
