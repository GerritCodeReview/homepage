---
title: "Gerrit Code Review - Support"
permalink: support.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Quick Links

* [Mailing list][repo-discuss]
* [Issue tracker][issue-tracking]

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
| 3.3      | Active         |       |
| 3.2      | Active         |       |
| 3.1      | Active         |       |
| 3.0      | EOL            | [EOL since December 1st, 2020](https://www.gerritcodereview.com/2020-09-07-gerrit-3.3-release-plan.html#end-of-life-for-gerrit-30x) |
| 2.16     | EOL            | [EOL (with exceptions) since June 1st, 2020](https://www.gerritcodereview.com/2020-04-22-gerrit-3.2-release-plan.html#end-of-life-for-gerrit-216x) |
| 2.15     | EOL            | [EOL since November 15th, 2019](https://www.gerritcodereview.com/2019-11-15-gerrit-2.15-eol.html) |
| 2.14     | EOL            | [EOL since May 31st, 2019](https://www.gerritcodereview.com/2019-05-31-gerrit-end-of-life-update.html) |
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

There are companies that are very active in developing and supporting the Gerrit Code Review
core and the associated plugins: see below a short non-exhaustive list of companies and their
published support policies.

### [GerritForge](http://www.gerritforge.com)

GerritForge is [UK-based Private Limited Company](https://find-and-update.company-information.service.gov.uk/company/06895373)
with a passion for Open-Source and is fully committed to providing *all of its source code contributions*
and know-how to the community, including bug-fixes, features, plugins, help and support.

GerritForge has been active in the Gerrit Code Review community
[since GitTogether 2011](https://opensource.googleblog.com/2011/12/gittogether-2011.html),
has contributed [thousands of changes](https://analytics.gerrithub.io/kibana/s/gerritcodereview/goto/1102029a35bbff8b89187b8aa31a22b4)
to the Gerrit platform and has been organizing the Gerrit User Summits and Hackathons
since the [Longon Hackathon 2013](https://gerritforge.com/events.html).

### Community support policy

GerritForge provides free Community Support (CS) for the Gerrit community using two channels:
1. [Repo-discuss mailing list](https://groups.google.com/g/repo-discuss)
2. [Gerrit issue-tracker](https://bugs.chromium.org/p/gerrit)

The channels are monitored daily, 8:00-23:00 GMT (working days, excluding UK+EU Bank Holidays).
The target response time is aligned with the general Gerrit Support SLO.

**NOTE**: GerritForge does not answer to private e-mails or Slack channel direct messages,
because the aim of community support is to spread the knowledge with the whole community.

All Gerrit non-EOL releases are actively supported and GerritForge is happy to contribute bug-fixes
on [gerrit-review.googlesource.com](https://gerrit-review.googlesource.com) and provide
the [CI/CD pipeline](https://gerrit-ci.gerritforge.com) for building the packaged artifacts for
download.

GerritForge keeps an archive of EOL plugins builds on the
[CI/CD archive site](https://archive-ci.gerritforge.com/), available for download but not actively
maintained or supported.

Gerrit EOL releaes *may be* also supported on a good-will basis, if the problem can be also reproduced
and still relevant on a non-EOL version.

Problems and fixes associated with EOL releases, no more relevant for non-EOL releases, fall within
the scope fo the GerritForge's Enterprise support.

### Enterprise support policy

Enterprise Support (ES) is reserved for GerritForge customers and is provided using three main channels:
1. [GerritForge Support portal](https://www.gerritforge.com/support)
2. [GerritForge Support e-mail](mailto:support@gerritforge.com)
3. [Global phone numbers or Video-conference](https://www.gerritforge.com/contact.html)

The channels are monitored on a 24/7 basis, 365 days a year. The response time is guaranteed by the
[support contract terms and conditions](https://www.gerritforge.com/20191007.GerritEnterpriseSupport.TermsAndConditions.GerritForge.pdf)
while the resolution time depends on the problem.

See below the guaranteed response time SLA at a glance (Silver, Gold or Platinum support contracts):

| Severity | Description                                                    | Silver | Gold  | Platinum
|----------|----------------------------------------------------------------|---------------------------
| P1       | Emergency: complete outage or loss of service or functionality | 24 h   | 8 h   | 4 h
| P2       | Urgent: reduced service or functionality, security, integrity  | 5 wd   | 24 h  | 8 h
| P3       | Non-urgent: Software or procedural problems                    | 30 wd  | 5 wd  | 24 h
| P4       | Everything else                                                | -      | 30 wd | 5 wd

**LEGEND**: `wd`=working days (UK Calendar), `h`=hours.

### Supported plugins

[GerritForge team members](https://analytics.gerrithub.io/kibana/s/gerritcodereview/goto/1102029a35bbff8b89187b8aa31a22b4)
have developed a number of
[plugins over the past 10 years](https://www.gerritcodereview.com/plugins.html) and are happy to support
them.

The support for plugins follows the same CS and ES support policies adopted for Gerrit Code Review.

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
