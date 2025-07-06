---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2025-06-25-esc-minutes.html
summary: "Minutes from the ESC meeting held on June 25, 2025"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

# Engineering Steering Committee Meetings, June 25, 2025

**Participants**: Edwin Kempin [EK], Luca Milanesio [LM], Saša Živkov [SZ]

**Next meeting**: July 30, 2025

## Executive Summary

[LM] provided a status update of the issues with packed-refs and the status of
reftable testing, including pending issues with C Git. For the forthcoming
Gerrit User Summit 2025, there is interest in AI features for Gerrit Review
which will be reported by [LM] in his proposed talk.

## Issues with packed-refs

[SZ] detailed the current status of the `packed-refs` issues and their mitigation
strategy for the backdraft file issue, which involves a script to repair everything
using a global-refdb maintaining backups.

[LM] mentioned that their team has observed other strange issues related to concurrency
between deletion of refs and packing of the refs, including reverted refs during repacking
and the return of removed refs. A bug in the locking system for deleting refs was identified
and fixed by Dani.

[LM] also highlighted a POSIX compatibility issues with some specific NFS implementation,
where data written to a file and closed was not immediately visible to another node after
performing the open of the file after the closing on the other node.

## `reftable` test status

[LM] provided a positive update on extensive testing with `reftable`, noting that a problem
involving an unexpected closed file descriptor has been identified and a straightforward
fix is expected. They suggested adding [SZ] as a reviewer, as a stable reftable could be
a much better alternative to `packed-refs` due to scalability issues.
[LM] emphasized the significant problem with deleting refs in `packed-refs`, which requires
rewriting the entire file. Testing of `reftable` is also being done on NFS.

[LM] mentioned that C Git still has many issues with regards to `reftable`, including corruption
of the refs, and expressed a need to identify specific test cases.

## Gerrit User Summit in Paris, 17–19 October 2025

Regarding the Gerrit User Summit in Paris, [SZ] stated that their initial plan to organize
a hackathon there faced issues, and they will recheck the possibility of at least one or
two team members attending just for the summit.

## AI features in Gerrit Code Review

 [LM] highlighted the [ai-features topic](https://gerrit-review.googlesource.com/q/hashtag:%22ai-features%22+(status:open%20OR%20status:merged))
 on Gerrit Review related to AI features. [EK] clarified that their AI focus is currently internal
 for Googlers. [SZ] had also seen the feature, noting that the AI prompt appeared self-contained.
 [SZ] expressed interest in the Gerrit community consolidating ideas for AI integrations, mentioning
 a question from SAP about AI-based automation.
