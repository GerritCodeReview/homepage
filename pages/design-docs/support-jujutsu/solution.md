---
title: "Design Doc - Support posting changes from Jujutsu - Solution"
permalink: design-docs/support-jujutsu-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution

## <a id="overview"> Overview

* Gerrit detects Jujutsu change ID's in Git commit headers when commits are
  uploaded for review. The Jujutsu change ID is used as the Change-Id to
  identify changes in Gerrit.

* Gerrit preserves Jujutsu change ID's when rewriting commits.

* On cherry-pick Gerrit stores the information about the source change in
  NoteDb. This information is used to track cherry-picks across branches.

## <a id="detailed-design"> Detailed Design

* When a commit is pushed for review, Gerrit reads the Change-Id from the
  `change-id` commit header. If no `change-id` commit header is present, Gerrit
  reads the Change-Id from the `Change-Id` commit message footer.

* A change can either have a Jujutsu change ID or a Gerrit Change-Id, but not
  both.

* If an uploaded commit has both change ID's, the Gerrit Change-Id from the
  commit message footer takes precedence. This ensures that changes that have a
  Gerrit Change-Id can be reworked/rebased/cherry-picked locally by users that
  use Jujutsu. Jujutsu preserves the Gerrit Change-Id in the commit message, but
  generates a new Jujutsu change ID when the `change-id` commit header is
  missing, so that the commit then has both change ID's. By giving precedence to
  the Gerrit Change-Id from the commit message footer uploading such commits
  from Jujutsu will update the existing change (the one identified by the Gerrit
  Change-Id from the commit message footer).

* Gerrit accepts Jujutsu change ID's (that are a 32 character reverse-hex ID,
  e.g. `mlqnqnkrxpuvuuxzlzoltostwlwyskpx`) if they are provided as `Change-Id`
  footer in the commit message. This allows expert users that use native Git to
  copy Jujutsu change ID's from commit headers and insert them as footers into
  commit messages when reworking/rebasing/cherry-picking changes that only have
  a Jujutsu change ID. Note, this doesn't enable users that use native Git to be
  able to rework/rebase/chery-pick changes with a Jujutsu change ID with an
  acceptable user experience (see [below](#compatibility)), but it at least
  allows a manual workaround for users that are aware of the issue.

* The Jujutsu change ID is stored in the change metadata (in the change ref in
  NoteDb) the same way as the Gerrit Change-Id (in the `Change-id` footer).

* If needed, we can distinguish Jujutsu change ID's (32 character reverse-hex
  ID, e.g. `mlqnqnkrxpuvuuxzlzoltostwlwyskpx`) from Gerrit Change-Id's (I-hash,
  e.g. `I03b7960b44545e9f30b61fc2c63846595fd84434`) by looking at the format of
  the change ID.

