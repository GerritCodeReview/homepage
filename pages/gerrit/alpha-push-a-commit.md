---
title: "Pushing a Commit"
sidebar: userguide_sidebar
permalink: pushing-a-commit.html
---
{% include important.html content="This content is currently in <b>alpha</b>. It
is still under review." %}

With typical Git repositories, you work on the files stored in a local
repository. When your updates are ready, you push those changes from your local
machine directly to the remote repository.

{{site.data.alerts.note}}
Alternatively, if you are familiar with GitHub, you make a pull request.
This request asks an authorized member of the repository to pull changes from
your copy of the repository.
{{site.data.alerts.end}}

Gerrit follows the standard Git workflow pattern, in that you use the `git push`
command to copy your files from your local machine to the remote repository.
However, instead of your changes going directly into the repository, they go
into a specific namespace. This namespace uses the following pattern:

```
refs/for/[NAME]
```

where `[NAME]` is the name of the branch to which you want to push your commit.
To learn more about the refs/for namespace, see The refs/for namespace.

## Before you begin

+ Verify that you are authorized to contribute changes to the repositories that
  you want to clone.
+ Clone a repository with a commit-msg hook, as described in
  [Cloning a Gerrit Repository](/cloning-a-gerrit-repository.html).

## Adding files

From a terminal window, use the `git add` command to inform Git that you want
to includ your updates in the next commit.

```
git add [FILE_NAME]
```

## Committing files

Use the `git commit` command to record your changes to the local repository.

```
git commit -m [MESSAGE]
```

where `[MESSAGE]` is a description of the changes in the commit.

{% include note.html content="If you omit the `-m` flag, an editor opens in
which you can type your commit message." %}

## Pushing the commit

From a terminal window, type the following command:

```
git push origin HEAD:refs/for/[BRANCH_NAME]
```

For example, to push to the master branch, type:

```
git push origin HEAD:refs/for/master
```

Your commit is now ready for review.

## What's next?

+ Learn how to update a change
+ Read about how to mark a review as Work-in-Progress
+ Review how to mark a change as private
