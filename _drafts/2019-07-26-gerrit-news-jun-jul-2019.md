---
title: "Gerrit Project News #3: June-July 2019"
tags: news
keywords: news
permalink: 2019-07-26-gerrit-news-jun-jul-2019.html
summary: "Gerrit project news from June and July 2019."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Community Managers

The Gerrit Community Managers for 2019 were
[announced](https://www.gerritcodereview.com/2019-06-28-cm-announce.html):

* Edwin Kempin (Google)
* Marco Miller (Ericsson)
* Matthias Sohn (SAP)

See the linked post for details.

## User Summits and Hackathons in Sweden and USA

The schedules are finalized for the user summits in
[Gothenburg](https://gerrit.googlesource.com/summit/2019/+/refs/heads/master/schedule-europe.md)
and [Sunnyvale](https://gerrit.googlesource.com/summit/2019/+/refs/heads/master/schedule-usa.md).

## Work on Gerrit Performance

In 2019, one of the major efforts we are working on is performance. Gerrit’s new
UI has support for client-side monitoring through plugins which is great for
measuring exactly what the user experiences. We use these client side metrics
and apply the
[RAIL](https://developers.google.com/web/fundamentals/performance/rail) model to
provide targets for latency. The current focus is on read latency - that is
browsing around on the Gerrit web UI and looking at changes, diffs and
dashboards. Write latency - that is posting a code review, creating draft
comments, ... - will follow once reads are acceptably fast.

This is an effort that goes all across the stack, it covers the UI, Gerrit’s
backend as well as storage formats of data on disk where necessary.

Until now we picked a lot of low hanging fruits that speed things up notably.
For example: Rendering Polymer components
lazyly instead of all-at-once when the app starts up; sending index queries in
parallel if the index backend supports that; inline data that is required when
the app starts into index.html to spare extra requests; rendering the correct
avatar sizes by default to spare extra round trips to the backend.

In the upcoming months, we want to fine-tune caching, work on external IDs and
have the UI send requests to the backend earlier to allow for longer processing
without latency impact.

