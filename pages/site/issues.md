---
title: "Issue Tracking"
sidebar: gerritdoc_sidebar
permalink: issues.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

[Issues][list] are tracked at bugs.chromium.org.

[list]: https://bugs.chromium.org/p/gerrit/issues/list?can=2

## Status

Issues that do not have a contributor actively working on them may be
in one of three states:
- *New*: issue has not had initial review yet.
- *AwaitingInformation*: issue needs more detail attached.
- *Accepted*: problem reproduced or feature request acknowledged.

Issues being worked on should change the status to let others know it
may be resolved in the near future:
- *Started*: a contributor has begun work on this issue.
- *ChangeUnderReview*: a change for this issue been uploaded for
  code review.

Closed states resolve an issue:
- *Submitted*: a fix has been submitted to a stable branch or the
  master branch and will be included in a future release.
- *Released*: a release has been announced including this fix.

## Priority

| Priority          | Response     | Resolution     |
|-------------------|--------------|----------------|
| [Priority-0][p0]  |              | "soon"         |
| [Priority-1][p1]  |              |                |
| [Priority-2][p2]  | 3 months     | best effort    |
| [Priority-3][p3]  | 6 months     | best effort    |
| [Priority-4][p4]  | 12 months    | best effort    |

### Priority-0
- Critical issue causing failures in production.
- Major functionality broken that renders a feature unusable.

### Priority-1
- Urgent; the issue is blocking a user from getting their job done.
- Breakage blocking next release (e.g. Guice injectors).
- Defect causing functional regression in production.
- Production issue impacting customers.

### Priority-2
- Work tied to roadmap, or near term upcoming release.
- Inconvenient bug that should be addressed in one of the next few
  releases.

### Priority-3
- We feel your pain: the team would like to fix this, but lacks the
  resources to do this soon.  Gerrit is an open source project;
  contributions are appreciated.
- Desirable feature or enhancement *not* on the roadmap.

### Priority-4
- Ponies and icebox.
- Unfortunate: it's a legitimate issue, but the team never plans to
  fix this.

## Type
- *Type-Bug* is broken functionality.
- *Type-Feature* is a request for new feature or enhancement.

## Component

### PolyGerrit
The new web interface built in Polymer.  Issues in this component are
actively managed by PolyGerrit maintainers involved in the daily
development efforts.

### NoteDb
Related to the change metadata in Git project, which is migrating
Gerrit off the SQL "ReviewDb" database.

### googlesource
Issue is unique to the `googlesource.com` family of servers, including
gerrit-review.googlesource.com.  This covers both administration
support required (e.g.  correct a broken user account) and issues
unique to the server's plugins (e.g.  authentication/web sessions or
secondary index).

### plugins
Issues for a plugin project hosted under [plugins/][plugins].
Actively developed plugins may have their own subcomponent.

[plugins]: https://gerrit.googlesource.com/plugins/

[p0]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D0
[p1]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D1
[p2]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D2
[p3]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D3
[p4]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D4
