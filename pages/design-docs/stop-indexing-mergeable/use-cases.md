---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use-case

Speed up indexing a change by removing 'mergeable'.

## <a id="acceptance-criteria"> Acceptance Criteria

'Mergeable' is not indexed, hence not computed when we index a change.
The 'is:mergeable' operator is deprecated.

## <a id="background"> Background

We index a change on every update of the primary entity. Gerrit's indexing
implementation recomputes all fields from scratch.

'mergeable' is a searchable, boolean field that is the result of a dry run merge
operation of the current patch set into the target branch. By the virtue of the
operation - an in memory Git merge - it is slow to compute. For
  chromium/chromium/src hosted on googlesource.com, it's p50 is 2.2 seconds. The
  p99 is 12 seconds.

Gerrit caches 'mergeability' computations in a cache. The cache is keyed by the
target branch tip and the patch set. The target branch tip can advance
frequently. Gerrit has functionality for recomputing all cache values and
reindexing all changes for any update to the target branch. This does not scale.

Even instances with a small number of changes suffer from this by wasting CPU
cycles. For all instances on googlesource.com, this functionality is turned off.

#### <a id="questions"> Questions

None.
