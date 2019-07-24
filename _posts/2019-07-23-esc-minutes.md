---
title: "Gerrit ESC Meeting #4 Minutes"
tags: news
keywords: news
permalink: 2019-07-23-esc-minutes.html
summary: "Minutes from the ESC meeting held on July 23rd"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, July 23 2019

### Attendees

David Pursehouse, Alice Kober-Sotzek, Patrick Hiesel

### Place/Date/Duration

Online, July 23, 12:30 - 13:15 CEST

### Next meeting

The next meeting will be held on August 6, 12:30 CEST.

## Minutes

* Gerrit News Page

  There are still no contributions for the next edition of the project
  news, which is due to be published at the end of this month.

* REST API for retrieving Git trees

  The [design document](https://gerrit-review.googlesource.com/c/homepage/+/231894) was
  reviewed and the general feeling is that the feature is being proposed as a
  helper to an external implementation of signing GPG commits in the UI. We feel
  it would be better to look into how Gerrit can natively support GPG commit
  signing.

  Alice will post feedback on the design document.

* Redesign of external IDs

  Discussion is still ongoing in Patrick's
  [proposed redesign of external IDs](https://gerrit-review.googlesource.com/c/homepage/+/228398).

  Patrick has also proposed an
  [alternative solution](https://gerrit-review.googlesource.com/c/gerrit/+/231934)
  that doesn't require a full redesign of the external IDs. The idea is to try this
  solution and see if it fixes the issues that were being addressed by the redesign.

  If the alternative solution does not fix the issues, we will go back to the redesign
  and make a committee decision on whether to proceed.

* Pluggable authentication backend

  Support for a pluggable authentication backend has been on the table since
  2012 but has stalled several times.

  A [design](https://docs.google.com/document/d/17LSVzzqoRhpPAnd_fGm3p0_nuPDUA22Kz6Mvx4x3ous/edit)
  was proposed by Dariusz Luksza (CollabNet) and received several comments
  during the hackathon hosted by Axis in April last year, but then stalled
  again.

  Edwin has previously mentioned that Google would be interested in such a
  feature, and Patrick confirmed that this is still the case.

  CollabNet has a working implementation based on Gerrit 2.15, but it is not
  in a suitable condition to be pushed for review. It is probably better to
  start again from scratch either on master or stable-3.0.

  Patrick will check internally at Google whether they will be able to provide
  a team member to work on this in the 'mentor' role, with the assumption that
  the implementation will be done by CollabNet.

* Joint meeting with community managers

  A joint meeting between the ESC and community managers has been scheduled
  in September.
