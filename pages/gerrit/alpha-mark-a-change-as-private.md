---
title: "Marking a Change as Private"
sidebar: userguide_sidebar
permalink: marking-a-change-as-private.html
---
{% include important.html content="This content is currently in <b>alpha</b>. It
is still under review." %}

In most cases, you push commits to a remote repository to have other develoeprs
review and provide feedback. However, on occasion you might want to mark your
change as private. Private changes are visible only to you and any reviewers
already assigned to the change.

Some examples of when you might want to mark a change as private:

+ You want to check what the change looks like before formal review starts.
+ You want to use Gerrit to sync data between different devcies. By creating
  a private change without reviewers, you can push from one device, and fetch
  to another device.
+ You want to do code review on a change that has sensitive aspects.
  By reviewing a security fix in a private change, outsiders can't discover the
  fix before it is pushed out. Even after merging the change, the review can be
  kept private.

You can mark a change as private when you first push the commit, or while a
change is under review.

## Before you begin

+ Verify that you understand the steps in [Pushing a Change](/pushing-a-change.html)
  to push a change to the remote repository.

## Mark a change as private using the command line

From the terminal window, mark the change as private by adding `%private` at
the end of a `git push` command:

```
git push origin HEAD:refs/for/master%private
```

When you are ready for other contributors to review the change, you can unmark
the change from the command line:

```
git push origin HEAD:refs/for/master%remove-private
```

## Mark a change as private using the user interface

1. Navigate to the Gerrit site for your project. For example, the URL for the
   Gerrit project is `gerrit-review.googlesource.com`.
1. If you have not already done so, sign in using the icon in the upper right
   corner.
1. From the main menu bar, select **Changes** from the **Your** menu.
1. Click the change you want to mark private.
   The Change screen opens.
1. From the **More** menu, select **Mark private**.

To unmark the change as private, from the **More** menu, select
**Unmark private**.
