---
title: "Design Doc - Zoekt-Based Code Search for Gerrit - Conclusion"
permalink: design-docs/zoekt-search-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/zoekt-search
---

# Zoekt-Based Code Search for Gerrit - Conclusion

Proceed with a Gerrit-aware search platform, not direct exposure of the
underlying search engine.

The recommended initial deployment is:

* The Gerrit search plugin as the sole user-facing entry point.
* A private search platform that only ever receives project/branch-scoped
  queries, never a raw, unscoped query.
* Default-branch indexing first, expanding only after measuring real
  demand and cost.
* Search capacity and index rollout managed independently of Gerrit itself.

This gives Gerrit users access-control-respecting code search while
keeping the underlying search platform free to scale on its own terms.