* Gerrit supports Jujutsu change ID's at all places where Gerrit Change-Id's
  (I-hashes) can be used:

  * In the code we use `String` as datatype for Change-ID's. This means, most
    of the codebase does not need to be adapted to work with Jujutsu change
    ID's.

  * Gerrit accepts Jujutsu change ID's as a
    [change identifier](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-id)
    in the REST API:

    * `<jj-change-id>`, if it uniquely identifies one change (since the Jujutsu
      change ID is a 32 character reverse-hex ID it can be easily distinguished
      from other change identifiers like change numbers or commit SHA1's).

    * `<project>~<branch>~<jj-change-id>` as a unique identifier for changes
      (similar to `<project>~<branch>~<Gerrit-Change-Id>`)

* Gerrit preserves Jujutsu change ID's when a new patch set is created on server
  side (e.g. when creating a new patch set via online edit, rebasing, by
  applying fixes or during submit).

* When a change that has a Jujutsu change ID is cherry-picked through the Gerrit
  API Gerrit generates a new Jujutsu change ID for the cherry-pick change (to be
  consistent with cherry-picks that are done in Jujutsu where the change ID is
  not preserved).

* When a change that has a Jujutsu change ID is cherry-picked through the Gerrit
  API Gerrit records the source change (and maybe patchset) in NoteDb. If a
  cherry-pick change is cherry-picked we may record the original source change.

* When a change is cherry-picked in Jujutsu Jujutsu records the source commit in
  a Git commit header. On upload Gerrit reads the information from this header
  and uses it to lookup the source change to record it in NoteDb.

* We use the information about the source change that is recorded for
  cherry-pick changes to populate the `Cherry picks` section on the change
  screen and to allow querying all cherry-picks of a change (allows to check in
  which branches a change is contained).

* When a change that has a Jujutsu change ID is reverted through the Gerrit API
  Gerrit creates the revert change with a Jujutsu change ID.

* A new project configuration parameter controls whether changes that have a
  Jujutsu change ID are accepted on upload. Since changes that have a Jujutsu
  change ID cannot easily be reworked/rebased/cherry-picked by users that use
  native Git (see [below](#compatibility)) teams may decide to not accept
  changes with Jujutsu change ID's so that they don't need to deal with the
  problems that this limitation causes (but then contributors cannot use
  Jujutsu).

* A new project configuration parameter controls whether changes that are
  created through the Gerrit API (e.g. via the [Create
  Change](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#create-change)
  REST endpoint) should be created with a Jujutsu change ID or a Gerrit
  Change-Id.

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

## <a id="alternatives-considered"> Alternatives Considered

* Jujutsu preserves the `change-id` commit header on cherry-pick:

  Rejected by the Jujutsu team as they prefer change ID's to uniquely identify
  one change/review.

* Have a 2-part change ID where the first part is preserved on cherry-pick and
  the second part is unique:

  Having a dedicated commit header to track the source of a cherry-pick looks
  like a cleaner solution.

* Let users use `git cherry-pick -x` to do cherry-picks locally to include
  "(cherry picked from commit ...)" into the commit message footer section and
  then make Gerrit parse this information from there on upload:

  Discarded as it's not as nice as what we have now because it means people need
  to remember to use this option (now it just works unless users take action and
  remove the Change-Id) and we would need to add logic to parse this information
  from the commit message (looks error-prone).

* Disallow pushing the same commit twice, for inclusion into different branches:

  This would ensure that Jujutsu change ID's always uniquely identify a single
  change/review, but it doesn't buy us much since Jujutsu cannot rely on servers
  to always ensure the uniqueness of change ID's, so in any case Jujutsu needs
  to be able to handle ambiguous change ID's.

* Allow changes to have a Jujutsu change ID and a Gerrit Change-Id at the same
  time:

  This would complicate the implementation quite a lot, since we would need an
  additional field to store the Jujutsu change ID (rather than just storing it
  in the existing field that we use for the Gerrit Change-Id). It's also unclear
  which benefits this would have.


## <a id="compatibility"> Compatibility between users that use native Git and users that use Jujutsu

### Rework changes of other users

In Gerrit it's possible that users upload patch sets to changes of other users.

One use case here is to take over a change when the original author is
unavailable (e.g. they already left from work or they are on vacation). This is
normally not about making substantial modifications, but only about doing some
minor fix-ups (e.g. fix some spelling mistakes to unblock the submission). In
this case the original author stays the Git author (that gets the credits for
the change) and the person reworking the change becomes the Git committer.

Whether it's allowed to add patch sets to changes of other users is controlled
by the
[Add Patch Set](https://gerrit-review.googlesource.com/Documentation/access-control.html#category_add_patch_set)
permission. Teams may not grant this permission. In this case reworking changes
of other users is not possible and the considerations discussed here do not
apply.

When users are allowed to upload patch sets to changes of other users, there is
the question what happens when changes were uploaded by a user that uses Jujutsu
and a user that uses native Git attempts to rework them, or vice versa:

1. [OK] Rework a change in Git that was uploaded from Jujutsu:

   If a change was uploaded from Jujutsu it has a `change-id` commit header with
   a Jujutsu change ID, but not a commit message footer with a Gerrit Change-Id.

   Reworking a change is done by amending the commit. Since `git commit --amend`
   preserves unknown commit headers the `change-id` header with the Jujutsu
   change ID stays intact and Gerrit will update the correct change on push.

1. [OK] Rework a change in Jujutsu that was uploaded from Git:

   If a change was uploaded from Git it has a commit message footer with a
   Gerrit Change-Id, but no header with a Jujutsu change ID.

   Reworking a change is done by amending the commit. Since `git commit --amend`
   preserves the commit message including the Change-Id footer the Gerrit
   Change-ID stays intact. Jujutsu may find that a `change-id` header is missing
   and add one with a newly generated change ID. Since Gerrit gives precedence
   to change ID's in commit message footers the correct change gets updated on
   push (and the newly generated change ID in the `change-id` header is
   ignored).

1. [NOT OK] Rework a change series in Git that was uploaded from Jujutsu:

   If a change series was uploaded from Jujutsu the changes have `change-id`
   commit headers, but no commit message footers with Gerrit Change-Id's.

   Reworking a change series is done by doing an interactive rebase. Depending
   on the actions that are done in the interactive rebase the Jujutsu change
   ID's may or may not be preserved. For example, if a change series consists
   out of a parent and a child, and the parent commit gets reworded, then the
   change ID is preserved for the parent (since rewording is done by amending
   the commit which preserves unknown commit headers) but the change ID for the
   child is lost (since it is rebased onto the amended parent commit and rebase
   doesn't perserve unknown commit headers).

   If a change ends up without a change ID it will be rejected by Gerrit on
   upload. In this case it's hard for users to understand the situation, find
   the correct Change ID's and include them into the correct commit messages (by
   doing another interactive rebase).

   Even worse when a commit is first rebased (drops the `change-id` header) and
   then amended the `commit-msg` hook would insert a newly generated Gerrit
   Change-Id as a commit message footer. On push this would lead to the creation
   of new changes, instead of updating the existing changes.

1. [OK] Rework a change series in Jujutsu that was uploaded from Git:

   If a change series was uploaded from Git the changes have commit messages
   footers with Gerrit Change-Id's, but no `change-id` commit headers.

   Reworking a change series is done by doing an interactive rebase. Since the
   actions in an interactive rebase preserve the commit messages, the Gerrit
   Change-Id's stay intact. Jujutsu may find that `change-id` headers are
   missing and add them with newly generated change ID's. Since Gerrit gives
   precedence to change ID's in commit message footers the correct changes gets
   updated on push (and the newly generated change ID's in the `change-id`
   headers are ignored).

### Rebase changes of other users

In Gerrit it's possible that users upload patch sets to changes of other users.

One use case here is to rebase a change when the original author is unavailable
(e.g. they already left from work or they are on vacation) to resolve conflicts
and make it submittable.

Whether it's allowed to add patch sets to changes of other users is controlled
by the
[Add Patch Set](https://gerrit-review.googlesource.com/Documentation/access-control.html#category_add_patch_set)
permission. Teams may not grant this permission. In this case rebasing changes
of other users via git push is not possible and the considerations discussed
here do not apply.

When users are allowed to upload patch sets to changes of other users, there is
the question what happens when changes were uploaded by a user that uses Jujutsu
and a user that uses native Git attempts to rebase them, or vice versa:

1. [NOT OK] Rebase a change in Git that was uploaded from Jujutsu:

   If a change was uploaded from Jujutsu it has a `change-id` commit header with
   a Jujutsu change ID, but not a commit message footer with a Gerrit Change-Id.

   Rebasing commits in Git doesn't preserve unknown headers (see
   [below](#git-does-not-preserve-jj-change-ids)). This means the Jujutsu change
   ID gets lost on rebase.

   If a change ends up without a change ID it will be rejected by Gerrit on
   upload. In this case it's hard for users to understand the situation, find
   the correct Change ID's and include them into the correct commit messages (by
   doing an interactive rebase).

   Even worse when a commit is first rebased (drops the `change-id` header) and
   then amended the `commit-msg` hook would insert a newly generated Gerrit
   Change-Id as a commit message footer. On push this would lead to the creation
   of new changes, instead of updating the existing changes.

1. [OK] Rebase a change in Jujutsu that was uploaded from Git:

   If a change was uploaded from Git it has a commit message footer with a
   Gerrit Change-Id, but no header with a Jujutsu change ID.

   Rebasing preserves the commit message including the Change-Id footer, so the
   Gerrit Change-ID's stay intact. Jujutsu may find that `change-id` headers are
   missing and add them with a newly generated change ID's. Since Gerrit gives
   precedence to change ID's in commit message footers the correct changes get
   updated on push (and the newly generated change ID's in the `change-id`
   headers are ignored).

### Cherry-pick changes of other users

It's possible that users cherry-pick changes of other users to other branches.

When this is done, there is the question what happens when changes were uploaded
by a user that uses Jujutsu and a user that uses native Git attempts to
cherry-pick them, or vice versa:

1. [NOT OK] Cherry-pick a change in Git that was uploaded from Jujutsu:

   If a change was uploaded from Jujutsu it has a `change-id` commit header with
   a Jujutsu change ID, but not a commit message footer with a Gerrit Change-Id.

   Cherry-picking commits in Git doesn't preserve unknown headers (see
   [below](#git-does-not-preserve-jj-change-ids)). This means the Jujutsu change
   ID gets lost on cherry-pick.

   If a change ends up without a change ID it will be rejected by Gerrit on
   upload. In this case it's hard for users to understand the situation, find
   the correct Change ID and include it into the commit messages (by amending
   the cherry-pick commit).

   Even worse when a commit is first cherry-picked (drops the `change-id`
   header) and then amended the `commit-msg` hook would insert a newly generated
   Gerrit Change-Id as a commit message footer. On push this would lead to the
   creation of new change that is not tracked as a cherry-pick of the original
   change and users would probably not notice this. As the result the list of
   cherry-picks shown in the UI and the results when querying for cherry-picks
   would be incomplete.

1. [OK] Cherry-picking a change in Jujutsu that was uploaded from Git:

   If a change was uploaded from Git it has a commit message footer with a
   Gerrit Change-Id, but no header with a Jujutsu change ID.

   Cherry-picking preserves the commit message including the Change-Id footer,
   so the Gerrit Change-ID's stay intact. Jujutsu may find that a `change-id`
   header is missing and add one with a newly generated change ID's. Since
   Gerrit gives precedence to change ID's in commit message footers the correct
   change get updated on push (and the newly generated change ID in the
   `change-id` header is ignored).

### Summary

* [OK] Reworking/rebasing/cherry-picking changes in Jujutsu that have been
  uploaded from Git works fine.

* [NOT OK] Reworking/rebasing/cherry-picking changes in Git that have been
  uploaded from Jujutsu is problematic.

Thoughts on addressing/mitigating this:

* [PREFERRED] If Git would preserve unknown commit headers, or at least the
  `change-id` commit header, that would solve the problem. The Jujutsu team
  intends to reach out to the Git team to see if they can be convinced to change
  this.

* Teams can configure their projects to not accept Jujutsu change ID's, then
  these issues cannot happen for them, but then contributors also cannot use
  Jujutsu.

* Teams that disallow uploading patch sets to changes of other users are less
  affected since reworking/rebasing changes of other users is not possible, but
  they may face the problem with cherry-picking.

* Teams may decide to adopt Jujutsu all together. Then they are not affected,
  assuming that drive by contributors neither upload patch sets to changes of
  other users nor do cherry-picks.

* Cherry-picking is mostly done by experienced team members. They may be aware
  of this issue and may be OK with always using Jujutsu for cherry-picking.

* When changes without a change ID are pushed to Gerrit, Gerrit rejects the push
  and returns an error message. We could say something useful in the error
  message that helps users to restore the correct Change-Id.

* The first step for human users to rework/rebase/cherry-pick a change from
  someone else is to fetch it from Gerrit. For this users copy a download
  command from the Gerrit change screen. We could show a warning here when the
  change was uploaded from Jujutsu saying that Jujutsu must be used to
  rework/rebase/cherry-pick it.

* The first step for human users to rework/rebase/cherry-pick a change from
  someone else is to fetch it from Gerrit. For this users copy a download
  command from the Gerrit change screen. We could change the commands there or
  add new ones if we find a command that mitigates the issues.

* Expert users may use `git cat-file` to inspect the commit headers after they
  have fetched a change that was created in Jujutsu into Git to learn about the
  change ID and then insert it manually into the commit message before they
  rework/rebase/cherry-pick it.

* Gerrit doesn't have the capability to send messages to the client when a
  change is fetched. If this was possible we could include a warning into the
  output when a users fetches a change that has a Jujutsu change ID.

* We discussed whether we could change the `commit_msg` hook to copy the change
  ID from the `change-id` commit header (if present) into the commit message as
  a `Change-Id` footer, but we found that this doesn't work (because the
  `commit_msg` hook only gets the path to a temporary file that contains the
  commit message written by the developer as an input and hence doesn't have
  access to the original commit) and also doesn't help (the `commit_msg` hook is
  not invoked on rebase or cherry-pick, but only when a commit is created or
  amended, and `git commit --amend` already preserves unknown commit headers).
  In addition, this would require all Gerrit users to update the hook for all
  their cloned repositories, which is hard to achieve.

## <a id="known-limitations"> Known Limitations

### <a id="git-does-not-preserve-jj-change-ids"> Native Git doesn't preserve Jujutsu change ID's on rebase and cherry-pick

Changes that have a Jujutsu change ID cannot be reworked/rebased/cherry-picked
locally by users that use native Git. This is because Git doesn't preserve the
`change-id` commit header on rebase and cherry-pick (the Jujutsu team intends to
reach out to the Git team to see if they can be convinced to change this). This
means at the moment it's not an option for Gerrit to adopt change ID's in Git
headers regardless of the client (and drop Gerrit Change-Id's in commit message
footers completely).

## <a id="implementation-plan"> Implementation Plan

Main tasks (not an exhaustive list):

* Extend JGit so that Gerrit can read/write arbitrary commit headers.
* Adapt Gerrit to read Change-Id's from commit headers.
* Adapt Gerrit to retain Change-Id's in commit headers when creating new patch
  sets.
* Support Jujutsu change ID's as change identifiers in the REST API.
* Store information about cherry-picks in NoteDb and use this information for
  tracking cherry-picks across branches.

## <a id="time-estimation"> Time Estimation

At this point no work on implementing this is planned yet. The Gerrit team at
Google may pick this up in Q3.

