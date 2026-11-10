---
title: ""
permalink: design-docs/threaded-change-lists.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Design Doc - Change Dependency Threads

Make dependencies between changes a first-class part of Gerrit's primary
navigation surfaces: change lists (dashboards and search results) and the
relation chain on the change page. Cover Git ancestry in core, and let plugins
contribute other dependency kinds such as Zuul's `Depends-On` footers.

* [Use Cases](/design-docs/threaded-change-lists-use-cases.html)
* [Solution: Indexed parents, threaded rendering and a dependency provider API](/design-docs/threaded-change-lists-solution.html)

## Status

The proposed solution has a working implementation under review:

* Core: [hashtag:threaded-change-list](https://gerrit-review.googlesource.com/q/hashtag:%22threaded-change-list%22)
* Plugin: [change-network](https://opendev.org/inaugust/gerrit-change-network)

The implementation predates this document. Early review showed that the work
touches the change index, the query API, the frontend and the plugin API, which
is more than change-by-change review can settle. This document is here to agree
scope and direction first.
