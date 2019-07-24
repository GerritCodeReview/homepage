---
title: "Gerrit ESC Meeting Minutes"
tags: news
keywords: news
permalink: 2019-06-11-esc-minutes.html
summary: "Minutes from the ESC meeting held on June 11th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Third meeting of the engineering steering committee for the 2019 term

Today the third meeting of the Engineering Steering Committee took
place. This post contains a short summary of the topics that were
covered.

### Attendees

Luca Milanesio, David Pursehouse, Alice Kober-Sotzek, Ben Rohlfs, Patrick Hiesel

### Place/Date/Duration

Munich, June 11, 12:30 - 13:15 CEST

### Next meeting

The next meeting will be held on June 25, 12:30 CEST.

## Minutes

* Gerrit Plugins

  Luca's proposed documentation of
  [the current process that is used for creating new plugins](https://gerrit-review.googlesource.com/c/gerrit/+/226659)
  was accepted and submitted. We should now begin looking into
  what we want to change in that process, i.e. how do we decide that a plugin
  is 'unmaintained' and deprecate it?

  Work was started on collecting a list of existing plugins, their status, and usage.
  This is still ongoing.

  Plugins are not consistently versioned. We should propose a process to
  improve this.

* Security notification changes

  Some of the changes related to this were cleaned up and submitted, and will be
  included in the next maintenance releases. There are still some changes and
  feature requests in progress, but they need more feedback.

* End of life for 2.14

  The announcement was reviewed by maintainers, and then sent to the project
  mailing list.

* Gerrit User Summits

  The schedule for the upcoming summit in Gothenburg (August) will be announced
  after it has been reviewed by speakers, and there will be a call for proposals
  for the user summit in Sunnyvale (November).

* JGit

  We would like to switch to building JGit from source in the Gerrit tree, rather
  than consuming prebuilt artifacts. Work was started on this some time ago by
  Shawn Pearce; we should revive that and make it work with Bazel. We also need
  to consider how to work around the fact that JGit source code currently doesn't
  comply with the same Error Prone checks as Gerrit.

* Java 8 and large heap

  We are aware that Gerrit/JGit with Java 8 can run into memory issues in specific
  setups and think that upgrading to Java 11 could help. Even though we can't upgrade
  immediately, it's one of the items we intend to put on our roadmap.

* Maintainer Update

  Wyatt agreed to step down as maintainer, but will keep in touch with the project.

  Viktar and Becky remain maintainers. Viktar is still involved in plugin reviews, and
  will attend the user summit in Gothenburg. Becky would like to remain in touch with
  the project and will look for ways to contribute in future.

* Quota backend changes

  Patrick will follow up on the quota backend changes that were proposed during the
  Munich hackathon.

* Git Protocol V2

  Work is ongoing to be able to enable protocol V2 on master. It depends on the new
  permission-aware ref database, which in turn depends on a new release of JGit.

* New releases

  Version 2.15.14 will be released this week; 2.16.9 and 3.0.1 will follow later,
  but no specific date is decided yet.
