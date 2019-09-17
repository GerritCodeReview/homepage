---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-05-28-esc-minutes.html
summary: "Minutes from the ESC meeting held on May 28th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Second meeting of the engineering steering committee for the 2019 term

Today the second meeting of the Engineering Steering Committee took
place. This post contains a short summary of the topics that were
covered.

### Attendees

Luca Milanesio, David Pursehouse, Alice Kober-Sotzek, Ben Rohlfs, Patrick Hiesel

### Place/Date/Duration

Munich, May 28, 12:30 - 13:15 CEST

### Next meeting

The next meeting will be held on June 11, 12:30 CEST.

## Minutes

* New Plugins

  We would like to establish a process for creating new plugins on
  gerrit-review such that we can review the functionality, reduce overlap
  between plugins and keep track of who is maintaining the plugin.

* Existing Plugins

  We would like to know more about the current state of all the plugins
  that are hosted on gerrit-review:

  * How many users do they have?
  * Who owns and maintains them?

  Keeping old plugins buildable costs time. We are tentatively looking into
  four buckets for plugins:

  * core
  * maintained
  * unmaintained
  * obsolete.

  we would like to come up with criteria for being in a bucket and
  transitioning to another.

* Security-related email notifications

  We are generally open to proposed changes to add more email notifications
  for security relevant events, but we are also concerned about potential
  email spam, and we would like to audit extension points to be used, if
  possible.

* Homepage

  We will consolidate the list of people (ESC, community managers, maintainers)
  on one page. We will keep using Jekyll and will integrate it into checks and
  CI such that the homepage is generated automatically after every submit.

* Bug tracker

  Potentially changing to a different bug tracker other than Monorail has low
  priority. We will continue to collect issues, though, and will do some
  experimenting on the side. We may want to do some cleanup at the Gothenburg
  Hackathon to reduce the high number of old bugs.

* Release 2.14

  It has reached end of life. Will send out an announcement with details soon.

* Roadmap

  We will be starting to discuss and brainstorm at the next ESC meeting.
