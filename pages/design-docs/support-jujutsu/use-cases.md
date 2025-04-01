---
title: "Design Doc - Support posting changes from Jujutsu - Use Cases"
permalink: design-docs/support-jujutsu-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Goal

Enable contributors to use [Jujutsu](#background) when working with Gerrit.

# Use Cases

## <a id="primary"> Primary Use Cases

Uses case that a solution must address:

* Contributors can use Jujutsu locally to make commits and upload them to Gerrit
  for review as new changes.

* Contributors can use Jujutsu locally to rework commits and upload them to
  Gerrit for review as new patch sets for existing changes.

* Contributors can use Jujutsu locally to rebase changes and resolve conflicts.

* Contributors can use Jujutsu locally to cherry-pick changes to other branches.

## <a id="secondary"> Secondary Use Cases

Use cases that a solution may address:

* Contributors that use Jujutsu locally can rework/rebase/cherry-pick changes
  that have been uploaded by users that use native Git locally.

* Contributors that use native Git locally can rework/rebase/cherry-pick changes
  that have been uploaded by users that use Jujutsu locally.

* Contributors that use native Git (or other clients) locally can use Jujutsu
  change ID's (stored as a Git header) intead of Gerrit Change-Id's (stored as a
  footer in the commit message).

## <a id="acceptance-criteria"> Acceptance Criteria

* Contributors that use Jujutsu locally do not need to install any commit-msg
  hook to add Change-Ids to commit messages.

* Commits that are uploaded for review from Jujutsu do not need to contain a
  Change-Id as a footer in the commit message.

* When a commit is uploaded for review from Jujutsu Gerrit retrieves the
  Change-Id from a Git header (called `change-id`).

* Gerrit accepts Jujutsu change IDs that are a 32 character reverse-hex ID (e.g.
  `mlqnqnkrxpuvuuxzlzoltostwlwyskpx`).

* Gerrit supports Jujutsu change ID's at all places where Gerrit Change-Id's
  (I-hashes) can be used.

* Gerrit continues to be able to track cherry-picks across branches although
  Jujutsu change ID's are not preserved on cherry-pick.

* Uploading the very same commit for review for inclusion on different branches
  is possible if it's allowed by Gerrit's policy or configuration (in this case
  the Jujutsu change ID does not uniquely identify one change):

  * If a commit is accidentally pushed for the wrong branch, pushing it to the
    correct branch succeeds after abandoning the change for the accidental push.

  * A commit can be pushed for multiple branches when users
    [specify a base manually](https://gerrit-review.googlesource.com/Documentation/user-upload.html#base)
    or when the project has
    [receive.createNewChangeForAllNotInTarget=true](https://gerrit-review.googlesource.com/Documentation/config-project-config.html#receive.createNewChangeForAllNotInTarget)
    configured.

## <a id="background"> Background

[Jujutsu](https://github.com/jj-vcs/jj?tab=readme-ov-file#jujutsua-version-control-system)
is a version control system that allows to track and publish changes to the
code. The workflows to craft changes in Jujutsu look very compatible with
Gerrit (e.g check this
[video tutorial](https://www.youtube.com/watch?v=dwyMlLYIrPk)). In particular,
they identify changes and reviews by a change ID, which looks conceptually
similar to the Gerrit Change-Id. Supporting Jujutsu change ID's can elimate the
need to install the
[commit-msg hook](https://gerrit-review.googlesource.com/Documentation/cmd-hook-commit-msg.html)
which is a constant source of confusion, at least for new Gerrit users.

Jujutsu is gaining traction and support from developers, hence it makes sense
for Gerrit to support Jujutsu as a client. Long-term Jujutsu may become the
primary (command-line) client for Gerrit, as it seems easier to use than native
Git.

The Jujutsu project agreed with [GitButler](http://gitbutler.com/) to
standardize on storing change ID's as a Git commit header called `change-id`
where the [change ID is a 32 character reverse-hex
ID](https://jj-vcs.github.io/jj/latest/glossary/#change-id) (e.g.
`mlqnqnkrxpuvuuxzlzoltostwlwyskpx`). The change ID's are reverse-hex ID's so
that they can be easily distinguished from commit SHA1's. The Jujutsu team
reached out to us, the Gerrit Code Review project, to see whether we can support
these kind of change ID's too.

The main benefits we're hoping for are:

* Our tools become somewhat interoperable. People using Gerrit, Jujutsu and
  GitButler will be able to talk about the same Change ID and refer to them with
  their preferred tools locally.

* Standardization could bring momentum that convinces other projects to jump on
  the Change ID train:

  * Git forges (github, gitlab, forgejo) could use it to improve their code
    review tools.

  * Git itself could be convinced to set this commit header. It doesn't have to
    do anything with it (at first), but it will benefit users who interact with
    tools that read it. In particula `git rebase` could preserve the `change-id`
    header (which it currently doesn't).

## <a id="resources"> Resources

* Pull request that implements change IDs as Git commit headers in Jujutsu:
  https://github.com/jj-vcs/jj/pull/6162

