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
some updates (non-fast-forward updates) that currently cannot be reviewed.

### <a id="direct-updates">Direct Updates

The term 'direct update' is understood to mean an update of a branch that resets
the branch to exactly the commit that was pushed by the user. This can be a
fast-forward update (the commit that was pushed is a successor of the head of
the target branch) but also a non-fast-forward update (reset to an arbitrary
commit).

## <a id="problem-statement">Problem Statement

Having valid use-cases ([see below](#use-cases)) that require doing direct
updates with bypassing code review is a security problem because it means that
the involved users need to have permissions to do direct pushes. If their
account is compromised, an attacker could use these permissions to do malicious
updates without involving another person.

Also during normal operations being able to review direct updates increases
safety, since reviews make erroneous updates less likely.

## <a id="use-cases">Use Cases

As a project owner I would like ...

* ... to rebase a series of internal patches on top of a branch that is
  fetched from an open-source project (when this branch has changed) ...
* ... to split a repository into multiple repositories (e.g. move a
  subfolder into a new repository) [1] ...
* ... to import arbitrary code drops that were received from external
  partners ...

... without needing to bypass code review.

[1] requires using 'git filter-branch' to rewrite the history of the
repository/branch.

## <a id="acceptance-criteria">Acceptance Criteria

Reviewing [direct updates](#direct-updates) is possible:

* A direct update can be pushed for review.
* The change shows the diff between the head of the target branch and the pushed
  commit.
* Submitting a change that applies direct updates requires more/other
  permissions than submitting normal changes.
* On submit of the change the target branch is reset to the commit that has been
  pushed.
* The previous state of the branch is recorded for audit in the code review.

