---
title: "Fixing a bug"
permalink: bug-fixing.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Who is allowed to fix bugs?

Anyone who has accepted [the CLA for the Gerrit Code Review project](https://gerrit-review.googlesource.com/Documentation/dev-cla.html)!
If you feel like contributing and need a place to start you will always find bugs that need
fixing, big and small, on the [issue-tracker](https://www.gerritcodereview.com/issues.html).

_Consider bugs in "accepted" state first since these have already been through triage._

## How do I go about it?

You should probably start by [setting up a development environment](https://gerrit-review.googlesource.com/Documentation/dev-readme.html).
After which you can follow the workflow below.

## Bug-fix workflow

### 1. Add yourself as owner to the corresponding issue and mark it as "Started"

This will announce to everyone else that you are working on the bug, which most likely will
make other affected users very happy which is always positive.

If there is no issue for the bug you want to fix you'll need to create one first in the
[issue-tracker](https://www.gerritcodereview.com/issues.html).

### 2. Find the earliest supported branch that has the bug

Besides master you'll need to check the [supported stable-branches](https://www.gerritcodereview.com/releases-readme.html).

_One way to accomplish this is to write a test-case that reveals the bug and cherry-pick that onto
each supported branch to see if the issue reproduces on that branch._

### 3. Fix the bug on this branch

Hard to give any generalizable advice since all bugs are not created equal, but if you get stuck you
can always post a question on
 [discord](https://discord.gg/HkGbBJHYbY) or the
[mailing list](https://groups.google.com/forum/#!forum/repo-discuss).

_You should always aim to add a test-case that fails without your bug-fix._

#### Fixed on master?

Although this workflow should be followed when fixing bugs it sometimes happens that some of the
steps are skipped. It may pay off to check if the bug is fixed on master.

__NOTE:__ Not all changes are applicable or a good fit for older stable-branches. You should
take great care when cherry-picking or otherwise back-porting fixes from newer stable branches
or master.

### 4. Link your commit to the issue

To link the bug-fixing commit to the issue you should add a "Bug:" commit-message footer.
Example:
For the issue https://bugs.chromium.org/p/gerrit/issues/detail?id=14152, the "Bug:" footer would
look like:

```
Document our current bug-fix workflow

Bug: Issue 14152
Change-Id: I43574b6464b288643327529a3d0121bc9aad3b67
```

### 5. Push for review

You are now ready to [push your fix for review](https://gerrit-review.googlesource.com/Documentation/intro-gerrit-walkthrough-github.html#create-change).

### 6. Update release notes

Add an entry in the [release-notes](https://gerrit.googlesource.com/homepage/+/refs/heads/master/pages/site/releases/)
for the version were your fix will end up and upload for review.

### 7. [Optional] Merge your submitted fix back to master

Once submitted, if you applied your fix on a [stable branch](https://www.gerritcodereview.com/releases-readme.html),
that stable branch needs to be merged up to master through the more recent stable branches to
apply the bug-fix on those as well.

This is eventually done as part of the release work so it isn't necessary but it's appreciated if
you perform these merges yourself since, from fixing the bug, you have gathered a fresh
understanding of the context and you are hence probably best suited to solve any conflicts.

## Severe bugs and security fixes

Severe bugs and [security issues](https://gerrit-review.googlesource.com/Documentation/dev-processes.html#security-issues)
are on occasion fixed in branches that are EOL since we try to offer some support to instances that
haven't been able to migrate to a supported version yet.
