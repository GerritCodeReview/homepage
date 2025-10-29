---
title: "Gerrit ESC Meeting Minutes, September 23, 2025"
tags: esc
keywords: esc minutes
permalink: 2025-09-23-esc-minutes.html
summary: "Minutes from the ESC meeting held on September 23, 2025"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

**Participants**: Edwin Kempin [EK], Luca Milanesio [LM], Saša Živkov [SZ]

**Next meeting**: October 29, 2025

## Executive Summary

[LM] presented the
[Gerrit 3.13 release plan](https://www.gerritcodereview.com/2025-09-17-gerrit-3.13-release-plan.html)
and discussed the risks of an NPM-like supply chain attack, the Gerrit User Summit,
and the transactionality of Lucene. [EK] announced the open-sourcing of the
[Google MCP server for Gerrit](https://gerrit.googlesource.com/gerrit-mcp-server/+/refs/heads/master)
and addressed JJ client-side support for Gerrit.
[SZ] suggested implementing a durable event log for Lucene and rethinking the "transactionality" name for future developments.

## Release Plan for Gerrit 3.13

[LM] presented the
[release plan for Gerrit 3.13]((https://www.gerritcodereview.com/2025-09-17-gerrit-3.13-release-plan.html)),
proposing an RC0 release on September 29th, followed by five RCs until November 3rd,
with a release freeze and target release date of November 10th.
[SZ] noted that SAP does not depend on these releases; also Google typically works on master.
Nevertheless, most of the community works on stable releases, therefore cutting regular stable
branches and release them it's a general good practice for the rest of the Gerrit
community.

## Gerrit User Summit and Community Engagement

[LM] provided an update on the
[Gerrit User Summit 2025](https://gerrit.googlesource.com/summit/2025/+/refs/heads/master/index.md),
highlighting increased participation and new speakers like Patrick from GitLab and Scott Chacon,
co-founder of GitHub.
The summit will also include remote presenters and live streaming on
[GerritForge's YouTube Channel](https://youtube.com/gerritforgetv),
with talks covering topics like GitButler and JJ integration, and case studies from Qualcomm and NVIDIA.

## NPM Supply Chain Attack and Gerrit Release Process

[LM] raised concerns about the
[NPM supply chain attack](https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem)
and the learnings for improving the security of the Gerrit's release process.
[LM] suggested to move towards more automated release processes, similar to Google's
internal CI system, to minimize security vulnerabilities and assuring complete
repeatibility of the releases from the source code.

Lastly, [LM] highlighted the need to use separate signing keys and short-lived Maven authentication
tokens for publishing the release, so that any potential leak of credentials won't impact the
safety of the published artifacts.

## Transactionality of Lucene

[LM] discussed the issues of transactionality of the Gerrit indexes stored in Lucene
(see [Issue 450577969](https://issues.gerritcodereview.com/issues/450577969) and
[Issue 440360427](https://issues.gerritcodereview.com/issues/440360427)).
While the problem is rare, it has been exacerbated by the introduction of AI agents
creating and abandoning changes, leading to increased concurrency.

[SZ] and [EK] suggested implementing a durable event log or queue for indexing to
ensure eventual consistency and recoverability from failures, an approach Google
already uses for their internal indexing system.

[SZ] took the initiative to start drafting a design document on the rewrite of
the indexing subsystem in Gerrit, something that SAP is already planning to do
with the split of the reindexing tasks to a separate service in their deployment.

## MCP Server Open Sourcing

[EK] announced that a team at Google received approval to
[open source the MCP server](https://gerrit.googlesource.com/gerrit-mcp-server/+/refs/heads/master)
and will present during the GerritMeet on the
[19th of November at Google HQ in Munich](https://www.meetup.com/gerritmeets/events/310709185/),
with the code expected to be published by then.
[EK] clarified that the Google team is not taking ownership of its maintenance, making it a
community-driven effort. [LM] stated that [GerritForge](https://www.gerritforge.com)
is willing to contribute to the project but clarified that support will follow Gerrit's
[support process](https://www.gerritcodereview.com/support.html#general-support).

## JJ Client-Side Support for Gerrit

[EK] mentioned that JJ is working on supporting Gerrit change IDs natively, which has now been
[merged and presented at the Gerrit User Summit 2025](https://youtu.be/UwIJvXMs3_0).
[LM] highlighted that a guide has been approved and merged into the JJ project to
simplify integration.
[LM] also noted that GerritForge plans to fully transition to JJ for client development
and sees strong synergies with the JJ community.

## Gerrit Project Roadmap

[LM] stated that the [project roadmap](https://www.gerritcodereview.com/roadmap.html)
will be updated to reflect the v3.13 release and future plans.
They anticipated that major game-changers for Gerrit in 2026 will be the
integration of JJ and the MCP server, along with work being done at SAP.
[SZ] suggested rethinking the "transactionality" in Gerrit and potentially transition
to a micro-service based deployment for a future v4.0 release.
