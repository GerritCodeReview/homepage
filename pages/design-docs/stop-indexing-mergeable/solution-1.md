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
default. If callers need the field, the can call the respective API endpoint that
computes just this one bit or provide a 'MERGEABLE' query option.

This is motivated by the fact that most caller don't need this bit, yet, Gerrit
is currently still forced to compute it - or reconstruct a likely stale variant
from the index.
