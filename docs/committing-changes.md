# Committing Changes

This guide covers the common scenarios you might encounter as you create
and commit changes using Gerrit.

[TOC]

## Cloning a  Gerrit project

Cloning a Gerrit project is done the same way as cloning any other git
repository by using the `git clone` command.

**Clone Gerrit Project.**

      $ git clone ssh://gerrithost:29418/RecipeBook.git
      Cloning into RecipeBook...

The URL for cloning the project can be found in the Gerrit web UI under
`Projects` &gt; `List` &gt; &lt;project-name&gt; &gt; `General`.

For git operations Gerrit supports the
[SSH](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/user-upload.html#ssh) and the
[HTTP/HTTPS](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/user-upload.html#http) protocols.

> **Note**
>
> To use SSH you may need to [configure your SSH public key in your
> `Settings`](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/user-upload.html#ssh).

## Uploading a change

Uploading a change to Gerrit is done by pushing a commit to Gerrit. The commit
must be pushed to a ref in the `refs/for/` namespace which defines the target
branch: `refs/for/<target-branch>`. The magic `refs/for/` prefix allows Gerrit
to differentiate commits that are pushed for review from commits that are pushed
directly into the repository, bypassing code review. For the target branch it is
sufficient to specify the short name, e.g. `master`, but you can also specify
the fully qualified branch name, e.g. `refs/heads/master`.

**Push for Code Review.**

      $ git commit
      $ git push origin HEAD:refs/for/master

      // this is the same as:
      $ git commit
      $ git push origin HEAD:refs/for/refs/heads/master

**Push with bypassing Code Review.**

      $ git commit
      $ git push origin HEAD:master

      // this is the same as:
      $ git commit
      $ git push origin HEAD:refs/heads/master

> **Note**
>
> If pushing to Gerrit fails consult the Gerrit documentation that explains the
> [error messages](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/error-messages.html).

When a commit is pushed for review, Gerrit stores it in a staging area which is
a branch in the special `refs/changes/` namespace. A change ref has the format
`refs/changes/XX/YYYY/ZZ` where `YYYY` is the numeric change number, `ZZ` is the
patch set number and `XX` is the last two digits of the numeric change number,
e.g. `refs/changes/20/884120/1`. Understanding the format of this ref is not
required for working with Gerrit.

Using the change ref git clients can fetch the corresponding commit, e.g. for
local verification.

**Fetch Change.**

      $ git fetch https://gerrithost/myProject refs/changes/74/67374/2 && git checkout FETCH_HEAD

> **Note**
>
> The fetch command can be copied from the
> [download commands](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/user-review-ui.html#download)
> in the change screen.

The `refs/for/` prefix is used to map the Gerrit concept of "Pushing for Review"
to the git protocol. For the git client it looks like every push goes to the
same branch, e.g. `refs/for/master` but in fact for each commit that is pushed
to this ref Gerrit creates a new branch under the `refs/changes/` namespace. In
addition Gerrit creates an open change.

A change consists of a [Change-Id](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/user-changeid.html),
meta data (owner, project, target branch, and so on), one or more patch sets,
comments and votes. A patch set is a git commit. Each patch set in a change
represents a new version of the change and replaces the previous patch set. Only
the latest patch set is relevant. This means all failed iterations of a change
will never be applied to the target branch, but only the last patch set that is
approved is integrated.

The Change-Id is important for Gerrit to know whether a commit that is pushed
for code review should create a new change or whether it should create a new
patch set for an existing change.

The Change-Id is a SHA-1 that is prefixed with an uppercase `I`. It is specified
as footer in the commit message (last paragraph):

      Improve foo widget by attaching a bar.

      We want a bar, because it improves the foo by providing more
      wizbangery to the dowhatimeanery.

      Bug: #42
      Change-Id: Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b
      Signed-off-by: A. U. Thor <author@example.com>

If a commit that has a Change-Id in its commit message is pushed for review,
Gerrit checks if a change with this Change-Id already exists for this project
and target branch, and if yes, Gerrit creates a new patch set for this change.
If not, a new change with the given Change-Id is created.

If a commit without Change-Id is pushed for review, Gerrit creates a new change
and generates a Change-Id for it. Since in this case the Change-Id is not
included in the commit message, it must be manually inserted when a new patch
set should be uploaded. Most projects already
[require a Change-Id](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/project-configuration.html#require-change-id)
when pushing the very
first patch set. This reduces the risk of accidentally creating a new change
instead of uploading a new patch set. Any push without Change-Id then fails with
[missing Change-Id in commit message footer](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/error-missing-changeid.html).
New patch sets can always be uploaded to a specific change (even without
any Change-Id) by pushing to the change ref, for example,
`refs/changes/74/67374`.

Amending and rebasing a commit preserves the Change-Id so that the new commit
automatically becomes a new patch set of the existing change, when it is pushed
for review.

**Push new Patch Set.**

      $ git commit --amend
      $ git push origin HEAD:refs/for/master

Change-Ids are unique for a branch of a project. E.g. commits that fix the same
issue in different branches should have the same Change-Id, which happens
automatically if a commit is cherry-picked to another branch. This way you can
[search](user-search.html) by the Change-Id in the Gerrit web UI to find a fix
in all branches.

Change-Ids can be created automatically by installing the `commit-msg` hook as
described in the
[Change-Id documentation](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/user-changeid.html#creation).

Instead of manually installing the `commit-msg` hook for each git repository,
you can copy it into the [git template directory](http://git-scm.com/docs/git-init#_template_directory).
Then it is automatically copied to every newly cloned repository.

## Uploading a new patch set

If there is feedback from code review and a change should be improved a new
patch set with the reworked code should be uploaded.

This is done by amending the commit of the last patch set. If needed this commit
can be fetched from Gerrit by using the fetch command from the
[download
commands](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/user-review-ui.html#download)
in the change screen.

It is important that the commit message contains the
[Change-Id](https://gerrit-documentation.storage.googleapis.com/Documentation/2.14.5.1/user-changeid.html)
of the change that should be updated as a footer (last paragraph). Normally the
commit message already contains the correct Change-Id and the Change-Id is
preserved when the commit is amended.

**Push Patch Set.**

      // fetch and checkout the change
      // (checkout command copied from change screen)
      $ git fetch https://gerrithost/myProject refs/changes/74/67374/2 && git checkout FETCH_HEAD

      // rework the change
      $ git add <path-of-reworked-file>
      ...

      // amend commit
      $ git commit --amend

      // push patch set
      $ git push origin HEAD:refs/for/master

> **Note**
>
> Never amend a commit that is already part of a central branch.

Pushing a new patch set triggers email notification to the reviewers.

## Adding reviewers

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

## Submitting a change

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

## Rebasing a change

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

## Abandoning and restoring a change

Sometimes during code review a change is found to be bad and it should be given
up. In this case the change can be [abandoned](user-review-ui.html#abandon) so
that it doesn’t appear in list of open changes anymore.

Abandoned changes can be [restored](user-review-ui.html#restore) if later they
are needed again.

## Using topics

Changes can be grouped by topics. This is useful because it allows you to easily
find related changes by using the [topic search
operator](user-search.html#topic). Also on the change screen [changes with the
same topic](user-review-ui.html#same-topic) are displayed so that you can easily
navigate between them.

Often changes that together implement a feature or a user story are group by a
topic.

Assigning a topic to a change can be done in the [change
screen](user-review-ui.html#project-branch-topic).

It is also possible to [set a topic on push](user-upload.html#topic), either by
appending `%topic=...` to the ref name or through the use of the command line
flag `--push-option`, aliased to `-o`, followed by `topic=...`.

**Set Topic on Push.**

      $ git push origin HEAD:refs/for/master%topic=multi-master

      // this is the same as:
      $ git push origin HEAD:refs/heads/master -o topic=multi-master

## Using private changes

Private changes are changes that are only visible to their owners and reviewers.
Private changes are useful in a number of cases:

-   You want to check what the change looks like before formal review starts. By
    marking the change private without reviewers, nobody can prematurely comment
    on your changes.

-   You want to use Gerrit to sync data between different devices. By creating a
    private throwaway change without reviewers, you can push from one device,
    and fetch to another device.

-   You want to do code review on a change that has sensitive aspects. By
    reviewing a security fix in a private change, outsiders can’t discover the
    fix before it is pushed out. Even after merging the change, the review can
    be kept private.

To create a private change, you push it with the `private` option.

**Push a private change.**

      $ git commit
      $ git push origin HEAD:refs/for/master%private

The change will remain private on subsequent pushes until you specify the
`remove-private` option. Alternatively, the web UI provides buttons to mark a
change private and non-private again.

When pushing a private change with a commit that is authored by another user,
the other user will not be automatically added as a reviewer and must be
explicitly added.

For CI systems that must verify private changes, a special permission can be
granted ([View Private
Changes](access-control.html#category_view_private_changes)). In that case, care
should be taken to prevent the CI system from exposing secret details.

## Editing files inline

It is possible to [edit changes inline](user-inline-edit.html#editing-change)
directly in the web UI. This is useful to make small corrections immediately and
publish them as a new patch set.

It is also possible to [create new changes
inline](user-inline-edit.html#create-change).

## Replying by email

Gerrit sends out email notifications to users and supports parsing back replies
on some of them (when [configured](config-gerrit.html#receiveemail)).

Gerrit supports replies on these notification emails:

-   Notifications about new comments

-   Notifications about new labels that were applied or removed

While Gerrit supports a wide range of email clients, the following ones have
been tested and are known to work:

-   Gmail

-   Gmail Mobile

Gerrit supports parsing back all comment types that can be applied to a change
via the WebUI:

-   Change messages

-   Inline comments

-   File comments

Please note that comments can only be sent in reply to a comment in the original
notification email, while the change message is independent of those.

Gerrit supports parsing a user’s reply from both HTML and plaintext. Please note
that some email clients extract the text from the HTML email they have received
and send this back as a quoted reply if you have set the client to plaintext
mode. In this case, Gerrit only supports parsing a change message. To work
around this issue, consider setting a [User Preference](#email-format) to
receive only plaintext emails.

Example notification:

    Some User has posted comments on this change.
    (https://gerrit-review.googlesource.com/123123 )

    Change subject: My new change
    ......................................................................


    Patch Set 3:

    Just a couple of smaller things I found.

    https://gerrit-review.googlesource.com/#/c/123123/3/MyFile.java
    File
    MyFile.java:

    https://gerrit-review.googlesource.com/#/c/123123/3/MyFile@420
    PS3, Line 420:     someMethodCall(param);
    Seems to be failing the tests.


    --
    To view, visit https://gerrit-review.googlesource.com/123123
    To unsubscribe, visit https://gerrit-review.googlesource.com/settings

    (Footers omitted for brevity, must be included in all emails)

Example response from the user:

    Thanks, I'll fix it.
    > Some User has posted comments on this change.
    > (https://gerrit-review.googlesource.com/123123 )
    >
    > Change subject: My new change
    > ......................................................................
    >
    >
    > Patch Set 3:
    >
    > Just a couple of smaller things I found.
    >
    > https://gerrit-review.googlesource.com/#/c/123123/3/MyFile.java
    > File
    > MyFile.java:
    Rename this file to File.java
    >
    > https://gerrit-review.googlesource.com/#/c/123123/3/MyFile@420
    > PS3, Line 420:     someMethodCall(param);
    > Seems to be failing the tests.
    >
    Yeah, I see why, let me try again.
    >
    > --
    > To view, visit https://gerrit-review.googlesource.com/123123
    > To unsubscribe, visit https://gerrit-review.googlesource.com/settings
    >
    > (Footers omitted for brevity, must be included in all emails)

In this case, Gerrit will persist a change message ("Thanks, I’ll fix it."), a
file comment ("Rename this file to File.java") as well as a reply to an inline
comment ("Yeah, I see why, let me try again.").

