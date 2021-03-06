---
title: "Change Log Experiment"
tags: news
keywords: news
permalink: 2020-05-06-change-log-experiment.html
summary: "Announcing an experiment with the Change Log view"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Change Log Experiment

On all googlesource.com Gerrit instances we are currently running a UX
experiment in the Change Log. Some users will see a new version of that view,
and we would like to collect feedback and validate these changes before rolling
out to all users.

## What is changing?

- The "Only Comments" toggle is renamed to “Show all entries” and is set to off
by default.

- The rules for when log entries are shown have changed: All human messages are
shown, but for autogenerated messages they are only shown on one patchset. If
for example a CI system posts on patchsets 3, 4, 5, 6, 7, and a Linter posts on
patchsets 3, 5, 6, then the CI messages are only shown on ps 7, and the Linter
messages are only shown on ps 6.

- Full comment threads are shown in expanded entries instead of just the
individual comment. For example a "Done." reply is shown in the context of the
comment that it is referring to. This is similar to how comment threads are
shown in the diff views and on the Comment Threads tab.

- The additional filters/expanders "show all x messages" and "show x more" are
removed, because the default filtered view is assumed to be short enough, such
that additional filtering does not help. Users likely prefer a bit more
scrolling than having to expand some hidden messages.


## How to give feedback or report bugs?

Please use this link:
<https://bugs.chromium.org/p/gerrit/issues/entry?template=Experiment+Change+Log>
