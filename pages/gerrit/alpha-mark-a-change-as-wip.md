---
title: "Marking a Change as a Work In Progress"
sidebar: userguide_sidebar
permalink: marking-a-change-as-a-wip.html
---
{% include important.html content="This content is currently in <b>alpha</b>. It
is still under review." %}

Usually, you push a commit when you want other contributors to review it. By
default, all changes are public, which means any contributor can review the
change. There are several situations in which you might want to push a commit
but not have other contributors review it. In such cases, you can mark your
change as a work in progress.

{% include note.html content="Another option is to mark a change as private, so
that only the reviewers you choose can access it." %}

Some examples of when you might mark a change as a work in progress include:

+ You want to run tests on your change before you officially request for
  feedback.
+ During a review, you decide you need to rework your change, and you want to
  stop notifying reviewers until you complete your updates.

You can mark a change as a work in progress using either the command line or
the user interface.

## Before you begin

+ Verify that you understand the steps in [Pushing a Commit](/pushing-a-commit.html)
  to push a change to a remote repository.

## Mark a change as work in progress using the command line

From a terminal window, mark the change as a work in progress by adding `%wip`
at the end of a `git push` command:

```
git push origin HEAD:refs/for/master%wip
```

When you're ready for other contributors to review your change, you can unmark
the change using the following command:

```
git push origin HEAD:refs/for/master%ready
```

## Mark a change as a work in progress using the user interface

1. Navigate to the Gerrit site for your project. For example, the URL for the
   Gerrit project is `gerrit-review.googlesource.com`.
1. If you have not already done so, sign in using the icon in the upper right
   corner.
1. From the main menu bar, select **Changes** from the **Your** menu.
1. Click the change you want to mark as a work in progress.
   The Change screen opens.
1. From the **More** menu, select **Mark as work in progress**.

To mark the change as ready for review, open the change and click
**Start Review**.

