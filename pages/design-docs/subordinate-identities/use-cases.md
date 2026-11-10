---
title: "Design Doc - Subordinate Identities - Use Cases"
permalink: design-docs/subordinate-identities-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="definitions"> Definitions

* **Subordinate identity (subordinate):** An account that is created and owned
  by another account and that can never do more than its owner can.
* **Parent:** The account that owns a subordinate. A parent may itself be a
  subordinate.
* **Primary account (primary):** The non-subordinate account at the top of a
  chain of parents. Every subordinate has exactly one primary, which is the
  accountable party for everything its descendants do.
* **Family:** A primary and all of its descendants.
* **Scope:** The list of permissions a subordinate may exercise. The
  subordinate's effective permissions are the intersection of its scope with
  its parent's effective permissions, evaluated at request time.
* **Provenance annotation:** Optional, owner-supplied metadata on a subordinate
  (for example "agent" or "CI") that the UI may render next to its actions.

## <a id="background"> Background

Gerrit 3.13 replaced the single HTTP password with multiple named
authentication tokens with a lifetime. That design explicitly left limited
scope for a separate design document: every token still carries the full
permissions of its account.

In practice a user who wants to hand a credential to an automated process has
three options today, none of them good:

* Give it one of their own tokens. The process can then do anything the user
  can, including approving and submitting changes, and its actions are
  indistinguishable from the user's.
* Ask an administrator for a service account. This needs a human in the loop,
  the resulting account's permissions are unrelated to the requesting user's,
  and nothing ties it back to an accountable person.
* Use the `serviceuser` plugin. This is the closest existing fit, but creation
  is gated on a capability and admin-defined policy, ownership is by group
  rather than by a person, and permissions still have to be granted to the
  service user separately through groups.

The number of such processes per user is growing quickly. CI jobs that propose
changes have existed for years; coding and review agents now mean a single
developer may want several distinct, narrowly empowered actors.

## <a id="use-cases"> Use Cases

* As a regular user, I want to give a Zuul job a credential that can propose
  changes to a project, and I want to be certain that credential cannot vote
  on or submit them.
* As a regular user, I want to run a review agent that comments and votes
  under its own name, so its reviews are distinguishable from mine and it can
  be added to a change as a reviewer in its own right.
* As a regular user, I want to give a coding agent an identity that can upload
  and amend changes in two projects and nothing else.
* As an orchestrating agent that holds a subordinate identity, I want to
  create short-lived, further-restricted identities for the workers I spawn,
  and revoke them when they finish.
* As a user, when I lose access to a project, everything I delegated loses
  that access at the same moment without anyone having to clean up.
* As a user, I want to revoke one subordinate, and everything it created,
  without touching my other credentials.
* As a project owner, I do not want my project's history or change screens to
  advertise which tools a contributor used. I want to switch provenance
  annotations off for my project.
* As a project owner, I want my submit requirements ("two approvals", "not
  the uploader") to keep meaning two *people*, regardless of how many
  subordinates a person operates.
* As an administrator or auditor, I want to trace any action by a subordinate
  to the primary account that is responsible for it.

## <a id="acceptance-criteria"> Acceptance Criteria

* Any user who may create auth tokens may create subordinates, without
  administrator involvement, up to a configurable limit.
* A subordinate is a real account: it has an account ID, can own changes, be a
  reviewer, vote, comment, and hold auth tokens and SSH keys.
* A subordinate's effective permissions are never a superset of its parent's.
  This holds continuously, not only at creation time.
* A subordinate may create subordinates of its own if and only if its scope
  includes that permission; the same subset rule applies recursively.
* A subordinate cannot widen its own scope or modify any ancestor.
* Deactivating or deleting an account applies to all of its descendants.
* Submit requirements cannot be satisfied by combining votes from members of
  one family where they could not be satisfied by a single person.
* Provenance annotations are optional per subordinate, and can be suppressed
  per project (inherited through the project hierarchy).
* The primary of any subordinate is always recorded and available to
  administrators, regardless of display policy.
* Existing accounts, tokens and permission configuration are unaffected.

## <a id="out-of-scope"> Out Of Scope

* Restricting a scope to specific refs. The first version scopes by permission
  and by project. Ref patterns can be added to the same grammar later.
* Per-credential scopes (a single account with tokens of differing power).
  The scope grammar defined here could later be applied to an individual
  token, but that is a separate feature.
* Web UI login as a subordinate.
* Replacing the `serviceuser` plugin. Group-owned service accounts with
  independently granted permissions remain a valid, different model.
