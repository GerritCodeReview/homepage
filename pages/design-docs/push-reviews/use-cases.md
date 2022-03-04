---
title: "Design Doc - Push Reviews - Use Cases"
permalink: design-docs/push-reviews-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/push-reviews
---

# Push Reviews - Use Cases

## <a id="objective">Objective

Enable code review for [direct updates](#direct-updates) (pushes that
update/reset the target branch directly to the pushed commit, including
non-fast-foward updates).

## <a id="background">Background

Gerrit's primary purpose is to support reviewing code changes, but there are
some updates (non-fast-forward updates, but also fast-forward updates to a
certain commit) that currently cannot be reviewed.

### <a id="direct-updates">Direct Updates

The term 'direct update' is understood to mean an update of a branch that sets
the branch to exactly the commit that was pushed by the user. This can be a
fast-forward update (the commit that was pushed is a successor of the head of
the target branch, aka 'git push <SHA1>:refs/heads/<branch>') but also a
non-fast-forward update (reset to an arbitrary commit, aka 'git push -f
<SHA1>:refs/heads/<branch>').

## <a id="problem-statement">Problem Statement

Having valid use-cases ([see below](#use-cases)) that require doing direct
updates with bypassing code review is a security problem because it means that
the involved users need to have permissions to do direct pushes. If their
account is compromised, an attacker could use these permissions to do malicious
updates without involving another person (also see the
[SLSA](https://slsa.dev/spec/v0.1/levels#what-is-slsa) [Two-Person Reviewed
requirement](https://slsa.dev/spec/v0.1/requirements#two-person-reviewed)).

Also during normal operations being able to review direct updates increases
safety, since reviews make erroneous updates less likely.

## <a id="use-cases">Use Cases

As a project owner I would like ...

* ... to rebase a series of internal patches on top of a branch that is
  fetched from an open-source project (when this branch has changed) ...
* ... to retroactively split up a repository (e.g. move a subfolder into a new
  repository while maintaining a rewriten history in both repositories) [1] ...
* ... to import arbitrary commits without changing the SHA1 (e.g. code drops
  that were received from external partners) ...

... without needing to bypass code review.

[1] requires using [git filter-repo](https://github.com/newren/git-filter-repo/)
to rewrite the history of the repository/branch.

As a user I would like ...

* ... to review [direct updates](#direct-updates).
* ... to inspect retroactively how a branch was changed by [direct
  updates](#direct-updates).

As an administrator I would like ...

* ... to be able to enforce code review for all updates without breaking uses
  cases that require project owners to do [direct updates](#direct-updates)
  today.
* ... to make sure that any commit that potentially went into a build of an
  artifact is preserved, so that any time it can be proved how binaries were
  made.

## <a id="non-goals">Non-Goals

* Support code review for updates that completely eliminate commits from the
  repository by erasing history (e.g. removing large files from the history of
  the repository, removing commits that have leaked data).
* Support GitHub-like pull requests.
* Support code review for branch creations (but push reviews may help
  implementing a workflow for this, see [below](how-to-review-branch-creations))

### <a id="how-to-review-branch-creation">Possible workflow to review branch creations with push reviews

While supporting code review for branch creations is not in scope of this
design, push reviews can help making branch creations reviewable. The envisioned
workflow is:

1. Create a branch with an initial empty commit.
2. Populate the branch with a push review.

1. currently requires doing a direct push, but it's intended to extend the
Create Branch REST endpoint so that it can create branches with an inital empty
commit (this feature is orthogonal to this design).

## <a id="acceptance-criteria">Acceptance Criteria

Reviewing [direct updates](#direct-updates) is possible:

* A direct update can be pushed for review.
* The change shows the diff between the head of the target branch and the pushed
  commit.
* Changes with large diffs are handled in an acceptable way, changes with
  unreasonable large diffs are rejected.
* Submitting a change that applies direct updates requires more/other
  permissions than submitting normal changes if the submission results in a
  non-fast-forward update.
* On submit of the change the target branch is set to the commit that has been
  pushed.
* The previous state of the branch is preserved for audit in the code review, so
  that users can inspect retroactively how the branch was changed.
* Previously merged changes and old patch sets stay intact when a push review
  has been submitted.
* Open changes show a conflict when a non-fast-forward push review has been
  submitted.
* Uploads of commits that are based on commits that have been removed from the
  branch history by the submission of a non-fast-forward push review are
  rejected unless they are push reviews themselves (this is to prevent that
  changes are accidentally created for all commits that have been removed from
  the history of the target branch).

