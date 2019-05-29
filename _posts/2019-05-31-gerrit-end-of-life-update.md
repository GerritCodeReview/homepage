---
title: Gerrit End of Life (EOL) Update
tags: news
keywords: news
permalink: 2019-05-31-gerrit-end-of-life-update.html
summary: "Update on the policy for bringing Gerrit releases to end of life (EOL)"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

Per the policy mentioned on the [project homepage](https://www.gerritcodereview.com/#support),
only the last 2 releases are maintained on a best effort basis. Contrary to this,
since releasing Gerrit 3.0.0 there are 4 stable branches that currently still have
varying levels of activity: stable-3.0, stable-2.16, stable-2.15 and stable-2.14.

This post clarifies the level of maintenence/support to be expected for the
earlier branches.

## Extended support for 2.15

Support for 2.15 will be extended, due to the fact that moving forward to 2.16
(and thus migrating to Note DB) is a large step that not all users are able to
take so soon.

## EOL for 2.14 and earlier

Per the policy, we will bring 2.14 to end of life. This means we do not intend to
make any further 2.14.x releases, and changes will not be accepted on the stable-2.14
branch, with the following caveats:

* Fixes for critical security issues may be accepted (and new releases made)
after discussion among the steering committee and maintainers

* We want to keep the branch buildable with the latest version of Bazel, so
related patches will be accepted. We may revisit this decision later depending on
the volume of changes.

Branches for earlier releases (stable-2.13 and older) are already inactive
and are considered unmaintained. We do not intend to make any new releases
from these branches, even for security fixes.

## Support for non-core plugins

* 2.15

  Plugins will continue to be
  [built for 2.15 on CI](https://gerrit-ci.gerritforge.com/view/Plugins-stable-2.15/),
  and core maintainers will ensure that they still build, on a best-effort basis.

* 2.14

  Plugins will continue to be
  [built for 2.14 on CI](https://gerrit-ci.gerritforge.com/view/Plugins-stable-2.14/),
  but core maintainers will not put extra effort into keeping the builds working.

* 2.13

  Plugins will no longer be built on CI for 2.13 and earlier. Previously built
  artifacts will be moved to the [CI archive](https://archive-ci.gerritforge.com/).

A separate activity to identify actively used plugins and determine
owners/maintainers will follow.
