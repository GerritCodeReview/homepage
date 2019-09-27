---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use-case

As a user, I want Gerrit operations to be fast and their end result to be
consistent. When I use change search, I expect all operators to work as
documented and the results to conform to my search query.

When I search for 'is:mergeable' I expect to see changes that are all mergeable
or get an error message that informs me about the operator being unavailable on
my Gerrit installation.

When I upload a change to Gerrit, post a comment or perform other write actions
on a change, I expect Gerrit to run only meaningful computations - at least
synchronously - and to return a result that is correct and consistent as fast as
possible.

## <a id="acceptance-criteria"> Acceptance Criteria

1) A change search for 'is:mergeable' and '-is:mergeable' produces correct
results or fails with a descriptive message. It does not give incorrect results,
ever.

2) When indexing a document, we compute only fields that are used either by
operators or for reconstructing information that is served to users when serving
query results.

3) The solution works for Gerrit instances of all sizes with respect to user
activity and the number of (open) changes.

## <a id="background"> Background

We index a change on every update of the primary entity. Gerrit's indexing
implementation recomputes all fields from scratch.

'mergeable' is a searchable, boolean field that is the result of a dry run merge
operation of the current patch set into the target branch. By the virtue of the
operation - an in memory Git merge - it is slow to compute. For
chromium/src hosted on googlesource.com, its p50 is 2.2 seconds. The p99 is 12
seconds.

Gerrit caches 'mergeability' computations. The cache is keyed by the target
branch tip and the patch set. The target branch tip can advance frequently.
Gerrit has functionality for recomputing all cache values and reindexing all
changes for any update to the target branch.
This is not problematic for Gerrit instances that either have a low number of
open changes or when the target refs advance only rarely.
For instances that violate either of these assumptions, this does not scale. The
bottleneck comes especially from the number of open changes. Imagine an instance
with 100k open changes for refs/heads/master. Upon ever update to that ref,
Gerrit would have to reindex 100k changes (given the current logic).

#### <a id="questions"> Questions

None.
