---
title: Gerrit 2.14 End of Life (EOL)
tags: news
keywords: news
permalink: 2019-05-31-gerrit-2-14-end-of-life.html
summary: "Announcement for End of Life (EOL) for Gerrit 2.14"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

Since releasing Gerrit 3.0.0 we have 4 stable branches that are maintained with
varying levels of activity: stable-3.0, stable-2.16, stable-2.15 and stable-2.14.

The Gerrit Engineering Steering Committee has decided that we will bring 2.14
to end of life.  This means we do not intend to make any further 2.14.x releases,
and changes will not be accepted on the stable-2.14 branch, with the following caveats:

* Fixes for critical security issues may be accepted (and new release made)
after discussion among the steering committee and maintainers

* We want to keep the branch buildable with the latest version of Bazel, so
related patches will be accepted. We may revisit this decision later depending on
volume of changes.

The caveat for security fixes also applies to stable-2.13 and earlier. Those
branches are not built with Bazel, so the second caveat is not relevant.

Plugins will continue to be built for 2.14 on CI, but there will no extra effort
from core maintainers to keep the builds working.  A separate activity to identify
actively used plugins and determine owners/maintainers will follow.

Plugins will no longer be built on CI for 2.13 and earlier. Previously built
artifacts will be moved to the archive.
