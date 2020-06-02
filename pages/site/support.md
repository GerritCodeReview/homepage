---
title: "Gerrit Code Review - Support"
permalink: support.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Supported Versions

The Gerrit open-source community actively supports the last 2 releases
on a best effort basis. Older releases are not actively maintained but
may still receive important fixes (e.g. security fixes), but there is
no guarantee for this. Which fixes are backported to these old
releases is decided on a case by case basis.

End of life for old release happens implicitly when a new Gerrit version is
released, and is announced via the [project news](https://www.gerritcodereview.com/news.html)
and on the mailing list.

The following table shows the current level of support for Gerrit releases:

| Version  | Support Status | Notes |
|----------|----------------|-------|
| 3.2      | Active         |       |
| 3.1      | Active         |       |
| 3.0      | Active         |       |
| 2.16     | EOL            | [EOL (with exceptions) since 1 June 2020](https://www.gerritcodereview.com/2020-04-22-gerrit-3.2-release-plan.html#end-of-life-for-gerrit-216x) |
| 2.15     | EOL            | [EOL since 15 November 2019](https://www.gerritcodereview.com/2019-11-15-gerrit-2.15-eol.html) |
| 2.14     | EOL            | [EOL since 31 May 2019](https://www.gerritcodereview.com/2019-05-31-gerrit-end-of-life-update.html) |
| 2.13     | EOL            |       |
| pre 2.13 | EOL            |       |

The same support status, as well as notes and documentation for every recent Gerrit release is
[detailed here](https://www.gerritcodereview.com/releases-readme.html).

## General Support

[Repo Discuss][repo-discuss] should be your first stop when you
encounter an issue with Gerrit.

Here you will reach a majority of Gerrit contributors and Gerrit
admins around the world. Often someone has had your issue before
and can help you.

Many questions regarding Gerrit concerns are a direct result of
local environment and configuration. Often such issues have already
been discussed on the repo-discuss mailing list and you may find an
answer by searching through the existing posts. If you have a new
question, you can start a new discussion thread. Via the mailing
list you can reach a plethora of Gerrit experts in our world wide
community and benefit from their collective knowledge.

The repo-discuss mailing list is managed to prevent spam posts. This
means posts from new participants must be approved manually before they
appear on the mailing list. Approvals normally happen within 1 work
day. Posts of people that participate in mailing list discussions
frequently are approved automatically.

Using the [mailing list][repo-discuss], you can also request to be
invited to the open [Slack][slack-workspace] channel if prompted to. A
maintainer or community manager should then be able to address your
request. Please try [accessing it][slack-workspace] first before issuing
a request for it.

You could also check the questions tagged with "gerrit" on
[Stack Overflow][stack-overflow].

## Response time and [SLO](https://landing.google.com/sre/sre-book/chapters/service-level-objectives/)

Gerrit Code Review is an open-source project, which means that the people
that are using the tool are invited to cooperate and join for contributing
to its development and support.
Opening new issues, triaging existing ones and helping to resolve them are
ways of contributing to the project.

There **is not a formal support contract** amongst the members of the
community, therefore there **IS NO guaranteed Service Level Agreement**
on the response and resolution of the issues raised, but we are happy to
define our [SLO (Service Level Objectives)](https://landing.google.com/sre/sre-book/chapters/service-level-objectives/).
However, amongst ourselves, we are aiming to achieve the following response times,
depending on the severity of the issue raised.

| Severity | Description                                                 | Target response time
|----------|-------------------------------------------------------------|---------------------
| P0       | Major functionality broken that renders a feature unusable  | 1 working day
| P1       | Defect causing regression in production                     | 5 working days
| P2       | Work tied to roadmap or near term upcoming release          | 30 working days
| P3       | Desirable feature or enhancement not in the roadmap         | -
| P4       | Everything else                                             | -

> **NOTE**: Bug reports about existing features are typically classified between P0 and P3,
> feature requests are classified between P2 and P4.

## Bugs

If the issue/question you posted on Repo Discuss is considered a bug
the community will ask you to create an issue for tracking it.
Bugs are reported to the [issue tracker][issue-tracking].
The issue tracker is not always the best place to initially request
new features, as the main focus for those consuming it is fixing
bugs.

## New Features

The Gerrit project has adopted a
[feature request model][feature-request] where you are asked to
submit your feature request together with some valid, general,
use-cases.

[feature-request]: https://gerrit-review.googlesource.com/Documentation/dev-design-docs.html#propose
[issue-tracking]: /issues.html
[repo-discuss]: https://groups.google.com/forum/#!forum/repo-discuss
[slack-workspace]: https://gerritcodereview.slack.com
[stack-overflow]: https://stackoverflow.com/questions/tagged/gerrit
