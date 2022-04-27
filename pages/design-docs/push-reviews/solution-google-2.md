---
title: "Design Doc - Push Reviews: Solution 2 proposed by Google"
permalink: design-docs/push-reviews-solution-google-2.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution 2 proposed by Google

## <a id="objective"> Objective

Address the [problems](/design-docs/push-reviews-use-cases.html#problem-statement)
and [use cases](/design-docs/push-reviews-use-cases.html#use-cases) through a
new `push-review` push option which creates a change for a push to a real
(non-magic/non-symbolic) ref. These "push-review changes" store the head at
upload time as the base commit for computing diffs in the change metadata to
make the push reviewable like any other Gerrit change. Submitting this change
sets the target branch to the pushed commit.

## <a id="design"> Design

The same as [solution 1](/design-docs/push-reviews-solution-google-1.html) but
with the following differences:

* Pushing with the `push-review` option creates a normal change that has the
  pushed commit as the patch set and that stores the head of the target branch
  at upload time as base commit in a new
  `refs/changes/\<sharded-change-ID\>/base` meta ref.
* Creating a ref for the base commit is necessary so that this commit is
  guarenteed to be still referenced from a ref after the push review change is
  submitted. Submitting a push review change may remove the base commit from the
  history of the target branch, and without the new
  `refs/changes/\<sharded-change-ID\>/base` meta ref it may become unreachable
  in this case, so that it would be garbage-collected at some point. This would
  break the acceptance criteria that requires the old SHA1 to stay available for
  auditing purposes.
* The new `refs/changes/\<sharded-change-ID\>/base` meta ref that stores the
  base commit is read whenever the change meta ref is read. For perfomance
  reasons we may store a flag in the change metadata to identify push review
  changes so that the `refs/changes/\<sharded-change-ID\>/base` meta ref only
  needs to be read for push review changes, and not for all changes.
* When the list of changed files is computed the stored base commit is used as
  the base for the comparison (`FileInfoJsonImpl` calls
  `DiffOperations#listModifiedFiles` with `oldCommit` = stored base commit if
  present).
* When a file diff is computed the stored base commit is used as the base for
  the comparison (when `PatchScriptFactory#create` is created with  `patchSetA`
  = null it uses the stored base commit if present).
* Disallow submit if the stored base commit doesn't match the current head of
  the target branch (submission requires a rebase that updates the stored base
  commit).
* The UI has a special visualization for push review changes so that users
  clearly understand that this change is applying a direct update. Note that the
  commit message is the one of the pushed commit and that there is no dedicated
  message explaining the direct update (also see [cons](#cons) section).

All the rest is the same as with
[solution 1](/design-docs/push-reviews-solution-google-1.html), in particular we
still add a new submit strategy that (re)sets the target branch to the pushed
commit that is applied when a push review change is submitted.

### <a id="pros-and-cons"> Pros & Cons

A quick summary of the pros and cons of this solution.

Pros:

* The patch set commit is the pushed commit:
    * Clients that fetch the commit get exactly the same commit to which the
      branch will be (re)set (same SHA1). This may matter for CI systems that
      expect to do verifications on the exact commit that is being submitted.
    * It's possible to have changes that depend on a push review change
      (successor changes) and submit them without needing to rebase them.

* Since push review changes are normal commits, not merge commits as with
  solution 1, we do not need special casing in the UI to hide the AutoMerge and
  the second parent commit in the base selection that are of no interest for
  push review changes.

<a id="cons">Cons:

* It's not possible to attach a message to the direct push to explain what the
  push is about (the shown commit message is the one of the pushed commit which
  cannot be altered as this would change the SHA1).
* Higher effort than implementing solution 1:
    * We must implement support for a new change meta ref which is expected to
      be a signifacant amount of extra work.
    * The UI must implement a special visualization for push review changes.
    * We need special casing when computing the file list and file diffs. The
      implementation looks quite straight-forward, but we need good test
      coverage for the new logic.
* Inventing a new change meta ref makes the storage scheme more complicated:
  The additional complexity means that the code gets more difficult to read and
  maintain and makes future extensions more difficult.
* All code that computes the list of changed files (via `DiffOperations`) must
  be aware of push reviews (including plugins, e.g. the `code-owners` plugin).
  It might be difficult to find all relevant places and make sure that new code
  doesn't forget about the push review case. To prevent this we may need to
  rework the `DiffOperations` API.

