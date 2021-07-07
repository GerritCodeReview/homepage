---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-07-07-esc-minutes.html
summary: "Minutes from the ESC meeting held on July 7, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---



## Engineering Steering Committee Meeting, July 7, 2021

### Attendees

Han-Wen Nienhuys, Luca Milanesio, Saša Živkov, Albert Cui

### Place/Date/Duration

Online, July 7, 17:30 - 18:30 CET

### Next meeting

September 15, 2021 - 17:30 - 18:30 CET

## Minutes

### Next steps for case-insensitive username matching

The design is currently blocked on the decision as to whether Gerrit can
completely drop support for case-sensitive usernames. This change is already on
master and would require an offline conversion of any duplicate accounts.

The ESC discussed the
[results](https://docs.google.com/presentation/d/11Ivu6xtYZBYTU5e5y_lc6tni3nm9fNIUbX2VRTyTMbE/edit#slide=id.ge209b6f75c_0_971)
from the recently ran Gerrit Community Survey which had a question about how
identity providers handle usernames. The results showed that 64% of providers
use case-insensitive usernames and over 19% use case-sensitive names. However,
the question was not very useful for determining whether Gerrit can deprecate
support for case-sensitive names as the survey didn't ask whether or not that
would be an issue for administrators.

The consensus was to send out a few follow up questions to the community in
order to more explicitly gage whether we can drop support for case-sensitive
usernames.

GerritForge will look into contributing a change for online migration to enable
zero-downtime upgrades in Gerrit v3.5.

### Roadmap Updates

The ESC discussed discrepancies between the published Gerrit
[roadmap](https://www.gerritcodereview.com/roadmap.html) and the planning cycles
of our individual organizations.

Going forward, Google will update the roadmap with respect to its quarterly
planning cycle.

GerritForge uses both an annual planning process as well as a free-form
Kanban-based process where anyone can contribute ideas to an non-public board.
However, GerritForge works in the open so any active work can be seen in the
Gerrit issue tracker and on reviews. The near term priorities are improving
replication, working mostly in JGit. As the Gerrit roadmap only covers Gerrit
specific items, we discussed the need to find a place to surface these planned
changes.