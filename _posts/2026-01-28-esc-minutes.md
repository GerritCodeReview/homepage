---
title: "Gerrit ESC Meeting Minutes, January 28th, 2026"
tags: esc
keywords: esc minutes
permalink: 2026-01-28-esc-minutes.html
summary: "Minutes from the ESC meeting held on January 28th, 2026"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

**Participants**: Edwin Kempin [EK], Luca Milanesio [LM], Saša Živkov [SZ]

**Next meeting**: February 25th, 2026

## Executive Summary

[LM] proposed a release plan for version 3.14 starting at the end of February, which was
later suggested to be delayed by a month to align with a meetup and allow Thomas and David
Ostrovski to finalize the migration to Bazel mode. [LM] also raised the change ID duplication
issue, noting it is increasing, particularly with AI-driven workflows; [EK] confirmed Google
also recently changed indexing for human users to be asynchronous to improve user experience,
and [SZ] and [EK] see the issue less frequently.
[LM], [SZ], and [EK] discussed the potential for calculating the change ID on the server and
concluded that although the duplication issue is concerning, it is not a current priority
over other issues like concurrency problems with the ref-table.

## Release Plan for 3.14

* **Draft Plan:** [LM] drafted the release plan for version 3.14, initially proposing a
  start date at the end of February.

* **Bazel Migration:** It was decided to check with Matias regarding the status of the migration
  to `bzlmod` (managed by David Ostrovski and Thomas), as this could serve as a major feature for
  the release.

## Technical Issue: Change ID Duplication

### The Problem

Luca raised an [issue](https://issues.gerritcodereview.com/issues/313935024) where Gerrit
generates the Change ID on the client side.
This causes duplication problems when indexing is set to asynchronous or has high latency.

A similar duplication problem may happen with the
[change number duplication issue](https://issues.gerritcodereview.com/issues/391394129) where
the same change number is assigned to two changes on different projects.

* **Frequency:** [SZ] and [EK] noted they see this issue less frequently. However, [EK]
  mentioned that Google recently switched to asynchronous indexing for human users
  performing git pushes to improve the User Experience (UX). All the web-ui
  interactions caused already asynchronous indexing.

* **AI Workflow Impact:** [LM] observed an increase in clients reporting this issue, particularly
  those adopting AI-driven workflows which significantly increase push traffic.

### Mitigation & Solutions

[SZ] stated that a fix cannot be prioritized immediately as it likely requires updates to the global
ref-db in a multi-master scenario. However, there are other issues to be solved on v3.14,
such as [ref-table concurrency](https://issues.gerritcodereview.com/issues/460019541),
are currently higher priority.

* **Risk Assessment:** [LM] agreed that while the issue is concerning regarding AI adoption, the
  probability of occurrence remains relatively low, in less than 0.1% of the cases.

* **Long-term solution:** Solving this fundamentally would require a design document, potentially moving
  Change ID calculation from the client to the server, used in the ref-name of the change instead of
  the change number.

* **Current Mitigation:** The preferred solution (implemented by Google) is to configure
  indexing as **asynchronous for human users** (to reduce push times) but keep it
  **synchronous for agents/bots** to prevent duplication.

## Timeline Adjustment & Meetup

* **Schedule Shift:** Luca suggested delaying the 3.14 release start by one month, to allow a proper
  fix of the ref-table implementation and finalise the Bazel migration.

* **Sunnyvale Meetup:** The new timeline aligns with the
  [upcoming meetup in Sunnyvale](https://www.meetup.com/gerritmeets/events/312898799)
  on the 19th of February. This allows for a preview of version 3.14 (currently in master) while
  accommodating the migration work.
