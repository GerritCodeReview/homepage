---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-02-25-esc-minutes.html
summary: "Minutes from the ESC meeting held on February 25th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, February 25, 2020

### Attendees

David Pursehouse, Luca Milanesio, Alice Kober-Sotzek, Patrick Hiesel

### Place/Date/Duration

Online, February 25, 12:30 - 13:00 CEST

### Next meeting

The next meeting will be held on March 10, 12:30 CEST.

## Minutes

### Gerrit News Page

Alice's summary of the new "preview/apply fix" feature is still pending
for the next issue which is due to be published at the end of March.

No other news items were disussed during this meeting. As usual, we invite
the community to propose any items that they think would be interesting.

### Gerrit Roadmap

Alice has published an update to the roadmap per the decisions made in
the previous meeting.

### Hackathon/Summit Planning

There is no news about the schedule for a hackathon/summit. Luca has followed
up with Matthias about the possibility for SAP to host, but there is no
decision yet.

### Review of open design documents

* [Threaded feedback in the change log](https://gerrit-review.googlesource.com/c/homepage/+/245316)

  This is waiting for Jacek to respond to review comments. David will remind him.

* [Auth backend extension point](https://gerrit-review.googlesource.com/c/homepage/+/246449)

  The first part (linked above) seems to be OK, apart from a couple of pending
  minor comments from Edwin and broken links pointed out by David.

  David will remind Jacek to follow up.

* [Deletion of groups](https://gerrit-review.googlesource.com/c/homepage/+/246928)

  CollabNet is OK with the proposed design, and now the only thing remaining is
  to include the recent discussions from the review into the actual document.

  David will take care of that, and begin the development, later. No further
  action is needed from ESC until the document has been updated.

* [Subchecks](https://gerrit-review.googlesource.com/c/homepage/+/235693)

  Alice will follow up with James.

### Review of issues on the ESC component

* [Issue 40011458 - future of change Ids](https://issues.gerritcodereview.com/issues/40011458)

  We agreed that the other forms of change identifier should still be supported,
  and we should therefore cancel the deprecation that was announced with 2.16.

  David and Patrick will work on this. First there needs to be a change to revert
  the deprecation, and then a follow-up change to add more context information about
  the different identifiers and when/why they are useful.
