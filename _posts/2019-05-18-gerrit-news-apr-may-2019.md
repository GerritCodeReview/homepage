---
title: Gerrit Project News April-May 2019
tags: news
keywords: news
permalink: 2019-05-18-gerrit-news-apr-may-2019.html
summary: "Gerrit project news from April and May 2019."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Project Governance

Edwin Kempin (Google) led an effort to define a clear governance model for the
project, with the following goals:

1. Have clear project governance rules, including a steering committee
   for decision making.
2. Establish a new contribution process for large/complex features that
   requires to write a design doc first.
3. Offer mentorships to make contributions easier and faster, and raise
   the quality of new features.
4. Appoint a community manager, who focuses on the health of the
   Gerrit community and constantly improves community processes.

Edwin proposed several [documentation changes](https://gerrit-review.googlesource.com/q/hashtag:proposal-for-better-collaboration)
to define the new governance model. During the hackathon in Munich the proposed
changes were discussed face-to-face among the attendees, and other community members
via remote dial-in.

Notes from the discussion are available
[here](https://docs.google.com/document/d/1XPRpJo-0rwg0D5ZBiO9l00_Nqkem5Htc6vk_iddYfZ0/edit).

The proposed process was unanimously accepted by all the maintainers and
contributors present at the hackathon, despite concerns from Qualcomm,
and the changes were submitted. For futher details see
[Dave Borowitz's comment on change #223472](https://gerrit-review.googlesource.com/c/gerrit/+/223472/4#message-36f23fee51487933d33caf677764bf348a165ee6)
along with the review history of that change.

The new documentation is published on gerrit-review.googlesource.com
[here](https://gerrit-review.googlesource.com/Documentation/dev-community.html),
and work is ongoing to update the project homepage with related information.

## Engineering Steering Committee (ESC)

Following acceptance of the new project governance model, Han-Wen Nienhuys
announced that the Google-appointed members of the ESC will be Alice Kober-Sotzek,
Ben Rohlfs, and Patrick Hiesel.

A call was then made to nominate non-Google members. David Ostrovsky nominated
Luca Milanesio (GerritForge) and David Pursehouse (CollabNet). There were no
other nominations, so the nominations from David Ostrovksy were accepted.

## Community Managers

Han-Wen Nienhuys announced that Edwin Kempin will be the Google-appointed
community manager, and a call was made to nominate a non-Google member.

Saša Živkov (SAP) nominated Matthias Sohn (SAP), and Marco Miller (Ericsson)
also expressed an interest in taking the role. After discussion with Edwin,
it was decided that they would form a trio of community managers.

## Hackathon in Munich

From 13 to 17 May,
[around 20 core developers and maintainers](https://twitter.com/DevilJackj/status/1129287522297810944)
from Google, GerritForge, CollabNet, SAP, Ericsson and Axis gathered
for a hackathon at the Google office in Munich.

The major achievements during the hackathon were:

* Gerrit version 3.0.0 was finalized and released. See
  [this GerritForge blog post](https://gitenterprise.me/2019/05/20/gerrit-v3-0-is-here/)
  for details.

* The new community governance process was finalized.

* The new checks plugin was integrated with GerritForge CI. See the
  [mailing list announcement here](https://groups.google.com/d/msg/repo-discuss/rHIjzIlPzqY/zAGOaG6MAwAJ).

Changes created during the hackathon can be found on gerrit-review with
the
[muc-2019 hashtag](https://gerrit-review.googlesource.com/q/hashtag:muc-2019). A more
detailed report of the hackathon will come later.

## Dave Borowitz leaves the project

Shortly before the Munich hackathon Dave Borowitz
[announced](https://groups.google.com/forum/#!topic/repo-discuss/ySP84Q0DHsw)
that he will leave the project to move on to another opportunity within Google.

## Community Calendar

Edwin Kempin created a
[public calendar](https://www.google.com/calendar/render?cid=google.com_ubb1pla6ij785oqbjr61h4vdis@group.calendar.google.com)
which will contain community events like user summits and hackathons.
In future we will likely also create calendar entries for upcoming releases etc.
