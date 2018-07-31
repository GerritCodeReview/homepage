---
title: "Notedb"
permalink: notedb.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---


## What is notedb?

Notedb is the successor to ReviewDb: a replacement database backend for Gerrit.
The goal is to read code review metadata from the same set of repositories that
store the data. This allows for improved atomicity, consistency of replication,
and the creation of new features like federated review and offline review.

This document describes the state of migration (not necessarily completely up to
date), the tasks that remain, and notes on some of the challenges we've
encountered along the way. This document is **not** a full design document for
notedb; if you're that curious, bug dborowitz and he will help you out.

Finally, this document is for core developers. If you are a casual user of
Gerrit looking for documentation, you've come to the wrong place.

## Root Tables

While ReviewDb has a lot of tables, there are relatively few "root" tables, that
is, tables whose primary key's `get!ParentKey()` method returns null:

* **Change**: subtables ChangeMessage, PatchSet, PatchSetApproval,
  PatchSetAncestor, PatchLineComment, TrackingId
* **Account**: subtables AccountExternalId, AccountProjectWatch,
  AccountSshKey, AccountDiffPreference, StarredChange
* **AccountGroup**: subtables AccountGroupMember

TODO(dborowitz): Document other minor tables, audits, etc.

For each root entity in each of these tables, there is one DAG describing all
modifications that have been applied to the change over time. Entities DAGs are
stored in a repository corresponding to their function:

* **Change**: stored in `refs/changes/YZ/XYZ/meta` in the destination repository
* **Account**: stored in `refs/accounts/YZ/XYZ/meta` (TBD) in `All-Users`
* **AccountGroup**: stored in `TBD` in `All-Projects`

Most of this document focuses on Change entities, partly because it's the most
complex, but also because that's where most effort to date has been focused.

## Changes: What's Done

Current progress, along with some possibly-interesting implementation notes.

*   ChangeMessages: Stored in commit message body. Currently the subject of the
    commit message contains a machine-generated-but-readable summary like
    "Updated patch set 3"; we might decide to eliminate this and just use the
    ChangeMessage.
*   PatchSetApprovals: Stored as a footer "Label: Label-Name=Foo". Instead of
    storing an implicit 0 review for reviewers, include them explicitly in a
    separate Reviewer footer. Freeze labels at submit time along with the full
    submit rule evaluator results using "Submitted-with".
*   PatchLineComments: The only thing thus far actually stored in a note, on the
    commit to which it applies. Drafts are stored in a per-user ref in
    All-Users.
*   TrackingId: Killed this long ago and use the secondary index. (Just reminded
    myself I need to rip out the gwtorm entity.)
*   Change: Started storing obvious fields: owner, project, branch, topic.
*   PatchSet: Storing IDs and created on timestamps right now, not reading from
    it yet.

## Changes: What Needs to Be Done

*   PatchSetAncestors: Replace with a persistent cache, which should probably be
    rebuilt in RebuildNotedb.
*   PatchSet: Draft field. (Someday I think we should replace Draft with WIP,
    but I digress.)
*   Change: Kill more fields. Actually implement reading from changes; see
    challenges section.
*   Some sort of batch parser. If we get 100 changes back from a search,
    sequentially reading the DAG for each of those might take a while.
*   Benchmark and optimize the heck out of the parsers. Let's say a target is
    1ms per change DAG. Related, we may also need to disable (eager) parsing of
    certain fields, if we can prove with benchmarks that they are problematic.
    (We already do this for PatchLineComments, to avoid having to read anything
    but commits in the common case.)

## JGit Changes

*   Teach JGit to pack notedb refs in a separate pack file from everything else.
    We don't want to hurt locality within the main pack by interleaving metadata
    commits.
*   Teach JGit to better handle many small, separate commit graphs in the
    packer. Ordered chronologically, notedb metadata will be spread across a
    large number of separate DAGs. We will get better kernel buffer cache
    locality by clustering all commits in each disconnect DAG together. (But
    this may also hurt batch parsing; see above.)

## Challenges

TODO
