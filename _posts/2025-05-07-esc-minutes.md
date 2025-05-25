---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2025-05-07-esc-minutes.html
summary: "Minutes from the ESC meeting held on May 7, 2025"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

# Engineering Steering Committee Meetings, May 7, 2025

**Participants**: Edwin Kempin [EK], Luca Milanesio [LM], Saša Živkov [SZ]

**Next meeting**: June 25, 2025

## Executive Summary

[LM], [EK], and [SZ] reviewed and approved the Jujutsu
design document, planning its integration into Gerrit next quarter; Martin von Zweigbergk
will present Jujutsu at the GerritMeets on May 21st, with [LM] and [EK]'s
participation depending on the time. 

The Gerrit User Summit in Paris, hosted by the Open Infrastructure Foundation in October,
will include a Gerrit code review track, Zuul and Kubernetes tracks, and potentially a
hackathon (pending budget approval), with a Munich location as an alternative if the
Paris hackathon is not feasible.

## Jujutsu Design Document Review

[LM], [EK], and [SZ] reviewed the
Jujutsu design document.  [EK] agreed the document was good and ready for approval,
with a score of +2. They also planned to integrate Jujutsu into Gerrit in the next quarter.

Martin von Zweigbergk will present Jujutsu at the next GerritMeets on May 21st.
[LM] hopes that they can join remotely to explain integration plans with Gerrit.
[EK]'s availability depends on the time. Martin von Zweigbergk will be present in person
as he lives in Mountain View CA.

## Gerrit user Summit 2025 in Paris

The Open Infrastructure Foundation will provide free hosting for the Gerrit User Summit 2025 in Paris.
The summit will include a Gerrit Code Review track and will take place over three days in October.

[LM] mentioned the cost of tickets being low and the location being preferable to a US summit
due to travel concerns.  [SZ] suggested the possibility of a hackathon in conjunction with the summit,
pending travel budget approval.

The summit will also feature tracks on Zuul and Kubernetes. The Open Infrastructure Foundation's interest
stems from their use of Gerrit in their collaboration platform [OpenDev](https://opendev.net).

## Next Gerrit Code Review Hackathon

[SZ] proposed a hackathon in Paris, with [EK] expressing potential interest in attending.
However, it depends on travel budget and approval for presentation content.
If travel budget is limited, a Munich location is preferred by [EK].

## Reindexer Task in Kubernetes

[LM] and [SZ] discussed a reindexer task in Kubernetes.  The task’s goal is to recreate
the index without updating caches, which improves performance.

A concern was raised about the current behavior of updating caches, which negatively impacts memory usage. 
[LM] agreed the task should only update the index and not the caches, and acknowledged that the
online reindexing causes similar cache bloat issues.

The use of read-only caches to address the issue and the preferred approach versus alternative methods.
The primary concern is memory leaks due to a large H2 database.
The common agreement is to proceed with the change, acknowledging the potential for further improvements.






