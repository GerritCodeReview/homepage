---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use-case

Speed up indexing a change by removing or reworking 'mergeable'.

## <a id="acceptance-criteria"> Acceptance Criteria

Computing 'mergeable' during indexing a change document is either omitted or
reasonably fast (p50: 50ms, p99: 200ms)

The 'is:mergeable' operator is adapted to the behavior change which means that
in the case of stopping to compute 'mergeable' it is removed.

## <a id="background"> Background

We index a change on every update of the primary entity. Gerrit's indexing
implementation recomputes all fields from scratch.

'mergeable' is a searchable, boolean field that is the result of a dry run merge
operation of the current patch set into the target branch. By the virtue of the
operation - an in memory Git merge - it is slow to compute. For
chromium/chromium/src hosted on googlesource.com, its p50 is 2.2 seconds. The
p99 is 12 seconds.

Gerrit caches 'mergeability' computations. The cache is keyed by the target
branch tip and the patch set. The target branch tip can advance frequently.
Gerrit has functionality for recomputing all cache values and reindexing all
changes for any update to the target branch. This does not scale.

Even instances with a small number of changes suffer from this by wasting CPU
cycles. For all instances on googlesource.com, this functionality is turned off.

#### <a id="questions"> Questions

None.
