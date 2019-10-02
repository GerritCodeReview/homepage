---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Make indexing 'mergeable' configurable

## <a id="overview"> Overview

This solution adds a Gerrit config to decide if we index the field.

## <a id="detailed-design"> Detailed Design

We add a new Gerrit config: index.indexChangeMergeable. If true, Gerrit will
populate the 'mergeable' field by computing mergeability. If it is false, Gerrit
will set a special value. In the current implementation, we index this field as
a string and represent 'true' as 1 and false as '0'. It's therefore easy to
provide a special value even without upgrading the index schema.

We will clean up the existing configuration options:

index.reindexAfterRefUpdate will be removed. The decision whether or not to
reindex all changes upon an update to the target ref will be implicitly made
depending on whether or not 'mergeable' is included.

change.api.excludeMergeableInChangeInfo will be removed. The behavior will be
the new default without a global config to enable it.

We will remove SKIP_MERGEABLE from ListChangeOptions and add MERGEABLE instead.
In both cases - indexing mergeable / don't index mergeable - callers can request
the bit to be included in any ChangeInfo call by requesting 'MERGEABLE'.
The bit is served from the index if available and from the cache with the
fallback of computing it on the fly if not.

Strictly speaking, moving from SKIP_MERGEABLE to MERGEABLE isn't required, but
it seems desireable to clean up these options and move to stable, low-cost
defaults.

If index.indexChangeMergeable is false, the 'is:mergeable' operator is
unsupported.

## <a id="tradeoff"> Tradeoff discussion

Upside:
- We keep all current use cases. Most prominently, small Gerrit instances can
  still use 'is:mergeable' as query operator.
- Larger instances don't have to run an expensive computation when indexing a
  document that is never actually used and is typically stale.
- Configuration options get cleaned up and align more

Downside:
- Gerrit admins that start out with a smaller instance will run into a
  performance issue at some point and will have to turn off indexing 'mergeable'
  manually.

