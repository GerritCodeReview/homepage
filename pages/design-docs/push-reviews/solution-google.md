---
title: "Design Doc - Push Reviews: Solution proposed by Google"
permalink: design-docs/push-reviews-solution-google.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution proposed by Google

## <a id="objective"> Objective

The [use cases doc](/design-docs/push-reviews-use-cases.html) describes the
[the problems that we are trying to solve](/design-docs/push-reviews-use-cases.html#problem-statement) and
[the use cases that we are trying to address](/design-docs/push-reviews-use-cases.html#use-cases)
with this solution.


## <a id="design"> Design

* [Direct updates](/design-docs/push-reviews-use-cases.html#direct-updates) are
  pushed for review by using a new `push-review` push option.
* Pushing with the `push-review` option creates:
    * a merge commit that has
        * the same tree as the pushed commit
        * the tip of the target branch as the first parent commit
        * the pushed commit as the second parent commit
    * a change for the merge commit
* The created change has a flag that indicates it as push-review change.
* Looking at the change in the UI when selecting the first parent as base,
  reviewers see the diff between the content of the target branch at tip and
  the content of the pushed commit. This means reviewers can see what exactly is
  changing in the target branch by resetting it to the pushed commit.
* The diff against the AutoMerge base and the diff against the second parent
  commit are of no interest and may be hidden in the UI.
* [optional] Allow diffing against the merge base (common ancestor) of both
  commits.
* Submitting a push-review change requires the submitter to have the `Push`
  permission on the target branch.
* On submit of a push-review change the submit is processed by a new submit
  strategy that resets the target branch to the commit that was pushed (the
  second parent commit of the merge commit). This means the branch is reset to
  exactly the SHA1 of the pushed commit (even if it is a non-fast-forward update
  for the branch).
* Submitting a push-review change is not possible if the target branch has been
  updated since the change was created (tip of the target != first parent
  commit).
* Rebasing a push-review change is possible and replaces the first parent commit
  of the merge commit with the current tip of the target branch.
* [optional] Uploading a new patch sets is possible by doing another push with
  the `push-review` option that specifies the Change-Id of the push-review
  change as a value for the `push-review` option (`push-review=<Change-Id>`).
* [optional] Include a magic `COMMIT_LIST` file into push-review changes that
  lists the commmits that are added to history of the target branch and the
  commits that are removed from the history of the target branch by submitting
  this change (similar to the existing magic `MERGE_LIST` file that exists for
  merge changes).

