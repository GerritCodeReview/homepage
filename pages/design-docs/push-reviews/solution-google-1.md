---
title: "Design Doc - Push Reviews: Solution 1 proposed by Google"
permalink: design-docs/push-reviews-solution-google-1.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution 1 proposed by Google

## <a id="objective"> Objective

Address the [problems](/design-docs/push-reviews-use-cases.html#problem-statement)
and [use cases](/design-docs/push-reviews-use-cases.html#use-cases) through a
new `push-review` push option which creates a change for a push to a real
(non-magic/non-symbolic) ref. These "push-review changes" use an automatically
created merge commit as the patch set commit to make the push reviewable like
any other Gerrit change. Submitting this change sets the target branch to the
pushed commit.

## <a id="design"> Design

* [Direct updates](/design-docs/push-reviews-use-cases.html#direct-updates) are
  pushed for review by using a new `push-review` push option.
* Pushing with the `push-review` option creates:
    * a merge commit which is used to record the push review and that has
        * the same tree as the pushed commit
        * the tip of the target branch as the first parent commit
        * the pushed commit as the second parent commit
    * a change for the merge commit
* The created change has a flag that indicates it as push-review change.
* Looking at the change in the UI when selecting the first parent as base,
  reviewers see the diff between the content of the target branch at tip and
  the content of the pushed commit. This means reviewers can see what exactly is
  changing in the target branch by (re)setting it to the pushed commit.
* The diff against the AutoMerge base and the diff against the second parent
  commit are of no interest and may be hidden in the UI.
* [optional] Allow diffing against the merge base (common ancestor) of both
  commits.
* Submitting a push-review change requires the submitter to have the `Push`
  permission with the `force` flag on the target branch, even if the submission
  results in a fast-forward that only adds a single commit to the target branch
  (according to the
  [acceptance criteria](/design-docs/push-reviews-use-cases.html#acceptance-criteria)
  this is the only case that doesn't need to require special permissions, but in
  order to keep things simple we are not special casing this and just always
  require the submitter of push review changes to have the `Push` permission
  with the `force` flag).
* On submit of a push-review change the submit is processed by a new submit
  strategy that (re)sets the target branch to the commit that was pushed (the
  second parent commit of the merge commit). This means the branch is (re)set to
  exactly the SHA1 of the pushed commit (even if it is a non-fast-forward update
  for the branch).
* Submitting a push-review change is not possible if the target branch has been
  updated since the change was created (tip of the target != first parent
  commit). In this case the change shows a merge conflict. This is important
  since otherwise the approval is done for the old diff (pushed commit vs. head
  of the target branch at upload time) and any concurrent updates of the target
  branch would be lost unnoticed since they do not show up in the change diff.
* Rebasing a push-review change is possible and replaces the first parent commit
  of the merge commit with the current tip of the target branch.
* [optional] Uploading a new patch set is possible by doing another push with
  the `push-review` option that specifies the Change-Id of the push-review
  change as a value for the `push-review` option (`push-review=<Change-Id>`).
* [optional] Include a magic `COMMIT_LIST` file into push-review changes that
  lists the commits that are added to the history of the target branch and the
  commits that are removed from the history of the target branch by submitting
  this change (similar to the existing magic `MERGE_LIST` file that exists for
  merge changes).

### <a id="pros-and-cons"> Pros & Cons

A quick summary of the pros and cons of this solution.

Pros:

* Easy to implement:
  This design has the advantage that the backend implementation of push reviews
  is mostly limited to 2 places only: 1. interception of the push to create the
  merge commit and a patch set for it 2. addition of a new submit strategy that
  handles push review changes and sets the branch to the intended commit (second
  parent commit). All other things would then mostly work the same way as for
  normal merge changes (e.g. showing the diff).

Cons:

* The patch set commit is the merge commit and not the pushed commit:
    * The merge commit and the pushed commit have exactly the same content (same
      tree) but their commit IDs differ. This means when a client fetches the
      patch set it sees the commit ID of the merge commit and not the commit ID
      of not pushed commit. This may matter for CI systems that expect to do
      verifications on the exact commit that is being submitted (but the same
      problem already exists for the cherry-pick and rebase-if-necessary submit
      strategies).
    * This means it's not possible to have a change that depend on a push review
      change (successor change) and submit it without needing to rebase it. A
      possible use-case where this is important is applying an upstream vendor
      update (push review change) and a follow-up change that adapts internal
      code to fix build issues, in this case the CI system may like to verify
      and submit these changes together. Note, this is not a use-case that we
      are trying to support.

* Comparing push reviews against the AutoMerge base and against the second
  parent commit are of no interest:
  This means we need special casing in the UI to hide the AutoMerge and the
  second parent commit in the base selection.

### <a id="alternatives-considered"> Alternatives Considered

* Add a project level option that allows to configure a project to implicitly
  assume the `push-review` option for all direct pushes even if the client does
  not specify the `push-review` option.
    * This idea was discarded because enabling this option would mean that doing
      a `git push` will report success, although the update wasn't applied. This
      can cause confusion, especially for existing scripts that currently do
      force push + pull, as for these scripts the behavior would silently change
      by enabling this option.

* Prevent that the AutoMerge commit is being calculated for push reviews,
  assuming it is expensive to calculate. Since the comparison of a push review
  against its AutoMerge base is of no interest, it is not offered by the UI and
  hence computing the AutoMerge commit is unneeded.
    * This is a possible optimisation that we may want to do later (e.g. only
      when we observe that this is actually a performance issue).

* Require the client to use the `--force` option on git push when creating a
  push review change that will result in a non-fast-forward update on
  submission.
    * Doing this would mean that users need to have force push permissions in
      order to create non-fast-forward push reviews, but this would make it
      impossible allowing users to create such push reviews while at the same
      time disallowing them to do direct pushes.

