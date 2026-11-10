---
title: "Design Doc - Subordinate Identities - Solution - Subordinate Accounts"
permalink: design-docs/subordinate-identities-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Subordinate Accounts

## <a id="overview"> Overview

A subordinate is an ordinary account with two additions: a `parent` link and
a `scope`. Permission checks for a subordinate are evaluated against the
parent's group memberships and then filtered by the scope. Because the scope
lives on the identity rather than on a credential, the existing auth tokens
and SSH keys work for subordinates unchanged.

The design treats delegation as attenuation: authority can be passed down and
narrowed, never widened. "Can a subordinate create another subordinate?" is
therefore not a special case. Creating subordinates is a permission like any
other; a subordinate has it if its scope includes it, and anything it creates
is bounded by its own effective permissions.

## <a id="detailed-design"> Detailed Design

### Storage

Subordinates are stored like any account, under `refs/users/XX/ID` in
`All-Users`. `account.config` gains:

```
[account]
  fullName = Zuul proposer
  parent = 1000096
[provenance]
  kind = ci
  description = Proposes requirements updates
[scope]
  project = openstack/*
  allow = read
  allow = upload
  allow = addPatchSet
```

* `account.parent` is immutable after creation.
* An account with `parent` set and no `[scope]` section has no permissions.
* `scope.project` is a list of project name patterns using the same syntax as
  project watches. Absent means "any project the parent can act on".
* `scope.allow` uses the permission names already used in `project.config`
  (`read`, `push`, `addPatchSet`, `abandon`, `submit`, `label-Code-Review
  -1..+1`, ...) and global capability names.
* A subordinate's username is `<primary username>/<name>`, for example
  `mordred/archon`. The current username pattern rejects `/`, so no existing
  or future ordinary account can occupy this namespace. Every other readable
  separator (`+ . - _ ~ ! @ =`) is already legal inside a username and would
  need reserving and an audit of existing accounts; `:` is rejected but
  collides with HTTP Basic authentication.
* The general username pattern is not widened. The subordinate creation
  endpoint is the only place that mints names of this form, and the places
  that look accounts up by username accept it in addition to the existing
  pattern.
* In REST URLs the username must be encoded as `mordred%2Farchon`, as project
  names with slashes already are.

One addition to the vocabulary is needed in the first version. In
`project.config`, proposing a change and pushing directly to a branch are the
same permission (`push`) distinguished only by ref (`refs/for/*` versus
`refs/heads/*`). Since ref patterns are out of scope, the scope vocabulary
defines `upload` as "`push` on `refs/for/*`", so that "may propose but may not
land" is expressible from day one.

### Permission evaluation

* A new `CurrentUser` subtype represents an authenticated subordinate. Its
  account ID is the subordinate's. `getUserForPermission()`, which already
  exists to support impersonation, returns a user whose effective groups are
  the parent's.
* `PermissionBackend` gains a decorating layer, applied in core rather than in
  `DefaultPermissionBackend`, so that alternative backends are covered. For a
  subordinate it evaluates the requested permission as the parent and then
  requires the scope to allow it.
* For nested subordinates this recurses to the primary. The depth is limited by
  `accounts.maxSubordinateDepth` (default 3) to bound the cost.
* Evaluation is always dynamic. Nothing about the parent's permissions is
  snapshotted at creation time, so a parent losing access takes effect for
  all descendants immediately.
* Subordinates cannot be members of groups. Any membership would grant
  permissions independently of the parent and break the subset invariant.
* A system group `Subordinate Users` contains every subordinate, so that
  projects can write `BLOCK` rules against them if they wish.

### Account-level operations

Many account operations are not guarded by ACLs today; they are allowed when
the caller is the account being modified. Those checks must not let a
subordinate modify itself, or the scope is meaningless. The rule is:

| Operation | Who may perform it |
| --- | --- |
| Create a subordinate | Any account whose effective permissions include `createSubordinate`; the new scope must be a subset of the creator's effective permissions |
| Change a subordinate's scope, tokens, SSH keys, name, annotation, active state | Any ancestor |
| Delete a subordinate | Any ancestor; cascades to descendants |
| Modify its own scope, parent, or credentials | Never |
| Modify an ancestor or a sibling | Never |

`createSubordinate` is a new global capability granted to `Registered Users`
by default. A subordinate holds it only if its scope lists it.

A subset check at creation time is a convenience for early errors only.
Because evaluation is dynamic, a scope that names more than the parent has is
harmless.

Deactivation is evaluated up the chain: an account is active only if every
ancestor is.

### Authentication

No change to token or SSH key verification. The subordinate authenticates
with its own username and its own credentials. The authentication filters
construct the subordinate user type when the account has a parent.

### Email and commit identity

Subordinates have no email external IDs of their own. For committer and author
validation on push, a subordinate may use any verified email of its primary, so
a primary's commits can be uploaded by their subordinate without `forgeAuthor`
or `forgeCommitter`.

Notifications addressed to a subordinate are delivered to the primary, subject
to the primary's preferences. A subordinate is never required to have a mailbox
of its own.

So that the primary can tell these messages apart:

* Every notification sent on behalf of a subordinate carries an
  `X-Gerrit-Subordinate: <name>` header.
* Each subordinate has a `subaddress` setting, set by an ancestor, with three
  values:
  * `NONE` (default): mail goes to the primary's preferred email.
  * `DELIVERY`: the recipient address is the primary's preferred email with the
    subordinate's name inserted as a subaddress (RFC 5233):
    `mordred@example.com` becomes `mordred+archon@example.com`. The address is
    derived at send time, is never stored, and is not an identity: it is not
    shown as the subordinate's email and is not accepted as a committer or
    author.
  * `IDENTITY`: as `DELIVERY`, and in addition the subaddressed form becomes
    the subordinate's own email. It is registered as a `mailto:` external ID
    for the subordinate, shown as its email, and accepted as its committer and
    author identity. This gives a subordinate a distinct, attributable commit
    identity without anyone having to provision a mailbox for it.

