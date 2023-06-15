---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-12-10-esc-minutes.html
summary: "Minutes from the ESC meeting held on December 10th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, December 10, 2019

### Attendees

David Pursehouse, Luca Milanesio, Alice Kober-Sotzek, Patrick Hiesel

### Place/Date/Duration

Online, December 10, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on January 21, 12:30 CEST.

## Minutes

### Gerrit News Page

The next issue of the project news is due to be published at the end
of January next year. No news items were proposed during the meeting.

### Planning for next bugfix releases

There are no pending fixes for 2.16.14 and 3.0.5 and the release notes
are already almost up-to-date. For 3.1.1 there is still one change pending,
and it's expected to be submitted soon.

David will take care of releasing 3.0.5 and 3.1.1; Luca will release 2.16.14.

### Review of open design documents

* [Threaded change log](https://gerrit-review.googlesource.com/c/homepage/+/245316):

  Patrick has requested some updates related to replying to multiple
  messages. David will follow up with Jacek, the author.

* [Pluggable authentication backend](https://gerrit-review.googlesource.com/c/homepage/+/246449):

  Edwin reviewed the documents and provided feedback. Jacek has addressed
  the feedback and now we're waiting for a follow-up review.

### Initial results from Hackathon and User Summit survey

Luca gave a brief overview of the results so far from the Hackathon
and User Summit Survey.  Feedback is good, but there is still room
for improvement. The problems raised were pretty well aligned with
what we had already identified in the previous ESC meeting:

- Too many admins and not enough users
- Cramped room
- Prefer to meet during the week rather than the weekend
- Too close to the Thanksgiving holiday period

Also, the proposal to have a workshop for regular users received positive feedback.

### Use Swagger for the Gerrit REST API

[Issue 11401](https://bugs.chromium.org/p/gerrit/issues/detail?id=11401) suggests
to use Swagger, which will allow generate REST API documentation and
stubs for clients.

We decided not to make a decision on this right now, but look into it
some more on open standards like [OpenAPI](https://www.openapis.org/) (Swagger is
just one implementation of the standard) and come up with a plan.

### Gerrit Roadmap

The initial version of the roadmap was published and is now available
[on the homepage](https://www.gerritcodereview.com/roadmap.html).

During the
[review](https://gerrit-review.googlesource.com/c/homepage/+/246712) there
were suggestions about how to keep the roadmap up to date, i.e. with links
to changes, design docs, issues, etc.

We discussed this and decided to continue with the current format. It will
be a lot of effort to keep it up to date in such detail.

### Critical User Journeys

The UX team at Google wants to define Critical User Journeys (CUJs) - a
written down status quo of how users use Gerrit and the important workflows.

We didn't discuss this in detail, but put an action point for everyone to
think about it and provide feedback for the next meeting.

### Review of issues on the ESC component

We briefly went over the issues that have been added to the
[ESC component](https://issues.gerritcodereview.com/issues?q=status:open%20componentid:1371029)
on the issue tracker.

- [Issue 12000 - Publishing plugin artifacts to Maven Central](https://bugs.chromium.org/p/gerrit/issues/detail?id=12000):

  This was requested for the checks plugin.

  Using separate group Ids is probably not feasible due the bureaucratic
  overhead required to manage them via Sonatype.

  Using the existing group Ids is also not feasible because granting permission
  would also allow people to publish core Gerrit artifacts.

  Maybe it will be enough to use the maven repository on the Google Storage
  Bucket?

  Luca will look into this some more.

- [Issue 11772 - Clarify future of change identifiers](https://bugs.chromium.org/p/gerrit/issues/detail?id=11772):

  Patrick confirmed that this did not get discussed during the user summit.
