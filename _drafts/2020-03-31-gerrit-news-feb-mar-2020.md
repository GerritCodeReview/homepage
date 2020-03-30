---
title: "Gerrit Project News #7: February-March 2020"
tags: news
keywords: news
permalink: 2020-03-31-gerrit-news-feb-mar-2020.html
summary: "Gerrit project news from February and March 2020."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Cancellation of Spring Hackathon

Due to the ongoing situation with COVID-19, there will be no Spring hackathon
this year. We are looking into the possibility of doing a remote/virtual
hackathon, and discussing plans for the release of Gerrit 3.2 which would have
been done during the hackathon.

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

Potential backports of the framework to
[supported](https://www.gerritcodereview.com/support.html#supported-versions) downstream Gerrit
versions could eventually be considered.

The [GerritForge](https://www.gerritforge.com) team, who originally
[introduced the framework](https://gitenterprise.me/2019/12/20/stress-your-gerrit-with-gatling/)
for Gerrit, have been using load test scenarios for the high-availability and multi-site plugins,
as well as to validate the Gerrit 3.1 release. Other community members are as welcome to start
using the framework, for either load or functional e2e test purposes. The
[documentation](https://gerrit-review.googlesource.com/Documentation/dev-e2e-tests.html) explains
the test scope differences in Gerrit, and how to use the framework where the e2e scopes apply.

Beside core, Gerrit plugins can now start reusing that framework in turn. Initial yet basic
functional scenarios were recently introduced for the
[high-availability](https://gerrit.googlesource.com/plugins/high-availability/) and
[multi-site](https://gerrit.googlesource.com/plugins/multi-site) plugins. It is currently likely
that more will come, as internal e2e test suites become open-sourced (thus reusable) that way.

## New 'Revert Submission' Feature

Development of the 'Revert Submission' feature has completed, and it is now live
on gerrit-review. See more about this feature in the
[design document](https://www.gerritcodereview.com/design-docs/revert-submit.html).

## New 'Preview/Apply Fix' Feature

When posting robot comments, suggestions for a fix can be directly attached to it. This feature has
been present in Gerrit for some years. However, those fixes weren't shown on Gerrit's UI. This has
changed. Robot comments now have a `Show fix` button when at least one fix is available for them.

![Robot Comment With Show Fix](/images/news-feb-march-2020-show-fix.png)

The button opens a dialog indicating how the fix would modify the code.

![Preview Fix Dialog](/images/news-feb-march-2020-preview-fix.png)

If several fixes are present, users can switch between them and use `Apply fix` on the one they
prefer. The code modifications will end up in a change edit which can be further adjusted before
being published.

## New 'Findings' Tab

The `Findings` tab next to the `Files` section gives an overview of and quick access to all robot
comments on a patch set. 

![Findings Tab](/images/news-feb-march-2020-findings-tab.png) 

## Frontend framework changes

Frontend development has moved from Bower to NPM, and from HTML to JS for imports.
