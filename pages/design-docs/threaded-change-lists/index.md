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
