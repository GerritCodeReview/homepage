---
title: "Gerrit ESC Meeting #4 Minutes"
tags: news
keywords: news
permalink: 2019-06-25-esc-minutes.html
summary: "Minutes from the ESC meeting held on June 25th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Fourth meeting of the engineering steering committee for the 2019 term

Today the fourth meeting of the Engineering Steering Committee took
place. This post contains a short summary of the topics that were
covered.

### Attendees

Luca Milanesio, David Pursehouse, Alice Kober-Sotzek, Ben Rohlfs

### Place/Date/Duration

Online, June 25, 12:30 - 13:15 CEST

### Next meeting

The next meeting will be held on July 19, 12:30 CEST.

## Minutes

* Security notification changes

  There is only one change still pending. The other issues in the tracker
  were closed.

* Gerrit User Summit in Gothenburg and Sunnyvale

  Alice and Edwin will propose summaries of their talks to the summit
  project. Luca will send a mail to prompt maintainers to sign up.

* CI Security

  Gerrit CI at GerritForge will move to read-only and X.509 strong authentication
  as proposed by Matthias Sohn and Thomas Draebing.

* JGit issues

  Recent JGit releases (from stable-5.1 and later) suffer from racy reads.  Matthias
  is aware of this and trying to fix it. Until then we can't upgrade the version of
  JGit used in Gerrit.

* Project News update

  There hasn't been any feedback on David's proposal to publish a regular news
  post on the project website. The draft for a post at the end of June is there,
  but has no content yet.

  David will try to get the ball rolling with a brief update on recent activity
  in the project. Ben suggested to add information about the recent Polymer 2
  work; Alice suggested mentioning recent work on performance improvement and
  the proposed design for external IDs.

* Polymer 2 Migration

  Polymer 2 is basically working and ready for testing. Ben will send out more
  information about this to the mailing list.

* New Gitiles release

  We need to make a new release of Gitiles to fix a recently introduced regression.
  The release with the regression is already included in Gerrit stable-3.0 and
  there have been several incompatible (with stable-3.0) changes submitted since
  then, so we will need to branch the Gitiles project if we want to also release a
  fixed version that can be used with Gerrit 3.0.x. David will take care of this.

* Frequency of Meetings

  It was agreed that the current bi-weekly meeting frequency is sufficient for
  now, and the next meeting will be in 2 weeks as usual. If we feel that we need
  a longer gap, i.e. during the summer holiday season, we will decide that on
  an ad-hoc basis.
