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

* A new configuration parameter controls whether changes that are created
  through the Gerrit API (e.g. via the
  [Create Change](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#create-change)
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

## <a id="known-limitations"> Known Limitations

* Changes that have a Jujutsu change ID cannot be reworked/rebased/cherry-picked
  locally by users that use native Git (e.g. because Git doesn't preserve
  the `change-id` commit header on rebase, the Jujutsu team may reach out to the
  Git team to see if they can be convinced to change this). This means at the
  moment it's not an option for Gerrit to adopt change ID's in Git headers
  regardless of the client (and drop Gerrit Change-Id's in commit message
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