If the primary's address already contains a subaddress, it is used unmodified
and `IDENTITY` is not available.

For `IDENTITY` the address is fixed when the setting is enabled, because it
will appear in commits and must keep resolving to the subordinate if the primary
later changes its preferred email. No verification mail is sent: the base
address is already verified and the owner is asserting that their mail system
supports subaddressing. Enabling it fails if another account already holds
that address.

The primary's own emails remain valid identities for the subordinate under every
setting, so a contributor to a project that does not want tooling recorded in
its history can continue to commit as themselves.
`change.showSubordinateProvenance` does not, and cannot, alter the author or
committer of a pushed commit.

The setting is off by default because subaddressing depends on the receiving
mail system. Where it is unsupported the message bounces, or could in
principle reach a different mailbox.

If the primary and one of its subordinates are both recipients of the same
notification, one message is sent when the addresses are identical and two
when subaddressing is in use.

### Submit requirements

Separate accounts under one person's control would otherwise allow that
person to satisfy "two approvals" or "approved by someone other than the
uploader" alone. To prevent this:

* The `non_uploader` and `non_contributor` arguments of the label predicate
  compare primaries, not account IDs.
* `count` arguments count distinct primaries.
* Ignore-self-approval behaviour compares primaries.

Votes are still stored and displayed per account. Only their evaluation in
submit requirements is collapsed to the family.

### Provenance

* The acting account is recorded in NoteDb as it is for any account; the primary
  is derivable from the account and is exposed in `AccountInfo` to callers
  with `viewAllAccounts` or `modifyAccount`.
* `provenance.kind` and `provenance.description` are optional and set by an
  ancestor. When present, `AccountInfo` carries them and the UI renders a
  chip next to the account name.
* A new inherited project setting, `change.showSubordinateProvenance` (`TRUE`,
  `FALSE`, `INHERIT`, default `TRUE`), controls whether those fields are
  returned and rendered for changes in that project. When `FALSE`, Gerrit also
  does not add subordinate-derived information to any commit it creates on
  submit.
* The setting controls annotations only. A subordinate is still a distinct
  account with its own name.

### Limits

* `accounts.maxSubordinatesPerPrimary` (default 10) bounds a family's size.
* `accounts.maxSubordinateDepth` (default 3).
* Subordinates count against their primary for any per-account quota.

### REST API and UI

* `GET/PUT/DELETE /accounts/{id}/subordinates/{name}` and
  `GET /accounts/{id}/subordinates/`.
* Existing token and SSH key endpoints under `/accounts/{subordinate}/` are
  authorised for ancestors.
* A "Subordinate identities" section in user settings to create, scope,
  annotate and revoke, and to manage each subordinate's tokens.
* A `primary:` change query operator to find changes owned by any member of a
  family.

## <a id="alternatives-considered"> Alternatives Considered

1. **Scopes on tokens.** A scope attached to an individual auth token of an
   ordinary account. This is simpler and cannot be used as a sockpuppet, but
   every action is the user's own: the credential cannot be a separate
   reviewer, cast a distinguishable vote, or be queried for. It also leaves
   SSH keys unscoped. It can be added later using the same scope grammar.
2. **Extending the `serviceuser` plugin.** The plugin grants permissions to
   service users through groups, independently of their owners. The subset
   invariant and the submit requirement handling need core support in either
   case.
3. **Snapshotting permissions at creation.** Copying the parent's permissions
   into the subordinate would avoid evaluating the chain on each request, but
   the subordinate would keep access the parent later lost.
4. **Denying all account operations to subordinates.** Simple, but it rules
   out agents that manage their own workers, and it is unnecessary once
   account management is expressed as permissions that a scope may or may
   not include.

5. **Presenting a subordinate's actions as its primary's when provenance is
   hidden.** This would hide the subordinate's existence entirely, but it
   touches every API that returns an account and makes the audit trail differ
   from what users see. Suppressing the annotation is sufficient for projects
   that do not want tooling advertised.
6. **Letting projects count family members as separate voters.** Rejected:
   a project that enforces a number of approvals is asking for that many
   people.

## <a id="pros-and-cons"> Pros and Cons

Pros: self-service; a compromised credential is bounded by a scope and by its
owner's own access; works for HTTP and SSH; revocation is transitive and
automatic; the accountable account is always known.

Cons: more accounts in `All-Users`; an extra account lookup per level of
nesting on each permission check; submit requirement evaluation must become
family-aware; plugins that perform their own "is this the caller's account"
checks need review.

## <a id="implementation-plan"> Implementation Plan

1. `account.parent`, the subordinate user type, and family-aware activity
   checks. No way to create one yet except in tests.
2. Scope storage and the `PermissionBackend` decorator.
3. Account-operation authorisation rules.
4. Family-aware submit requirement predicates.
5. REST API for creation and management; limits.
6. Settings UI.
7. Provenance fields, project setting and UI chip.
8. `primary:` query operator and documentation.

## <a id="open-questions"> Open Questions

* Whether `/` is accepted in SSH login names by the SSH server and common
  clients, and in `https://user@host/` clone URLs by common proxies. If not,
  `,` is the fallback: it is also rejected by the current pattern.
* A ref permission using `${username}`, such as
  `refs/heads/sandbox/${username}/*`, expands for a subordinate to a ref beneath
  its primary's. Whether the primary should thereby have access to its
  subordinates' sandbox refs.
