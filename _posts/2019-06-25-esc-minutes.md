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

* Upcoming Gerrit User Summits in Gothenburg and Sunnyvale

  The next Gerrit User Summits dates and schedule are now published. Google,
  GerritForge, and CollabNet are planning to send representatives to one or
  both events. More talks details are going to be published in the next few
  days, and slots for new talks are still available on the Sunnyvale event.

* Issues with recent JGit releases

  The recent releases of JGit, starting from 5.1.8, are experiencing
  [problems](https://bugs.eclipse.org/bugs/show_bug.cgi?id=548188)
  related to the racy reads of the Git repository files, which impacts the
  normal Gerrit operations. The JGit and Gerrit maintainers are aware of them
  and are working hard to get them identified and fixed. In the meantime,
  Gerrit will stay on the latest stable JGit versions which are not impacted
  by the racy read problem.

* Removal of Gerrit v2.13 and associated plugins from the Gerrit CI

  Gerrit v2.13 has not been supported by the community for a few months and it
  is now going also be removed from the Gerrit CI. That means that all existing
  builds artifacts are going to be [archived](https://archive-ci.gerritforge.com/)
  and Gerrit CI can drop the support for Gerrit v2.13 and associated plugin builds.
  This would allow to remove the support for the Buck-based builds and save a lot
  of space in the Docker build images.

* Gerrit CI security

  The current security on Gerrit CI is going to be upgraded to use X.509 Client
  certificates instead of the current GitHub OAuth authentication. The existing
  Jenkins instance will remain read-only for public unauthenticated access whilst
  the Gerrit maintainers will be provided with a client authentication
  certificate to install on their Web Browsers.

* Gerrit News Page

  There hasn't been any feedback on David's proposal to publish a regular news
  post on the project website. The draft for a post at the end of June is there,
  but has no content yet.

  David will try to get the ball rolling with a brief update on recent activity
  in the project.

* Polymer 2 Migration

  Polymer 2 support is currently available on gerrit-review.googlesource.com and
  accessible by adding the `?p2` URL parameter.

  Any Polymer 2 specific issues can be reported on the Gerrit Issue Tracker using
  the `Polymer2` hotlist.

  People started adopting Polymer 2 and reporting some initial feedback and fixes.
  Everyone is invited to try it out and report any issue. Similarly, plugins need
  to be checked for Polymer 2 compatibility and fixed if needed.

* New Gitiles release

  The current version of Gitiles needs to be fixed and a stable branch created to
  address one recent regression. See
  [change 227998](https://gerrit-review.googlesource.com/c/gitiles/+/227998).

  More generally the Gitiles project, that has historically had linear development
  on the master branch, needs to be branched and released more consistently with
  the Gerrit semantic versioning.

* Frequency of Meetings

  It was agreed that the current bi-weekly meeting frequency is sufficient for
  now, and the next meeting will be in 2 weeks as usual. If we feel that we need
  a longer gap, i.e. during the summer holiday season, we will decide that on
  an ad-hoc basis.
