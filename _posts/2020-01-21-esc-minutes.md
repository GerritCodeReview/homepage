---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-01-21-esc-minutes.html
summary: "Minutes from the ESC meeting held on January 21st"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, January 21, 2020

### Attendees

David Pursehouse, Luca Milanesio, Alice Kober-Sotzek, Patrick Hiesel, Ben Rohlfs

### Place/Date/Duration

Online, January 21, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on February 11, 12:30 CEST.

## Minutes

### Gerrit News Page

The next issue of the project news is due to be published at the end
of this month. There are already a couple of items in the draft, and
some more were proposed in this meeting:

- Update on the status of the checks plugin and Zuul integration (Luca)
- Summary of the new "preview/apply fix" feature (Alice)
- Patrick's presentation at the Git Merge conference (Patrick)

Patrick will send a reminder to the Gerrit team at Google to check if
anyone else has anything to add.

### Planning for next bugfix releases

There have been several fixes merged on the stable branches since the
last releases, so it's time to make new ones. David will take care of
putting together the release notes, and he and Luca will make the releases
during the last week of January.

### Planning for Spring hackathon and/or user summit

David suggested that while we don't need to fix any plans right now, we should
at least start thinking about if/when/where we will have a hackathon and/or
user summit in Spring. We should make sure to plan far enough in advance that
people are able to make travel arrangements.

Alice remembered that it had been mentioned that SAP might be able to host
us. Luca will follow up on this with Matthias.

### Escalation of LDAP permission saving issue

Ben mentioned that [issue 40010299](https://issues.gerritcodereview.com/issues/40010299)
was escalated to the mailing list and no progress seems to have been made.

Luca will try to reproduce the issue using the Docker environment.

### Conclusion of the Attention Set design proposal

We reviewed Luca's [conclusion document](https://gerrit-review.googlesource.com/c/homepage/+/249547)
and unanimously agreed that Ben's solution should be accepted.

### Review of open design documents

* [Deletion of groups](https://gerrit-review.googlesource.com/c/homepage/+/246928):

  CollabNet agrees to move the implementation to a plugin rather than core.

  Alice had already answered David's questions but he had overlooked it. Now the
  major concern is resolved, but the information from Alice's answer needs to be
  incorporated into the design document along with a couple of other minor nits.

  We will review it again in the next meeting.

* [Threaded change log](https://gerrit-review.googlesource.com/c/homepage/+/245316):

  Patrick has reviewed the design and is happy with it. Alice would like to
  also review it, so we will keep it open until the next meeting.

* [Permission tests](https://gerrit-review.googlesource.com/c/homepage/+/235929):

  Patrick will follow up with Gal to check on the status.

### Use Swagger for the Gerrit REST API

Patrick has done some reading around this topic but there is no conclusion
yet.

### Git Merge 2020

Patrick will be [presenting](https://git-merge.com/#notedb-58-an-adventure-where-git-is-your-database)
at the Git Merge 2020 conference in Los Angeles.

### Review of issues on the ESC component

There were no issues requiring action from the ESC.

### Gerrit Roadmap

We did not review the roadmap in this meeting due to running out of time.
We have bumped this to the first item on the agenda for the next meeting.
