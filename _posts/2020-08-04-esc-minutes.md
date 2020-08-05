---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-08-04-esc-minutes.html
summary: "Minutes from the ESC meeting held on August 4"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, August 4, 2020

### Attendees

Alice Kober-Sotzek, Ben Rohlfs, Luca Milanesio, Patrick Hiesel

### Place/Date/Duration

Online, August 4, 12:30 - 13:00 CEST

### Next meeting

The next meeting will be held on September 1, 12:30 CEST.

## Minutes

### Gerrit outdated screenshots

Luca has been working in updating the Gerrit screenshots on the homepage.
Further work will also include the updates on the Gerrit documentation, so that
the Gerrit project would not look outdated anymore.

As a follow-up, the screenshots layout in the homepage should be redesigned
as they are today too small and difficult to read.

### Review comments flagging

Luca presented the proposal of adding the ability to **flag** comments in a code-review,
coming from a discussion with the CMs. The new feature would allow to filter out comments that
are out of scope or inappropriate.

The Go project is big enough to have similar needs and it seems they do
not need the flagging feature.

The general consensus is to **NOT have the flagging** feature in Gerrit, as it won't be practical
because of:

1. Inability to have a properly staffed team for reading and flagging comments
2. The new feature is more likely to introduce more inter-personal conflicts rather than resolving them

### Issues on GerritHub.io

Currently, all issues reported on GerritHub.io are ending up to Ben's backlog, which causes some
overload and incorrect assignment to the PolyGerrit Team.

Luca proposed to create a proper template that would assign the issues to the GerritForge Team
and will have the host label set to gerrithub.io, similarly to what happens today with Googlesource.com.
The proposal is accepted.

### Project News

The Google team proposed to help David Pursehouse in brainstorming items for the Gerrit Projects News page.
Patrick checked internally and Youssef has agreed to take this on from now.

### Interactive vs robot accounts in Gerrit

The Google team has presented the results of the discussions with Qualcomm on the proposal of having
a new "robot" flag in the account settings, with the counter-proposal of defining a global capability
that could be assigned to groups.

Gerrit already has the __Non-Interactive Users__ group that could be potentially reused for this purpose,
but there are performance implications because the group resolution could be potentially slow.

Patrick will think this through once more and follow up via email.

### Review of open design documents

No progress.

### Review of issues on the ESC component

No new issues.
