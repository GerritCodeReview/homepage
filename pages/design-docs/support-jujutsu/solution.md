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

## <a id="detailed-design"> Detailed Design

* When a commit is pushed for review, Gerrit reads the Change-Id from the
  `change-id` commit header if no `Change-Id` footer is present in the commit
  message.

  * A change can either have a Jujutsu change ID or a Gerrit Change-Id, but not
    both.

  * If an uploaded commit has both change ID's, the Gerrit Change-Id from the
    commit message footer takes precedence. This ensures that changes that have
    a Gerrit Change-Id can be reworked/rebased/cherry-picked locally by users
    that use Jujutsu. Jujutsu preserves the Gerrit Change-Id in the commit
    message, but may generate a new Jujutsu change ID when the `change-id`
    commit header is missing, so that the commit then has both change ID's. By
    giving precedence to the Gerrit Change-Id from the commit message footer
    uploading such commits from Jujutsu will update the existing change (the one
    identified by the Gerrit Change-Id from the commit message footer).

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

* Jujutsu preserves the `change-id` commit header on cherry-pick:

  The Jujutsu team intends to an option to their `duplicate` command that lets
  users control if they want a new change ID or the old one. This way users are
  in control to preserve the change ID when cherry-picking changes to other
  branches in Jujutsu.

* When a change that has a Jujutsu change ID is reverted through the Gerrit API
  Gerrit creates the revert change with a Jujutsu change ID.

