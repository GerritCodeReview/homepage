---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2025-01-29-esc-minutes.html
summary: "Minutes from the ESC meeting held on January 29, 2025"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meetings, January 29, 2025

**Participants**: Edwin Kempin [EK], Luca Milanesio [LM], Saša Zivkov [SZ]

**Next meeting**: Feburary 26, 2025

### Monthly Catch-up Meetings

The team agreed to reinstate the monthly catch-up meetings, which will now take  
place on the last Wednesday of every month at 2 PM CET. This schedule aims to  
ensure regular alignment and discussions on key topics, with the flexibility
of reducing the meetings' duration in case the agenda is minimal.

### Welcoming Edwin Back to ESC

A warm welcome to Edwin [EK] to the ESC who will communicate this update,
and him leaving the role of Community Manager.

[EK] replaces Chris Poucet and Patrick Hiesel's roles as Google members
of the ESC.

### How to better prevent Google build failures from Community Contributions

[LM] raised the point on how to improve the stability of Community Contributions,
particularly concerning the update of features not used by Google, including
the Lucene and SSH protocol support.

Ensuring that [Gerrit-CI](https://gerrit-ci.googlesource.com) builds do not
break Google’s build remains a  challenge, as the current build still
includes Lucene and SSH. [LM] will investigate if it is possible to define
an extra build target and verification that would try to identify possible
breakages or build failures when Lucene and SSH are completely taken out
of the picture.

For reference, the issue of Lucene document metrics was discussed in connection  
with [Alvaro’s Lucene documents metrics](https://gerrit-review.googlesource.com/c/gerrit/+/446721)
which introduced an implicit dependency on the use of Lucene as Gerrit search
and indexing backend.

### Gerrit 2025 roadmap at the GerritMeets on the 19th of February 2025

The upcoming [GerritMeets event on the 19th of February](https://www.meetup.com/gerritmeets/events/305718795/)
was discussed, with a focus on securing volunteers to present the roadmap
for 2025 and beyond. There is an opportunity to showcase key plans for the
future of Gerrit, and [SZ] will  check internally whether anything related
to [k8s-gerrit](https://gerrit.googlesource.com/k8s-gerrit/) could be  
presented at the event.

### Use of Git refs to store the diff-cache instead of the H2 backend

[SZ] proposed the use of a diff cache directly in the repository instead
of keeping it in the H2 persistence backend. That would allow to easily
distribute and replicate that cache using the standard Git replication
and also making sure that it scales up seamlessly with the repository.

Both [EK] and [LM] agreed that this could be a beneficial approach, with [LM]  
emphasizing that it would also help address the issue of excessively large H2  
tables, which have become a bottleneck. While there is no firm commitment yet,  
[SZ] suggested that this change could potentially be included in Gerrit v3.12.

### Review of Open Design Proposals

The team also reviewed the [Dynamic Submit-Type feature request](https://gerrit.googlesource.com/homepage/+/48534d3302850cfbdde194dfb3c8c79b2013d521/pages/design-docs/dynamic-submit-type/index.md),
which was triggered by discussions surrounding the removal of Prolog rules. 
Given the potential impact of this change, it was agreed that [SZ]
would review the design document and provide feedback at the next meeting.
