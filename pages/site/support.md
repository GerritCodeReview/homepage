---
title: "Gerrit Code Review - Support"
permalink: support.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Quick Links

* [Mailing list][repo-discuss]
* [Issue Tracking][issue-tracking]

## Supported Versions

The Gerrit open-source community actively supports the last 3 releases
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
| 3.12     | Active         |       |
| 3.11     | Active         |       |
| 3.10     | Active         |       |
| 3.9      | EOL            | [EOL since May 19, 2025](https://www.gerritcodereview.com/2024-10-03-gerrit-3.12-release-plan.html#end-of-life-for-gerrit-39x) |
| 3.8      | EOL            | [EOL since Dec 2, 2024](https://www.gerritcodereview.com/2024-10-03-gerrit-3.11-release-plan.html#end-of-life-for-gerrit-38x) |
| 3.7      | EOL            | [EOL since May 17, 2024](https://www.gerritcodereview.com/2024-02-13-gerrit-3.10-release-plan.html#end-of-life-for-gerrit-37x)|
| 3.6      | EOL            | [EOL since Nov 24, 2023](https://www.gerritcodereview.com/2023-10-05-gerrit-3.9-release-plan.html#end-of-life-for-gerrit-36x) |
| 3.5      | EOL            | [EOL since May 19, 2023](https://www.gerritcodereview.com/2023-03-31-gerrit-3.8-release-plan.html#end-of-life-for-gerrit-35x)     |
| 3.4      | EOL            | [EOL since Nov 9, 2022](https://www.gerritcodereview.com/2022-09-29-gerrit-3.7-release-plan.html#end-of-life-for-gerrit-34x) |
| 3.3      | EOL            | [EOL since May 24, 2022](https://www.gerritcodereview.com/2022-02-24-gerrit-3.6-release-plan.html#end-of-life-for-gerrit-33x) |
| 3.2      | EOL            | [EOL since Dec 7, 2021](https://www.gerritcodereview.com/2021-09-07-gerrit-3.5-release-plan.html#end-of-life-for-gerrit-32x) |
| 3.1      | EOL            | [EOL since May 19, 2021](https://www.gerritcodereview.com/2021-03-16-gerrit-3.4-release-plan.html#end-of-life-for-gerrit-31x) |
| 3.0      | EOL            | [EOL since December 1st, 2020](https://www.gerritcodereview.com/2020-09-07-gerrit-3.3-release-plan.html#end-of-life-for-gerrit-30x) |
| 2.16     | EOL with [Support](#gerrit-v216-support) | [EOL since June 1st, 2020](https://www.gerritcodereview.com/2020-04-22-gerrit-3.2-release-plan.html#end-of-life-for-gerrit-216x) |
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

When posting to repo-discuss, you must adhere to the following policy:

1. Keep the discussion in topics: if there is already a topic for your
   question, you should reply to that topic. One problem is one topic and
   should be as specific as possible.

2. Avoid top-posting, use
   [interleaved posting](https://en.wikipedia.org/wiki/Posting_style#Interleaved_style)
   instead.

3. Look for existing solutions to known problems and avoid asking questions
   that have already been answered.

You can also join us on [discord][discord-server]. A maintainer or
community manager should then be able to address your request.


You could also check the questions tagged with "gerrit" on
[Stack Overflow][stack-overflow].

### Gerrit v2.16 Support

Existing users having issues with the migration to/through Gerrit v2.16 can
still use the [General Support](#generalsupport) on the mailing list as usual
and it's possible that community members will be able to assist them.

## Bugs

If the issue/question you posted on Repo Discuss is considered a bug
the community will ask you to create an issue for tracking it.
Bugs are reported to the [issue tracker][issue-tracker]. The issue tracker is
not always the best place to initially request new features, as the main focus
for those consuming it is fixing bugs. See the [issue tracking][issue-tracking]
documentation for more information.

## New Features

The Gerrit project has adopted a
[feature request model][feature-request] where you are asked to
submit your feature request together with some valid, general,
use-cases.

## Bug Triaging

All incoming issues should be triaged to decide on their
[priority](#priorities). The priority should be based on the severity, the
frequency and the risk of the issue.

Besides finding the right priority we also aim to clarify the issue so it is
well understandable what the problem is.

The triage is not meant to investigate the cause of bugs or assign issues.

Triaging should include the following steps:

1. Determine the right [priority](#priorities).
2. For feature requests set `Type` to `Feature Request`.
3. Check that the component is correctly set, and update it if necessary.
   Move security and privacy issues to the `Gerrit Code Review > Security`
   component (componentid: 1371046) to limit the issue visibility.
4. If necessary, update the issue summary to be clear.
5. If allowed flag spam issues as spam (3-dot menu -> `Mark as spam...`),
   otherwise close them as `Won't Fix (Infeasible)`.
6. Check whether the issue has been reported before and close it as `Duplicate`
   if possible.
7. Check if reproduction steps are present and clear. If not, ask the reporter
   to provide them, assign the issue to the reporter and asked them to unassign
   themselves from the issue once they provided the missing information (so that
   the issue goes back into the triage queue).
8. If the issue is about a bug that affects Gerrit servers hosted by Google
   (`googlesource.com` servers) add the issue to the `Environment-Google`
   hotlist (hotlistid: 5052245) so that Googlers can have a look.
9. For issues that do not effect Gerrit servers hosted by Google
   (`googlesource.com` servers), add the issue to the `Triaged-Yes` hotlist
   (hotlistid: 5052889) when the triaging is done.

**Tip:** Star this [bookmark
group](https://issues.gerritcodereview.com/bookmark-groups/763138) to get the
standard hotlists suggested when adding issues to hotlists.

Triaging incoming issues is a community effort and is done on a best effort
basis (also see [below](#response-time-and-slo)).

**Tip:** You can learn more about how the Gerrit project uses the issue tracker
on the [Issue Tracking][issue-tracking] page.

## Response time and [SLO](https://landing.google.com/sre/sre-book/chapters/service-level-objectives/)

Gerrit Code Review is an open-source project, which means that the people
that are using the tool are invited to cooperate and join for contributing
to its development and support.
Opening new issues, [triaging](#bug-triaging) existing ones and helping to resolve
them are ways of contributing to the project.

There **is not a formal support contract** amongst the members of the
community, therefore there **IS NO guaranteed Service Level Agreement**
on the response and resolution of the issues raised, but we are happy to
define our [SLO (Service Level Objectives)](https://landing.google.com/sre/sre-book/chapters/service-level-objectives/).
However, amongst ourselves, we are aiming to achieve the following response times,
depending on the severity of the issue raised.

<a id="priorities">Priorities:

| Severity | Description                                                 | Target response time
|----------|-------------------------------------------------------------|---------------------
| P0       | Major functionality broken that renders a feature unusable  | 1 working day
| P1       | Defect causing regression in production                     | 5 working days
| P2       | Work tied to roadmap or near term upcoming release          | 30 working days
| P3       | Desirable feature or enhancement not in the roadmap         | -
| P4       | Everything else                                             | -

> **NOTE**: Bug reports about existing features are typically classified between P0 and P3,
> feature requests are classified between P2 and P4.

There are companies that are very active in developing and supporting Gerrit
Code Review core and the associated plugins: see below a short non-exhaustive
list of companies and their published support policies.


### [Google](https://www.google.com)

The Gerrit team at Google runs its own Gerrit deployment under the
`googlesource.com` domain. This deployment is in service of Google
projects that have external visibility or external partners. The
deployment is based on the latest development commit of Gerrit.

Gerrit at `googlesource.com` shares its business logic with the
publicly available gerrit code, but has important differences in
low-level backend details, such as resource scaling, account handling,
search index, and the git storage. It also lacks SSH support. Due to
this we often lack expertise to analyze backend bugs on 'normal'
gerrit installations.

When filing a bug through the "report bug" link on googlesource.com,
the component 'Gerrit Code Review > Hosting > googlesource' is selected
by default. Issues on this component are triaged by the Gerrit
Infrastructure team at Google on a daily basis.

In addition, issues on the following components are triaged by Google:

*  The Gerrit Experiences team at Google has a daily triage round to
   look at all frontend/UI bugs (component
   'Gerrit Code Review > WebFrontend').

*  The Gerrit Infrastructure team at Google does a daily triage on all
   security bugs (component 'Gerrit Code Review > Security') as a
   matter of policy.

### [GerritForge](http://www.gerritforge.com)

GerritForge is a [USA-based Corporation](https://bizfileonline.sos.ca.gov/search/business)
with a passion for Open-Source and is fully committed to providing *all of its
source code contributions* and know-how to the community, including bug-fixes,
features, plugins, help and support.

GerritForge has been active in the Gerrit Code Review community
since [GitTogether 2011](https://opensource.googleblog.com/2011/12/gittogether-2011.html),
has contributed [thousands of changes](https://analytics.gerrithub.io/kibana/s/gerritcodereview/goto/1102029a35bbff8b89187b8aa31a22b4)
to the Gerrit platform and has been organizing the Gerrit User Summits and
Hackathons since the [London Hackathon 2013](https://gerritforge.com/events.html).

It also runs `gerrithub.io` and `eclipse.gerrithub.io`(a virtual host dedicated
to hosting Eclipse Foundation projects), which offers users an
easy way to use the latest version of Gerrit for code review and mirror branches
and tags to github.com.

GerritForge offers [**Enterprise Support (ES)**](#enterprise-support) to its
customers and [**Community Support (CS)**](#community-support) to the whole
Gerrit community; see below the SLO and SLA associated with its services.

### Community Support

GerritForge provides free Community Support (CS) for the Gerrit community using
two channels:
1. [Repo-discuss mailing list](https://groups.google.com/g/repo-discuss)
2. [Gerrit issue-tracker][issue-tracker]
3. [Discord-Server]: https://discord.gg/HkGbBJHYbY

GerritForge monitors the channels *on UK and EU working days, 8:00-23:00 GMT*,
and occasionally over week-ends and bank holidays.
Although a response is not guaranteed for community support, we aim to
meet the general [Gerrit Support SLO](#response-time-and-slo).

> **NOTE**: GerritForge does not answer to private e-mails or Discord direct messages
> under the CS umbrella, because the aim is to spread the knowledge with the whole community.

All Gerrit **non-EOL releases are actively supported** and GerritForge **is happy,
but not committed,** to directly fix the issue. GerritForge also hosts the
[CI/CD pipeline](https://gerrit-ci.gerritforge.com) for building the packaged
artifacts for download.

GerritForge keeps an archive of EOL plugins builds on the
[CI/CD archive site](https://archive-ci.gerritforge.com/).
The plugins artifacts are available for download but not necessarily maintained
or supported.

Gerrit **EOL releases may also be supported**, but not necessarily fixed, on a
good-will basis, but only if the problem can be **still relevant** on a non-EOL
version. All other problems and fixes associated with EOL releases fall within
the scope of the GerritForge's [Enterprise support](#enterprise-support).

### Enterprise Support

Enterprise Support (ES) is available to GerritForge customers [for a fee](http://gerritforge.com/pricing.html)
using dedicated channels, monitored on a **24/7 basis, 365 days a year**.

The response time is guaranteed by a strict SLA specified in the
[support contract terms and conditions](https://www.gerritforge.com/20191007.GerritEnterpriseSupport.TermsAndConditions.GerritForge.pdf).

See more details on the [GerritForge Enterprise Support web-site](https://www.gerritforge.com/support).

### Supported plugins

[GerritForge team members](https://analytics.gerrithub.io/kibana/s/gerritcodereview/goto/1102029a35bbff8b89187b8aa31a22b4)
have developed a number of
[plugins over the past 10 years](/plugins.html) and are happy to support
them.

The support for plugins follows the same [CS](#community-support) and [ES](#enterprise-support)
policies adopted for Gerrit Code Review.

[feature-request]: https://gerrit-review.googlesource.com/Documentation/dev-design-docs.html#propose
[issue-tracking]: /issues.html
[issue-tracker]: https://issues.gerritcodereview.com/
[repo-discuss]: https://groups.google.com/forum/#!forum/repo-discuss
[discord-server]: https://discord.gg/HkGbBJHYbY
[stack-overflow]: https://stackoverflow.com/questions/tagged/gerrit