* A new host and project configuration parameter controls whether Gerrit should
  require Gerrit Change-Id's in commit message footers, and ignore Jujutsu
  change ID's in commit headers. Since changes that have a Jujutsu change ID
  cannot easily be reworked/rebased/cherry-picked by users that use native Git
  (see [below](#compatibility)) teams may decide to require Gerrit Change-Id's
  so that they don't need to deal with the problems that this limitation causes
  (but then contributors cannot use Jujutsu without inserting Gerrit Change-Id's
  into their commit messages). By default, Gerrit Change-Id's are required.

* A new host and project configuration parameter controls whether changes that
  are created through the Gerrit API (e.g. via the [Create
  Change](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#create-change)
  REST endpoint) should be created with a Jujutsu change ID or a Gerrit
  Change-Id. By default, changes are created with Gerrit Change-Id's.

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

* Show a warning in the download dialog when a change has a Jujutsu change ID
  and hence cannot be reworked/rebased/cherry-picked in Git (see
  [below](#compatibility)).

  * [Optional] Skip showing the warning to Jujutsu users (we may know this from
    the changes that they have uploaded before).

* [Optional] Add a field for the change ID type (e.g. `I_HASH` vs.
  `REVERSE_HEX_ID`) and for the change ID location (e.g. `CHANGE_ID_FOOTER` vs.
  `CHANGE_ID_HEADER`) to
  [ChangeInfo](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info)
  and the change index. This allows the Gerrit UI and other callers to know if a
  change was created from Git or Jujutsu. Exposing this information might also
  be useful to gather statistics on how many changes are created from Git vs.
  Jujutsu.

## <a id="alternatives-considered"> Alternatives Considered

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

* Manipulate the download commands that are provided on the change screen to let
  user fetch an amended commit, a commit that has the Jujutsu change ID from the
  commit header copied as a `Change-Id` footer in the commit message (only if
  the change doesn't have a change ID as a footer yet).

  * This is not easily possible. We cannot magically replace the commit that is
    returned when the change ref is fetched, but we can only provide a command
    that fetches an alternative ref, but then we would need to create that ref
    and make it point to the amended commit. We already have a problem with
    creating too many refs, so we wouldn't like to create additional refs.

  * Returning an amended commit instead of the original commit is problematic.
    For example, if a user fetches a change of another user in order to make a
    new change that is based on the change of the other user, then on push the
    new commit would be based on the amended commit which is not a patch set of
    any change. Fixing that (e.g. recognize that the base change is the amended
    version of an existing change and rebase the new commit onto the original
    commit) is error-prone and adds too much complexity.

* On cherry-pick store information about the source change in NoteDb (when the
  cherry-pick is done via the Gerrit API or by push from a Git client we know
  the source change from the Gerrit Change-Id, when a cherry-pick is done in
  Jujutsu Jujutsu considered to record the source commit in a Git commit header
  that we could read on push). The recorded information could be used to track
  cherry-picks across branches.

  * Tracking cherry-picks separately is needed if Jujutsu doesn't preserve the
    change ID on cherry-pick. When discussing the idea of supporting change ID's
    in Git, it was concluded that Git should preserve the change ID on
    cherry-pick (see [below](#git-does-not-preserve-jj-change-ids)). To align
    with this Jujutsu intends to an option to their `duplicate` command that
    lets users control if they want a new change ID or the old one. This way
    Jujutsu users can preserve the change ID on cherry-pick and tracking
    cherry-picks separately in Gerrit is not needed.

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

1. [OK] Rework a change or change series in Jujutsu that was uploaded from Git:

   If changes were uploaded from Git they have a commit message footer with a
   Gerrit Change-Id, but no header with a Jujutsu change ID.

   Reworkig a change or change series in Jujutsu preserves the commit message
   including the Change-Id footer. Jujutsu may find that `change-id` headers are
   missing and add them with a newly generated change ID. Since Gerrit gives
   precedence to change ID's in commit message footers the correct changes get
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

* [PREFERRED SOLUTION] If Git would preserve the `change-id` commit header, that
  would solve the problem. The Jujutsu team has reached out to the Git team and
  it seems they agree to preserving the `change-id` header on rebase and
  cherry-pick (see [below](#git-does-not-preserve-jj-change-ids)).

* [SAVE DEFAULT] By default Gerrit Change-Id's are required. If teams do not
  configure their hosts or projects to use Jujutsu change ID's when a Gerrit
  Change-Id is not provided, these issues cannot happen for them, but then
  contributors also cannot use Jujutsu without inserting Gerrit Change-Id's into
  their commit messages.

* [BEST MITIGATION] The first step for human users to rework/rebase/cherry-pick
  a change from someone else is to fetch it from Gerrit. For this users copy a
  download command from the Gerrit change screen. We show a warning here when
  the change was uploaded from Jujutsu saying that Jujutsu must be used to
  rework/rebase/cherry-pick it.

* [BEST MITIGATION] The first step for human users to rework/rebase/cherry-pick
  a change from someone else is to fetch it from Gerrit. For this users copy a
  download command from the Gerrit change screen. We could change the commands
  there or add new ones if we find a command that mitigates the issues.

  * For example Matthias Sohn suggested the following command which amends the
    fetched commit locally to copy the Jujutsu change ID from the commit header
    to the `Change-Id` footer:

    ```
    git fetch https://gerrit.googlesource.com/homepage refs/changes/87/464287/6 \
      && git checkout -b change-464287 FETCH_HEAD \
      && git log -1 --format=%B \
      | git interpret-trailers --if-missing --trailer="Change-Id: mlqnqnkrxpuvuuxzlzoltostwlwyskpx" \
      | git commit --amend --no-edit -m "$(cat -)" \
      || echo "Error amending commit with jj Change-Id"
    ```

    > Note: Depending on their use case users need to use a download command
    > that fetches the original commit (to push a follow-up change) or the
    > amended commit (to rework/rebase/cherry-pick the change). We would need to
    > explain that in the Downloads commands popoup.

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

At the moment Git does not preserve the `change-id` commit header on rebase and
cherry-pick. Due to this changes that have a Jujutsu change ID cannot be
reworked/rebased/cherry-picked locally by users that use native Git (see
[above](#compatibility).

> Note: This limitation also means that at the moment it's not an option for
> Gerrit to adopt change ID's in Git headers regardless of the client (and drop
> Gerrit Change-Id's in commit message footers completely).

The Jujutsu team has reached out to the Git team to ask them if they would
consider changing this (see
[discussion thread](https://lore.kernel.org/git/Z_OGMb-1oV0Ex05e@pks.im/T/#m038be849b9b4020c16c562d810cf77bad91a2c87)).
The conclusion seems to be that the Git team is open to support a `change-id`
commit header that is preserved on rebase and cherry-pick (see this
[summary](https://lore.kernel.org/git/Z_OGMb-1oV0Ex05e@pks.im/T/#m2e6a57d8aeefd3146c7632e89dc36e2a0a8f68ba)).
This means that the behaviour for change ID's in Git would be the exactly the
same as it is for Gerrit Change-Id footers today (they are preserved on amend,
rebase and cherry-pick). This solves the [compatibility issues](#compatibility)
for us.

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

