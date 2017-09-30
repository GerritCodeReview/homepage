# Reviewing Changes

This is a Gerrit guide that is dedicated to Gerrit end-users. It explains the
standard Gerrit workflows and how a user can adapt Gerrit to personal
preferences.

It is expected that readers know about [Git](http://git-scm.com/) and that they
are familiar with basic git commands and workflows.

## Review Change

After [uploading a change for review](#upload-change) reviewers can inspect it
via the Gerrit web UI. Reviewers can see the code delta and [comment directly in
the code](user-review-ui.html#inline-comments) on code blocks or lines. They can
also [post summary comments and vote on review
labels](user-review-ui.html#reply). The [documentation of the review
UI](user-review-ui.html) explains the screens and controls for doing code
reviews.

There are several options to control how patch diffs should be rendered. Users
can configure their preferences in the [diff
preferences](user-review-ui.html#diff-preferences).

## Watching Projects

To get to know about new changes you can [watch the
projects](user-notify.html#user) that you are interested in. For watched
projects Gerrit sends you email notifications when a change is uploaded or
modified. You can decide on which events you want to be notified and you can
filter the notifications by using [change search expressions](user-search.html).
For example *`branch:master file:^.*\.txt$`* would send you email notifications
only for changes in the master branch that touch a *txt* file.

It is common that the members of a project team watch their own projects and
then pick the changes that are interesting to them for review.

Project owners may also configure [notifications on
project-level](intro-project-owner.html#notifications).

## Adding Reviewers

In the [change screen](user-review-ui.html#reviewers) reviewers can be added
explicitly to a change. The added reviewer will then be notified by email about
the review request.

Mainly this functionality is used to request the review of specific person who
is known to be an expert in the modified code or who is a stakeholder of the
implemented feature. Normally it is not needed to explicitly add reviewers on
every change, but you rather rely on the project team to watch their project and
to process the incoming changes by importance, interest, time etc.

There are also [plugins which can add reviewers
automatically](intro-project-owner.html#reviewers) (e.g. by configuration or
based on git blame annotations). If this functionality is required it should be
discussed with the project owners and the Gerrit administrators.

## Submit a Change

Submitting a change means that the code modifications of the current patch set
are applied to the target branch. Submit requires the
[Submit](access-control.html#category_submit) access right and is done on the
change screen by clicking on the [Submit](user-review-ui.html#submit) button.

In order to be submittable changes must first be approved by [voting on the
review labels](user-review-ui.html#vote). By default a change can only be
submitted if it has a vote with the highest value on each review label and no
vote with the lowest value (veto vote). Projects can configure [custom
labels](intro-project-owner.html#labels) and [custom submit
rules](intro-project-owner.html#submit-rules) to control when a change becomes
submittable.

How the code modification is applied to the target branch when a change is
submitted is controlled by the [submit
type](project-configuration.html#submit_type) which can be [configured on
project-level](intro-project-owner.html#submit-type).

Submitting a change may fail with conflicts. In this case you need to
[rebase](#rebase) the change locally, resolve the conflicts and upload the
commit with the conflict resolution as new patch set.

If a change cannot be merged due to path conflicts this is highlighted on the
change screen by a bold red `Cannot Merge` label.

## Rebase a Change

While a change is in review the HEAD of the target branch can evolve. In this
case the change can be rebased onto the new HEAD of the target branch. When
there are no conflicts the rebase can be done directly from the [change
screen](user-review-ui.html#rebase), otherwise it must be done locally.

**Rebase a Change locally.**

      // update the remote tracking branches
      $ git fetch

      // fetch and checkout the change
      // (checkout command copied from change screen)
      $ git fetch https://gerrithost/myProject refs/changes/74/67374/2 && git checkout FETCH_HEAD

      // do the rebase
      $ git rebase origin/master

      // resolve conflicts if needed and stage the conflict resolution
      ...
      $ git add <path-of-file-with-conflicts-resolved>

      // continue the rebase
      $ git rebase --continue

      // push the commit with the conflict resolution as new patch set
      $ git push origin HEAD:refs/for/master

Doing a manual rebase is only necessary when there are conflicts that cannot be
resolved by Gerrit. If manual conflict resolution is needed also depends on the
[submit type](intro-project-owner.html#submit-type) that is configured for the
project.

Generally changes shouldn’t be rebased without reason as it increases the number
of patch sets and creates noise with notifications. However if a change is in
review for a long time it may make sense to rebase it from time to time, so that
reviewers can see the delta against the current HEAD of the target branch. It
also shows that there is still an interest in this change.

> **Note**
>
> Never rebase commits that are already part of a central branch.

## Ignoring and Muting Changes

Changes can be ignored, which means they will not appear in the *Incoming
Reviews* dashboard and any related email notifications will be suppressed. This
can be useful when you are added as a reviewer to a change on which you do not
actively participate in the review, but do not want to completely remove
yourself.

Alternatively, rather than completely ignoring the change, it can be muted.
Muting a change means it will always be marked as "reviewed" in dashboards,
until a new patch set is uploaded.
