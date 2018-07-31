---
title: "Updating a Change"
sidebar: userguide_sidebar
permalink: updating-a-change.html
---
{% include important.html content="This content is currently in <b>alpha</b>. It
is still under review." %}

One of the main benefits of code review is the ability to receive and
incorporate feedback from other developers. With Gerrit, you incorporate these
changes by amending the commit. Gerrit uses the CHange-Id to ensure that each
iteration of the commit are stored together as patchsets.

{% include note.html content="You can only amend the most recent commit." %}

## Before you begin

+ Follow the steps in [Pushing a Change](/pushing-a-change.html) to push a
  change to the remote repository.

## Adding files

From a terminal window, use the `git add` command to inform Git that you want
to include your updates in the next commit.

```
git add [FILENAME]
```

## Amending the commit

Use the `git commit --amend` command to update the most recent commit.

```
git commit --amend
```

## Pushing the amended commit

From a terminal window, type the following command:

```
git push origin HEAD:refs/for/[BRANCH_NAME]
```

For example, to push to the master branch, type:

```
git push origin HEAD:refs/for/master
```

Gerrit updates the commit under review with your latest changes.

## What's next?

+ Learn about patchsets


