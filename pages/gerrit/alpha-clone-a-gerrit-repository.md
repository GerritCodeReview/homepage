---
title: " Cloning a Gerrit Repository"
sidebar: userguide_sidebar
permalink: cloning-a-gerrit-repository.html
---
{% include important.html content="This content is currently in <b>alpha</b>. It
is still under review." %}

As you start contributing to a Gerrit repository, your first step is to clone
the project to a local repository. To clone a Gerrit repository, you use the
same `git clone` command used for standard Git repositories. However, it is
recommended to clone the repository with a commit-msg hook. This hook
automatically adds the Change-Id that Gerrit uses to track iterations of a
commit as it goes through review.

## Before you begin

+ Verify that you are authorized to contribute changes to the repositories that
  want to clone.

## Cloning a repository with the commit-msg hook

1. Navigate to the Gerrit site for your project. For example, the URL for the
   Gerrit project is `gerrit-review.googlesource.com`.
1. If you have not already done so, sign in using the icon in the upper right
   corner.
1. From the main menu bar, click **Browse**.
   A list of available repositories opens.
1. Click the name of the repository you want to clone.
   A Downloads screen opens. This screen includes several commands that you can
   copy and use on your local machine.
1. Copy the contents of the **Clone with commit-msg hook** text box.
   By default, this command uses the HTTP protocol. Gerrit also supports SSO
   and RPC. To use one of these options, click either the **SSO** or **RPC**
   link.
1. From a terminal window on  your local machine, paste the command and run it.

You now have a clone of the repository on your local machine. In addition, any
commits you push to the remote repository automatically include a **Change-Id**.

## Cloning directly

If you want to clone a repository directly, you can do so by following the same
steps in the [previous section](cloning_a_repository_with_the_commit-msg_hook.html).
However, instead of using the command from the **Clone with commit-msg hook**
text box, copy the command from the **Clone** text box.

{% include warning.html content="Cloning this command means that your commits do
not automatically include a Change-Id." %}

## What's Next

+ Understand how to push a change to a repository
+ Read the overview of how to contribute changes to Gerrit
+ Learn more aobu tthe commit-msg hook
+ Learn more about Change-Ids



