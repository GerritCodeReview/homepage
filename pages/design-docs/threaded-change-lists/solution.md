---
title: "Design Doc - Change Dependency Threads - Solution"
permalink: design-docs/threaded-change-lists-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/threaded-change-lists
---

# Solution - Indexed parents, threaded rendering and a dependency provider API

## <a id="overview"> Overview

Split the problem into what Gerrit core already knows and what it does not.

* **Core knows Git ancestry.** Store each unmerged change's direct parent
  commits in the change index, expose them to list queries without leaving
  the index, and render lists and the relation chain as a base-first forest
  behind an opt-in preference.
* **Core does not know `Depends-On`.** Add a small frontend plugin API through
  which a plugin supplies extra typed edges, and optionally nominates missing
  members of a network. Gerrit keeps ownership of ordering, rendering,
  selection and pagination.
* **A plugin computes the network.** The `change-network` plugin combines Git
  ancestry with `Depends-On` footers, in both directions and across projects,
  and serves the result over REST. It feeds the frontend API above and is
  directly usable by Zuul or other similar systems.

Each layer is useful without the ones above it:

| # | Layer | Where | Change |
|---|-------|-------|--------|
| 1 | Index direct parents of unmerged changes; `parentcommit:` operator | core, backend | [646083](https://gerrit-review.googlesource.com/c/gerrit/+/646083) |
| 2 | `INDEXED_DEPENDENCIES` query option and server capability | core, backend | [646084](https://gerrit-review.googlesource.com/c/gerrit/+/646084) |
| 3 | `threaded_changes` preference; threaded list and relation chain | core, frontend | [644585](https://gerrit-review.googlesource.com/c/gerrit/+/644585) |
| 4 | `plugin.changeDependencies()` provider API | core, frontend | [646085](https://gerrit-review.googlesource.com/c/gerrit/+/646085) |
| 5 | `group_topics` preference, independent of threading | core, frontend | [646086](https://gerrit-review.googlesource.com/c/gerrit/+/646086) |
| 6 | Expansion of list results to whole networks | core, frontend | [654663](https://gerrit-review.googlesource.com/c/gerrit/+/654663) |
| 7 | Network REST API and dependency provider | plugin | [change-network](https://opendev.org/inaugust/gerrit-change-network) |

## <a id="detailed-design"> Detailed Design

### 1. Parent commits in the change index

Add a stored index field holding the ordered direct parent commit IDs of the
current patch set, together with the patch set number and revision the
snapshot was taken from.

* Written for **unmerged** changes only: new, work in progress and abandoned.
  Abandoned changes are included because a change in the middle of a stack can
  be abandoned while open changes still sit on top of it, and that is exactly
  the state a user needs to see. Merging a change removes its postings.
* Excluded from the default field selection of change queries. It is loaded
  only when a caller asks for it, so existing queries read no more than today.
* A missing snapshot means "unknown", not "no parents". Readers never fall
  back to Git or NoteDb.
* New search operator `parentcommit:SHA-1`: unmerged changes whose current
  patch set has that commit as a direct parent. It is an exact lookup. Callers
  that want Git children of a change combine it with `project:` and `branch:`
  and query each of the change's patch set commits, since a child may sit on
  an older patch set. The existing `commit:` operator already answers the
  forward direction.
* The index stores adjacency only. There is no materialised transitive closure
  to keep consistent; callers traverse.

This needs a new change index schema version and therefore a reindex.

### 2. `INDEXED_DEPENDENCIES` list option

A new `ListChangesOption` that adds `indexed_dependencies` to each returned
`ChangeInfo`:

```
"indexed_dependencies": {
  "revision": "…",
  "patch_set_number": 3,
  "parents": [
    {"change_number": 122, "patch_set_number": 2, "commit_id": "…"}
  ]
}
```

* Parents are resolved **only against other changes in the same response**
  (the union across queries for a multi-query request). Hidden, filtered-out
  and off-page parents are omitted, as are ambiguous matches. The option never
  changes which changes a query returns.
* A parent entry names the exact patch set referenced, which may be older than
  that change's current one. This is how a stale child is detected.
* It requires none of `CURRENT_REVISION`, `CURRENT_COMMIT` or `PARENTS`, opens
  no repository and issues no further queries. It is kept out of
  `ChangeJson.REQUIRE_LAZY_LOAD`, and tests assert this with NoteDb disabled.
* Rollout is explicit. `change.enableIndexedDependencies` (default `false`)
  makes the server advertise an `indexed_dependencies` capability in
  `ChangeConfigInfo`, and only when the active index has the field. The
  frontend requests the option only when it sees the capability. An
  administrator turns it on after all nodes are upgraded and the new index is
  active.

### 3. Threaded rendering

A new account preference `threaded_changes`, default `false`.

When it is on and the server advertises the capability:

* Change lists request `INDEXED_DEPENDENCIES`. The dashboard preload URL
  generated server-side uses the same option set as the runtime request, so
  preloading still hits.
* Each list section is projected onto a display forest: a change appears once,
  beneath its first visible parent, base first, with connector rails. A
  stack is positioned at its most recently updated member, so
  an update moves the stack as a whole.
* Multiple parents and cycles are kept in the graph data and broken only for
  display.
* Merged changes are never threaded. Edges never cross sections or pages.
* Keyboard navigation and bulk selection follow display order. The set of
  rows is exactly the query result.
* Deep stacks compress the rail columns to a shared maximum depth so the
  subject stays readable at phone width.
* The relation chain on the change page is rendered base first with the same
  component.

When the preference is off, nothing changes: same requests, same rendering.

### 4. Dependency provider API

`plugin.changeDependencies().register(provider)`, one provider per plugin.

```ts
interface ChangeDependenciesProvider {
  fetch(request: {
    context: 'change-list' | 'related-changes';
    changes: ReadonlyArray<{_number, project, branch,
                            current_revision?, current_revision_number?}>;
    signal: AbortSignal;
  }): Promise<{
    edges: Array<{from: number; to: number; type: 'git' | 'depends-on'}>;
    changes?: Array<ChangeDependencyChange>;   // see section 6
  }>;
}
```

* Edges point from dependent to dependency. Gerrit merges provider edges with
  native ones and deduplicates. Git ancestry wins when choosing the single
  display parent.
* All dashboard sections are batched into one request per provider.
* Native threads render immediately; provider edges refine the display when
  they arrive. A failed or slow provider leaves the native display intact.
  Requests are aborted on navigation, changed inputs, disabling the
  preference, or after thirty seconds.
* Providers are only invoked when `threaded_changes` is on.
* For the relation chain, providers may only connect entries already shown.

### 5. Topic grouping

A separate preference `group_topics`, default `false`, independent of
`threaded_changes`. Visible unmerged changes sharing a topic are made
contiguous and outlined as a group. Grouping never adds rows and, on its own,
requests no dependency data.

See [open questions](#open-questions) for the interaction with threading.

### 6. Network expansion

A provider may return `changes`: identities of network members that are not
in the result, such as the rest of a stack or a dependent in another project.

* Gerrit loads those rows itself through ordinary authenticated search. It
  renders nothing a plugin says about them beyond identity, so permissions and
  row content come from core. Unreadable, merged and stale members are dropped.
* Only members connected to a seed row are shown.
* Bounded: at most 500 nominated rows per provider per request, loaded in
  batches of 50.
* Pagination: the page limit is applied after expansion and is soft, so a
  network is never cut in half. The next page starts after the last *query
  result* consumed, not after the last row drawn. Counts and offsets always
  refer to query matches. A context row can therefore appear on more than one
  page; a match is never skipped.

This is frontend-only and works with any provider.

### 7. The change-network plugin

Backend:

```
GET /config/server/change-network~capabilities
GET /changes/{id}/change-network~network?max_nodes=N
```

The network response lists nodes (current patch set of each change), typed
edges (`git`, `depends-on`) with the original parent SHA or footer text,
unresolved references with a reason (`external`, `unavailable`, `invalid`,
`ambiguous`, `project_mismatch`), strongly connected groups as `cycles`, and a
`complete` flag with reasons when it is false.

* Traversal follows dependencies and dependents recursively through open
  changes. Merged and abandoned changes are terminal nodes.
* `Depends-On` is read from the trailing footer block, as Gerrit's footer index
  does. Forward resolution and reverse lookup share one finite set of URL
  spellings, so no edge can be found in one direction and missed in the other.
* Discovery uses Gerrit's existing indexes on demand. There is no plugin
  index, startup scan or background worker.
* Visibility is checked before a candidate takes part. A hidden dependency is
  indistinguishable from a missing one.
* Bounded by node count, candidate count and a time budget. Hitting a bound
  yields an explicit partial result or a 503, never a truncated graph marked
  complete.
* Consistency is that of the secondary index, and is advertised as eventual.
* Administrators can map URLs of another Gerrit server to local projects, so
  `Depends-On` URLs naming an upstream resolve to locally tracked copies.

Frontend: registers a provider that looks up the network of each displayed
component (two requests in flight at most, one response reused for every
member of the component), verifies revision identities against the list, and
returns edges plus missing members.

### <a id="scalability"> Scalability and performance

* **Preference off:** no change in requests, index fields loaded, or
  rendering.
* **Preference on, core only:** one extra stored field read per row, from the
  index. Parent resolution is in-memory over the page. Threading is linear in
  page size on the client.
* **Index:** one additional small stored field per unmerged change and one
  posting per parent. One reindex.
* **Plugin provider:** one network request per connected component on the
  page, two in flight. Each is index queries bounded as above. This is the
  most expensive part of the design and is confined to hosts that install the
  plugin and users who opt in.
* **Expansion:** additional list queries in batches of 50, bounded at 500 rows.

### Permissions

Core threading resolves parents only among rows already returned to the
caller. Expansion loads rows through the caller's own search. The plugin
filters by visibility before resolution, including for ambiguity decisions.

## <a id="alternatives-considered"> Alternatives Considered

* **Use existing list options (`CURRENT_COMMIT`, `PARENTS`).** The first
  implementation did this. It takes list queries off the index-only path:
  every row opens its repository and performs a parent lookup and a
  reachability walk, for all users of a page that requests it. Changing the
  option set on the client also stops the server-generated dashboard preload
  from matching. Serving parents from the index avoids both.
* **Default the preference to on.** Considered for hosts where stacks are the
  norm. A client-side default cannot be distinguished from a backend that
  does not know the preference, which forces the feature on during version
  skew. Default off, with data availability gated by a server capability, has
  no such window.
* **Call the related-changes endpoint per row from the client.** One Git walk
  per row. Worse than the above.
* **Reuse the indexed patch set `group` field.** It identifies changes pushed
  together, which approximates a stack but does not give order, forks, or
  which patch set a child is based on. The plugin uses it only to find
  candidates, then validates against actual parents.
* **Thread on the server and return ordered results.** Would change the
  meaning of query order, limits and `_more_changes` for every API client.
  Keeping the query result unchanged and projecting it in the UI is less
  invasive.
* **Implement the whole feature as a plugin.** There are no plugin hooks for
  reordering rows, drawing between them, or redefining selection order, and
  adding hooks that general would be a much larger API than the narrow edge
  provider proposed here. Git ancestry is also core data and should not need a
  plugin.
* **Understand `Depends-On` in core.** It is a convention of one CI system, and
  its resolution rules (URL forms, cross-server references, cycles) belong to
  that ecosystem.
* **Maintain a persistent dependency graph in the plugin.** An earlier version
  of the plugin did. It needed a bootstrap scan, a journal and a reconciliation
  loop, and could disagree with Gerrit's own index. Replaced with on-demand
  discovery over existing indexes.

## <a id="pros-and-cons"> Pros and Cons

Pros

* No cost and no visible change for users and hosts that do not opt in.
* List queries remain index-only with the feature on.
* Core gains two generally useful primitives regardless of the UI: a
  `parentcommit:` operator and index-served parent metadata.
* The plugin API is small, and core keeps control of rendering and selection.
* Dependency semantics that are not Gerrit's stay out of core.
* The same network answer serves the UI, CI and tooling.

Cons

* A schema bump and reindex.
* Two new account preferences and one new server option.
* Core-only threading sees only what is on the page: a stack split across
  pages or sections renders as separate pieces unless a provider expands it.
* The provider performs one request per component rather than one per page.
* Soft page limits mean a page can exceed the requested size, and context rows
  can repeat across pages.
* A new public frontend plugin API to maintain.

## <a id="open-questions"> Open Questions

1. **Topics combined with threading.** With both preferences on, a topic is
   placed as one unit at a single indentation level. A stack that shares a
   topic is therefore shown in dependency order inside an outline but without
   rails, and unrelated changes that share a topic are placed together under
   whichever parent one of them has. Options: keep
   rails inside a topic group and treat the outline as an overlay; group by
   topic only when members are not otherwise connected; or ship threading
   first and settle topic grouping separately.
2. **Should network expansion work without a plugin?** Core could expand Git
   stacks itself using `parentcommit:` and `commit:`. This would close the
   "stack split across pages" gap for hosts without the plugin, at the cost
   of extra queries per page.
3. **Batch network endpoint.** A plugin endpoint accepting many roots would
   replace per-component requests with one per page.
4. **Default.** Should the preference ever default to on, or should hosts be
   able to set the default?

## <a id="implementation-plan"> Implementation Plan

Changes land in dependency order; each is releasable alone.

1. Index field and `parentcommit:` operator (646083).
2. `INDEXED_DEPENDENCIES` and capability (646084).
3. Threaded rendering behind the preference (644585). Core-only threading is
   complete at this point.
4. Provider API (646085).
5. Network expansion (654663).
6. Topic grouping (646086), once open question 1 is settled. It currently
   sits below expansion in the stack; the two would be restacked so that
   expansion does not wait on it.
7. Move the `change-network` plugin repository to
   gerrit-review.googlesource.com and release it tracking the core API.

Owner: Monty Taylor.

## <a id="time-estimation"> Time Estimation

Most of the work is done.

* **Core changes:** all six are implemented, up for review and passing CI.
* **Running deployment:** the full series is running in a local deployment
  together with the plugin, and is in daily use there. Screenshots of the
  change list and relation chain are available on request.
* **Plugin:** `change-network` is implemented and deployed. It is currently
  hosted on OpenDev. We would like to move its repository to
  gerrit-review.googlesource.com, so that it is developed, reviewed and
  released alongside the core API it depends on.

Remaining effort is review iteration, resolving the open questions, and the
plugin repository move
