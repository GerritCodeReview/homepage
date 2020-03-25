---
title: "Gerrit Project News #7: February-March 2020"
tags: news
keywords: news
permalink: 2020-03-27-gerrit-news-feb-mar-2020.html
summary: "Gerrit project news from February and March 2020."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## New plugins home page

A [new page](https://www.gerritcodereview.com/plugins.html) that lists all Gerrit plugins has been
added to the homepage. Beside listing the plugins known to the project, that page shows the current
compatibility status of each plugin towards every supported Gerrit version. The page gets updated
at least daily, which makes its CI build status for each plugin and version fairly current.

For each plugin, the known plugin maintainers are also listed. New plugin maintainer candidates are
welcome, to help cover unmaintained plugins. Existing maintainer lists could also be augmented, or
amended, based on maintainer or community feedback.

This new page is reachable from the Code top menu, selecting Plugins.

## Emerging end-to-end test framework

There is an [initial framework](https://gerrit-review.googlesource.com/Documentation/dev-e2e-tests.html)
for Gerrit 3.1 and up, based on [Gatling](https://gatling.io/), to start implementing end-to-end
(e2e) tests. Initially meant for load testing, the framework started to support functional e2e test
scenarios, [reusing that stack](https://gatling.io/load-testing-continuous-integration/) further.

The GerritForge team, who originally
[introduced the framework](https://gitenterprise.me/2019/12/20/stress-your-gerrit-with-gatling/)
for Gerrit, have been using load test scenarios internally since. Other community members are as
welcome to start using the framework, for either load or functional e2e test purposes. The
[documentation](https://gerrit-review.googlesource.com/Documentation/dev-e2e-tests.html) explains
the test scope differences in Gerrit, and how to use the framework where the e2e scope applies.

Beside core, Gerrit plugins can now start reusing that framework in turn. Initial yet basic
functional scenarios were recently introduced for the
[high-availability](https://gerrit.googlesource.com/plugins/high-availability/) and
[multi-site](https://gerrit.googlesource.com/plugins/multi-site) plugins. It is currently likely
that more will come, as internal e2e test suites become open-sourced (thus reusable) that way.
