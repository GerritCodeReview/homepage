---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2023-12-07-esc-minutes.html
summary: "Minutes from the ESC meeting held on Dec 7, 2023"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Dec 7, 2023

Christophe Poucet, Patrick Hiesel, Luca Milanesio, Saša Živkov

### Next meeting

January, 2024

### Gerrit usafe defaults

Gerrit has not been great in choosing defaults; some of them resulted
being unsafe
(see [1](https://gerrit-documentation.storage.googleapis.com/Documentation/3.8.2/config-gerrit.html#index.paginationType)
and [2](https://gerrit-documentation.storage.googleapis.com/Documentation/3.8.2/config-gerrit.html#core.usePerRequestRefCache)).

Saša and Luca proposed to define what _"unsafe"_ means in the Gerrit
world for allowing the categorisation of configuration option settings;
the proposed definition is _"a parameter that, despite providing some
benefits may not be suitable for all setups, risking performance issues or
data corruption"_.

Patrick pointed out that when introducing new settings or improvements
to existing ones, a rule of thumb is to keep existing well-tested behaviour
as default.

How to enforce the adoption of safe default? Luca took the action of
amending the release process and including the cross-checking of new
settings and their defaults by diff-ing what changed in the
`/Documentation` folder. The definition of _"unsafe"_ default is proposed
as amendment of the current
[contributors'](https://gerrit-documentation.storage.googleapis.com/Documentation/3.9.1/dev-contributing.html)
guide.

### How to prevent breakages in Google hosted deployments

[Change 3900074](https://www.gerrit-review.googlesource.com/3900074) broke the
Gerrit setup of [Chromium](https://chromium-review.googlesource.com),
because of the lack of visibility from the contributor
of the impact of its changes on the closed-source fork of Gerrit maintained
by Google.

Patrick pointed out that a Google Prober validates all incoming changes
test in the internal CI/CD pipeline; however, the static resources servlet
was not properly covered, and the breakage passed unnoticed to the live
rollout.

Annotating the classes that are not used at Google with a `@NotUsedAtGoogle`
would not be enough to prevent future breakages because of the way that
Google manages its customisation of the unused classes.

Google will continue patrolling the incoming changes on master and complete
its internal probes suite for making sure that future modifications by 
the community would not impact the stability of its setups.

### Duplicate change-ids in the same repo/branch

Gerrit has no way to enforce the uniqueness of some secondary IDs for
a change, e.g. the triplet `Project~Branch~Change-Id`, because of the need
of trade-off uniqueness with the speed of execution.

[Issue 313935024](https://issues.gerritcodereview.com/issues/313935024)
has highlighted how it is quite simple to generate duplicates by uploading
new patch sets on the same change before the index is updated. Gerrit index
is a _best-effort_ lookup, and it may be stale or out of sync with the
underlying changes on the filesystem. Saša mentioned that the change
reindexing operation can be a lengthy operation, depending on the size of
the diff and the execution of complex Prolog rules: the scenario of
duplicates caused by a stale index are happening in real production
environments, Luca also confirmed the same.

Chris pointed out that it is impossible to assure more than one unique id
without having a transactional store, which is in two-phase-commit with the
Git repository. Hence, Gerrit needs to live with the problem and rely
on the only unique identifier that the repository can assure:
`Project~ChangeNum`.

Luca will amend the Gerrit documentation, mentioning making sure that it
is transparent for users and administrators that `Project~ChangeNum` is the
only identifier guaranteed to be unique, whilst the others are _best effort_
and can produce duplicates.

### Sunsetting plans for Prolog rules

After having declared the use of Prolog rules in repositories as deprecated,
the Gerrit community needs to know when precisely the existing rules will
end being supported.

Saša pointed out that there are still some corner cases where Gerrit
submit requirements aren't enough for implementing the equivalent of some
Prolog rules, for instance, when expressing a rule for changes having a set
of files excluding a regex.

Patrick suggested working on extending the change search predicates for
covering the missing use cases, as the submitted requirements can express
any constraint based on change queries.