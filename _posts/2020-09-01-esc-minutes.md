---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-09-01-esc-minutes.html
summary: "Minutes from the ESC meeting held on September 1st"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, September 1, 2020

### Attendees

Ben Rohlfs, Alice Kober-Sotzek, Patrick Hiesel, Luca Milanesio

### Place/Date/Duration

Online, September 1, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on October 6, 12:30 CEST.

## Minutes

### CI Results Tab and Composable Submit Rules

Ben and Patrick have met with all interested stakeholders and the
feedback loop is closing this week. Luca will take a final look at
both docs on Friday and approve if no major blockers surface until
then.

### Roadmap

We discussed if the roadmap should include generic items or rather
be very specific. Recent discussions have shown that if it's too
specfic adding items triggers discussions that already anticipate
discussions that would usually happen on design docs ("how" and
"why" not "what"). This seemingly discourages contributors from
adding items to the roadmap, which is not what we want.

The roadmap will therefore stay generic and contributors should feel
encouraged to add plans they have.

Items can be backed by tracking bugs if the owner wants that.

### Gerrit 3.3

We discussed plans for the 3.3 release and are targetting a release
in November with branches being cut in October. Luca will drive the
release. Google will check if there are internal resources to support
this effort, which was unclear at the time of the meeting.

Luca would also reach out other maintainers that would be willing to
help with the release.

### New maintainership

The nomination for a new maintainer is progressing well and will
conclude on Thursday.

### Gerrit Event Bus

Luca raised the priority of the redesign of the Gerrit events, which
is not in any of the next release plans. GerritForge is willing to
drive the effort, assuming that there is consensus in supporting the
initiative by Google and other companies contributing to Gerrit.

Alice, who initially raised the issue during the Hackathon 2019 in
Munich, is not currently planning to make progress, but will handover
her notes to Luca so that the effort can be carried over for making
it an official proposal.

Luca will follow up with a list of problems that GerritForge is having
with the current event system.
### Open designs

Besides the CI results tab and Composable Submit Rules, we discussed
deletion of groups. Alice volunteered to write a conclusion. The feature
should be implemented in a plugin so that the auditability of groups
remains intact in core.



