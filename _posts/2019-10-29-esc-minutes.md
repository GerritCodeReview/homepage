---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-10-29-esc-minutes.html
summary: "Minutes from the ESC meeting held on October 29th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, October 29, 2019

### Attendees

David Pursehouse, Luca Milanesio, Patrick Hiesel, Alice Kober-Sotzek

### Place/Date/Duration

Online, October 29, 12:30 - 13:20 CEST

### Next meeting

Per the biweekly schedule the next meeting should be held on November 12, but
we will skip it due to conflict with the Gerrit Hackathon.

The next meeting will be held on November 26, 12:30 CEST.

## Minutes

### Gerrit News Page

The next issue of the project news is due to be published on November 29.

There were no new items proposed during this meeting. Luca will write a
separate post about the live streaming of the upcoming user summit.

Members of the community may propose items by adding a change on the
[draft post](https://gerrit-review.googlesource.com/c/homepage/+/239186).

### Gerrit Roadmap

A separate meeting was held last week to discuss the contents of the
roadmap and how to manage it. Luca was not able to attend, so we went
over the discussion again today.

* The roadmap will be hosted on the project homepage on a dedicated
page. Alice will upload a change to add the initial version. The initial
version of the roadmap will then be announced in a news post and on the
project mailing list.

* We will not include version 3.1 in the roadmap because it is going
to be released in a couple of weeks. The initial roadmap will include
3.2 and "future releases".

* The roadmap is not a "wish list". This means that features on the
roadmap will only be those that have a commitment from an owner who
will drive it to be implemented for the corresponding release.

* We will have a standing agenda item to review the roadmap in the
biweekly ESC meeting, to ensure that features are still on track to be
completed in the expected release, and amend it if necessary. Updates to
the roadmap will be mentioned in the ESC meeting minutes.

* Community members may propose to add features to the roadmap either
by contacting the ESC or uploading a change to the homepage project.

We also briefly discussed the idea of having an "open roadmap"
like [Tuleap](https://blog.tuleap.org/open-roadmap-day-where-the-future-of-tuleap-is-shaped).
This is not something that we will do now, but will potentially
discuss again in future.

### Status and metrics for gerrit-review.googlesource.com

Patrick followed up on the discussion from the previous meeting
and reported that Google expects to work on this in 2020, however
there is no concrete plan yet.

### Hackathon and User Summit planning

We discussed scheduling of future user summits and agreed that we want
to have a clearer roadmap for them.

Luca asked if Google is willing to host a summit in the USA next year,
and if it would be feasible to collocate with the BazelCon. Patrick will
look into this.

We also dicussed whether or not we should continue with summits in Europe
given the low attendance of the recent one in Gothenburg. Luca suggested
that we could drop the European summit and rely on live streaming of the
USA summit. Patrick also pointed out that the Gothenburg summit and the
upcoming summit in Sunnyvale both have almost the same content, so maybe
it doesn't make sense to have two.

David mentioned that there may be a lot of users in China and APAC, based
on mails to the discussion list, so it might be worth considering a summit
and/or hackathon in Asia. We are unsure what level of interest there would
be, nor whether there is anyone who would be able/willing to host it.

### Gerrit narratives

Over the past months, Han-Wen has been trying to put together a narrative
for Gerrit at Google, i.e. a question & answer document that explains what
the team is doing, how they fit into the organization, and where they are
going.  Some of the questions and answers are not really about Google at
all, and are things that we should rather document in upstream Gerrit. Some
of it is part of the docs, but we should also have a pitch selling the
product and the community on our website, for example:

- What is the value of code review?
- What is the origin of Gerrit?
- Why is Gerrit open source?
- What is the Gerrit workflow?
- Why use Gerrit instead of other systems?
- etc

David pointed out that there have been several issues related to this raised
against the homepage. See
[issue 40011124](https://issues.gerritcodereview.com/issues/40011124),
[issue 40011463](https://issues.gerritcodereview.com/issues/40011463), and
[issue 40011464](https://issues.gerritcodereview.com/issues/40011464).

We agreed that we should improve the homepage to better "sell" Gerrit to
potential users. We will add this on the agenda for the next ESC and Community
Managers meeting.

### Review of open design proposals

There are several design proposals under review. We looked over the list and
confirmed that they all have someone from ESC involved, so no action is needed.

We decided that rejected designs should not be published on the designs
section of the homepage, but rather should be abandoned. The homepage already
has a link to query the abandoned designs on gerrit-review.

### Review of issues on the ESC component

We briefly went over the issues that have been added to the
[ESC component](https://issues.gerritcodereview.com/issues?q=status:open%20componentid:1371029)
on the issue tracker and did not find any that need urgent attention.
