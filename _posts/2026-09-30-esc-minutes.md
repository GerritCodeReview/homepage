---
title: "Gerrit ESC Meeting Minutes, September 30th, 2026"
tags: esc
keywords: esc minutes
permalink: 2026-09-30-esc-minutes.html
summary: "Minutes from the ESC meeting held on September 30th, 2026"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

**Participants**: Hari Jeyamani [HJ], Luca Milanesio [LM]

**Next meeting**: October 28th, 2026.

---

# Executive Summary

This meeting of the Gerrit Engineering Steering Committee focused on balancing our upcoming
Gerrit v3.15 release with critical security and maintenance tasks.

Key decisions included implementing feature flags for AI review and comment permissions to
ease the review and merge of the pending changes for adding the new permissions to
the master branch.

We also outlined the release schedule for Gerrit 3.15, targeting the November user summit.

# Gerrit Engineering Steering Committee (ESC) Meeting Summary

## AI Review and Comment Permissions

To address the historical design choice that allows any registered user to comment—which has
increasingly exposed the project to spammers and inappropriate content, David Ostrovsky proposed
[a new feature flag](https://gerrit-review.googlesource.com/c/gerrit/+/635464) that would allow
Google to keep the current behaviour and settings whilst the rest of the community can use the
new permission model.

This will preserve default visibility for registered users while adding much-needed control.
[HJ] confirmed that both discussed feature flags are viable and can be configured as safe defaults.

If the feature flag for AI review can work for Google, we could think about using a similar
approach with David Ostrovsky's [second feature flag](https://gerrit-review.googlesource.com/c/gerrit/+/636063)
for enabling the introduction of the change comment permission model.

## Codebase Maintenance and Core Reduction

Reflecting on our 18-year history and having reached 4,284 contributors, we must aggressively
manage technical debt. [LM] proposed moving very old core features, such as OpenID authentication,
out of the core tree and into plugins to reduce future risks. [HJ] confirmed there is internal
alignment on formally track and deprecate these unused features.

## Performance Troubleshooting

[HJ] acknowledged that there have been performance regressions in dashboards and common code paths
since March. To resolve these bottlenecks, [LM] has offered his technical troubleshooting
assistance to Josh and the rest of the team.

## Release Plan for Version 3.15

Looking ahead, [LM] outlined the release schedule for Gerrit v3.15, which we are targeting for the
November user summit. A major highlight for Gerrit v3.15 is that it will deliver significant performance
improvements on the master branch without requiring our users to upgrade their underlying hardware.

## Action Items

* **[HJ]**: Create tracking bugs in the Google board for the new AI review and comment
  permission changes to monitor implementation progress.

* **[HJ]**: Review internal feature developments and provide an update by next week regarding
  potential items to include in the Gerrit v3.15 release.

* **[LM]**: Create a restricted mailing list tailored for large Gerrit installations to facilitate
  secure communication regarding future critical security updates.

* **[LM]**: Published the [draft release plan for Gerrit v3.15](https://gerrit-review.googlesource.com/c/homepage/+/636163)
  to the maintainers for review.
