---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Remove field

## <a id="overview"> Overview

This solution removes the 'mergeable' field from the index entirely.

## <a id="detailed-design"> Detailed Design

We will remove the 'mergeable' field from the indexed document by adding a new
index schema version. We also remove the respective operator.

This will require a change index schema upgrade.

Furthermore, we will stop serving 'mergeable' on the change search responses by
default. If callers need the field, they can call the respective API endpoint that
computes just this one bit or provide a 'MERGEABLE' list changes option.

This option requires lazy loading. This is behavior also used for other options
that Gerrit backfills by reading repository data or running computations (an
existing example is ALL_COMMITS).

This is motivated by the fact that most callers don't need this bit, yet, Gerrit
is currently still forced to compute it - or reconstruct a likely stale variant
from the index.

This solution will remove index.reindexAfterRefUpdate and
change.api.excludeMergeableInChangeInfo. The first one is no longer needed as
the index document would not change if the target ref updates.
The second one will just be the default and callers need to request the field
explicitly. Therefore, it can be removed.

## <a id="tradeoff"> Tradeoff discussion

Upsides:
- No bottleneck when a small Gerrit instance grows
- Clean configs with less moving parts

Downsides:
- Removal of operator and functionality that breaks existing use cases
