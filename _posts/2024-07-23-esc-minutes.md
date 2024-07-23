---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2024-07-23-esc-minutes.html
summary: "Minutes from the ESC meeting held on July 23, 2024"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meetings, July 23 and Mar 6, 2024

Patrick Hiesel, Luca Milanesio, Saša Živkov

### Update to Servlet API 6.0 (ESC of July 23)

JGit [moved to Jakarta 5.0 back in May 2024](https://eclipse.gerrithub.io/c/eclipse-jgit/jgit/+/189213)
and when its `next` branch was merged to `master`, it made it incompatible
with Gerrit that still relies on servlet API v3.1.0.
JGit has now moved [to Jakarta Servlet-API v6.0](https://eclipse.gerrithub.io/c/eclipse-jgit/jgit/+/201617).

The impact of upgrading Gerrit to Jakarta is large and it implies amending
all imports to javax.servlet. Patrick is checking the impact and status
of Google's implementation of the Servlet API.

### SPAM on gerrit-review.googlesource.com (ESC of July 23)

Spammers have been targeting 
[Change 390074](https://gerrit-review.googlesource.com/390074) broke the
Gerrit setup of [Chromium](https://chromium-review.googlesource.com),
because of the lack of visibility from the contributor
of the impact of its changes on the closed-source fork of Gerrit maintained
by Google.

The repo-discuss mailing list has a message moderation policy that allows
existing regular members to keep on posting without delay; however, new
users would require a manual approval by a moderator. Taking the same
approach for Gerrit would be one option.

Patrick offered to check also another option where gerrit-review.googlesource.com
could require strong authentication (e.g. using Google Authenticator or
a valid Mobile Phone with text message verification) for allowing
users to access Gerrit.

### Security issues when running Gerrit on Windows Server (ESC of July 23)

Gerrit Code Review is not actively tested, verified and supported on
Microsoft Windows Server. It is a common agreement amongst the ESC members
that the status-quo needs to be made more visible and explicit in Gerrit
documentation. It is not in the interest of the community to activey
fix problems reported on Windows Server, including security issues, when
they do not impact Linux or other popular Unix platforms.

Luca has created [Change 433917](https://gerrit-review.googlesource.com/c/gerrit/+/433917)
for amending Gerrit documentation accordingly.

### Library compliance speed-lane (ESC of Mar 6)

Saša highlighted that the library updates in the Gerrit code-base are
often slowed down by delays in obtaining the `Library-Compliance +1` and
therefore changes getting merged.

Patrick highlighted the challenges at Google where all the libraries need
to aligned across all products, which takes some time because of the challenges
in making the associated code changes.

Luca proposed a _speed-lane_ process where dependencies updates can be trialled
in the Gerrit open-source community first and then adopted by Google at later
time once the products alignment process is complete. That would be potentially
feasible if the dependencies changes do not involve source code changes in the
Gerrit code-base but only a different build process.

The ESC agreed to document the _sleed-lane_ process and make a trial for the
forthcoming dependencies updates, especially the urgent ones related to security
fixes in the 3rd party libraries.

### Gerrit-CI security incident - CVE-2024-23897 (ESC of Mar 6)

Luca reported the status of the actions taken to mitigate the impact of the
[Jenins security vulnerability CVE-2024-23897](https://nvd.nist.gov/vuln/detail/CVE-2024-23897)
on the Gerrit CI. The sequence of events, mitigations and post-mortem analysis
is published on [Google Docs](https://docs.google.com/document/d/1vDjunjDrLYYpVoVON-B_c83f56Nhm-lMDMjXmYmFYk4/edit#heading=h.okh75qn4l4b9)
and all actions have been completed, with the split of the CI system into two parts:

- [Public Gerrit CI](https://gerrit-ci.gerritforge.com) for incoming change validations but
  without any stored credentials or keys.

- Private Gerrit CI (not exposed to any external network) for publishing of the Gerrit
  homepage and other End-to-End validations that would require the use of stored credentials.

### Transition of the RBE executions to BuildBuddy (ESC of Mar 6)

Luca has presented the [work made by Alvaro](https://groups.google.com/g/repo-discuss/c/jQPgaKmaNQA)
for transitioning the execution of Gerrit RBE builds to BuildBuddy with on-premises workload executors.

The ESC agreed to transitioning the executions to BuildBuddy / on-premises.
