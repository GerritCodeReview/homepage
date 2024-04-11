---
title: "Issue Tracking"
permalink: issues.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

[Issues][list] are tracked in the [Gerrit Code Review Issue Tracker][tracker].

[list]: https://issues.gerritcodereview.com/issues?q=status:open
[tracker]: https://issues.gerritcodereview.com/

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

| Priority          | Target Response Time | Resolution     |
|-------------------|----------------------|----------------|
| [Priority-0][p0]  | 1 working day        | "soon"         |
| [Priority-1][p1]  | 5 working days       |                |
| [Priority-2][p2]  | 30 working days      | best effort    |
| [Priority-3][p3]  | -                    | best effort    |
| [Priority-4][p4]  | -                    | best effort    |

As explained on the [support](support.html#response-time-and-slo) page the
Gerrit community aims to achieve the target response times that are documented
above, but there **IS NO guaranteed Service Level Agreement**.

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
  resources to do this soon.  Gerrit is an open-source project;
  contributions are appreciated.
- Desirable feature or enhancement *not* on the roadmap.

### Priority-4
- Ponies and icebox.
- Unfortunate: it's a legitimate issue, but the team never plans to
  fix this.

## Type
- *Type-Bug* is broken functionality.
- *Type-Feature* is a request for new feature or enhancement.

## Components

Overview about the most important components (not an exhaustive list).

### WebFrontend
Component for the Gerrit web frontend. Issues in this component are actively
triaged by the Gerrit Experience team at Google.

### Backend
General component for Gerrit backend issues. Issues that affect the
`googlesource.com` family of servers, including gerrit-review.googlesource.com,
may be tagged with the `Host-Googlesource` label, which brings them to the
attention of the Gerrit Infrastructure team at Google.

### Hosting>googlesource
Component for issues that are unique to the `googlesource.com` family of
servers, including gerrit-review.googlesource.com. This covers both
administration support required (e.g. fix a broken user account) and issues
unique to the server's plugins (e.g. authentication/web sessions or secondary
index). Issues in this component are actively triaged by the Gerrit
Infrastructure team at Google.

### SteeringCommittee
Component for issues regarding the
[governance of the Gerrit project](https://gerrit-review.googlesource.com/Documentation/dev-processes.html#steering-committee).
The [Engineering Steering Committee](https://www.gerritcodereview.com/members.html#engineering-steering-committee)
is triaging issues on this component on a regular basis (e.g. monthly).

### Community
Component for issues regarding the health of the Gerrit community. The
[community managers](https://www.gerritcodereview.com/members.html#community-managers)
are triaging issues on this component on a regular basis (e.g. monthly).

### plugins
Plugins that are actively developed may have their own subcomponent:
`Plugins>{plugin-name}`

[p0]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D0
[p1]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D1
[p2]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D2
[p3]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D3
[p4]: https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=Priority%3D4
