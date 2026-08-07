---
title: "Design Doc - Zoekt-Based Code Search for Gerrit - Solution: Gerrit-Aware Search Platform"
permalink: design-docs/zoekt-search-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/zoekt-search
---

# Solution: Gerrit-Aware Search Platform

## <a id="overview">Overview</a>

Gerrit remains the identity and trust boundary for every search request.
A logged-in user's query flows from Gerrit's own UI, through a Gerrit-side
component that knows the user and their allowed scope, to a separate search
platform built around stock Zoekt. The search platform is only ever told a
query together with the scope it's allowed to touch.

The search platform adds the pieces that stock Zoekt does not provide on
its own: a scoped gateway in front of multiple Zoekt webservers, repository
ID management, index generation publishing, per-node shard activation, and
a control plane for routing and node health.

The full step-by-step walkthrough, for both the query path and the
indexing path, is in [End-to-End Flow](#end-to-end-flow) below.

![Zoekt-based code search high-level architecture](/images/zoekt-search-architecture.png)

## <a id="components">Components</a>

The design is built from a small number of responsibilities, split across
two independent systems: one on the Gerrit side, one forming a standalone
search platform.

**On the Gerrit side:**

* **Search plugin** — the only user-facing entry point and trust boundary.
  Requires a logged-in Gerrit user, resolves their identity through
  whichever authentication method the deployment already uses, attaches
  that user's allowed scope, and returns results through Gerrit's UI and
  REST API, with each result linking out to Gitiles for viewing the
  matched file. Also exposes, for the same allowed scope, which of the
  user's readable projects and branches are currently indexed.
* **Visibility awareness** — continuously derives, from Gerrit's real
  access control rules and the currently indexed project/ref coverage,
  which projects and refs each group of users can read, and keeps that
  answer ready so most search requests do not have to wait on it. A bounded
  on-demand computation handles a group that has not yet been seen. The
  plugin can keep both a group-level visibility cache and an account-level
  cache of the effective scope for recently active users.
* **Index coverage configuration** — records which projects and branches
  should be indexed. This can start as an administrator-owned
  configuration and later expose project-owner controls if a deployment
  wants delegated management.

**In the search platform (independent of Gerrit, reusable by any caller
that can supply a valid scope):**

* **Search gateway** — the entry point for scoped queries and coverage
  requests. It translates the caller-supplied `{server, project, refs}`
  scope into Zoekt repository IDs and branches, ANDs that scope into the
  parsed Zoekt query, routes to the right shard groups, fans out to one
  healthy replica per touched group, and merges ranked results. Empty,
  missing, or fully unresolved scope returns zero results with scrubbed
  statistics.
* **Zoekt webservers** — stock Zoekt instances that hold `.zoekt` shards
  and execute the actual search. The design does not require forking Zoekt;
  scope is enforced by adding a `BranchesRepos` constraint to each query
  before it reaches Zoekt.
* **Indexer** — obtains stable non-zero repository IDs from the control
  plane, stamps them into repositories before indexing, invokes Zoekt's
  normal git indexer, and publishes the resulting shards as immutable
  generations.
* **Sync agents** — run next to Zoekt webservers, fetch the newest
  generation for the node's shard group from the artifact store, validate
  shards locally, and atomically rename them into the directory watched by
  Zoekt.
* **Artifact store** — holds published index generations durably, so
  nodes can fetch a generation independently of the indexing pipeline that
  produced it.
* **Control plane** — owns repository ID allocation, routing snapshots, and
  node health. It can be backed by a consistent store and exposed through a
  small stateless broker API.

This split is deliberate: the search platform never needs to understand
Gerrit's users, sessions, or access rules. All Gerrit-specific knowledge
stays on the Gerrit side.

## <a id="end-to-end-flow">End-to-End Flow</a>

**Query flow — a user searches:**

1. A logged-in Gerrit user submits a query through Gerrit's own UI or REST
   API.
2. The **search plugin** resolves the user's identity and asks
   **visibility awareness** for that user's currently known allowed scope
   — normally an already-computed answer, occasionally a short, bounded
   wait if this is the first time that user's group has ever been asked.
3. The search plugin forwards the query together with the allowed scope to
   the **search gateway**. The scope always travels separately from the
   query text, so a user's own query can never be used to widen it.
4. The **search gateway** resolves project names to repository IDs,
   converts refs to branch labels, builds a Zoekt `BranchesRepos` scope,
   and combines that scope with the parsed user query.
5. The gateway uses its cached control-plane routing snapshot to choose one
   healthy Zoekt replica for each touched shard group, sends concurrent
   requests, and treats an unavailable shard group as incomplete rather
   than widening scope or failing open.
6. Each Zoekt webserver evaluates the query only against the content named
   by the scope constraint, and returns its matches.
7. The search gateway merges, ranks, and returns the combined results to
   the search plugin, which renders them back to the user.

Three outcomes are always distinguished: normal results; "no results"
(covering both a genuinely empty match and a user with no readable scope —
deliberately indistinguishable, so a lack of access can never be inferred
from the response); and "search unavailable" (the search platform itself
could not be reached), so an outage is visible rather than mistaken for an
empty result.

**Coverage flow — a user checks what's indexed:**

1. A logged-in Gerrit user asks the search plugin which of their readable
   projects/branches are indexed. For large result sets, the request can
   include pagination and filters over project or branch names.
2. The search plugin asks **visibility awareness** for the user's allowed
   scope, the same way it does for a search query.
3. The search plugin asks the **search gateway** for indexed coverage and
   returns the intersection of that coverage and the user's allowed scope
   — never revealing coverage for a project/branch outside the user's
   allowed scope.

The same indexed/not-indexed status can be shown from repository and
branch views by asking for coverage only for the project/branch rows the
caller is already allowed to see.

**Indexing flow — keeping the index current:**

1. A deployment supplies the repositories and refs that should be indexed,
   according to its configured coverage policy (see
   [Branch Policy](#branch-policy)). The source repositories may come from
   Gerrit's normal replication or another local mirror maintained by the
   site.
2. The **indexer** asks the control plane for the stable non-zero
   repository ID for each project, stamps that ID into the repository
   metadata consumed by Zoekt, and runs Zoekt's normal git indexer for the
   configured refs.
3. Newly built shards are grouped by shard partition and published to the
   **artifact store** as immutable generation directories.
4. A **sync agent** next to each Zoekt webserver polls or watches for the
   newest generation for its partition, downloads those shards to local
   disk, validates them, and atomically renames them into the webserver's
   watched directory. Publish and activation are deliberately separate:
   the indexer never writes directly into a serving node.
5. The **control plane** records repository IDs, routing, and live nodes.
   Gateway instances consume this as cached snapshots.

## <a id="branch-policy">Branch Policy</a>

Which projects and branches get indexed and access-checked is a deployment
decision, not a fixed requirement of this design. A deployment can start
by indexing only default branches for selected projects and expand from
there — to a broader active-branch set, to specific long-lived branches,
or further — once it has measured the actual demand, storage cost, and
access-check cost of doing so for its own repositories. Nothing in this
design requires starting anywhere other than the smallest option.

Coverage configuration should be treated as data consumed by the indexing
pipeline and control plane, not as code baked into either service. That
lets administrators or project owners change indexed coverage without
rebuilding the search platform.

Repository IDs are part of that managed data. IDs must be stable, non-zero,
and never reused for another project; otherwise a query scoped to one
project could accidentally match shards for another project. The control
plane should be the single authority that allocates and persists IDs, and
the indexer should fail closed if it cannot obtain a valid ID.

## <a id="scalability">Scalability</a>

Indexed content and query load are spread across many serving nodes, and
that fleet can grow, shrink, or be rebalanced independently of the
Gerrit-side components — a busier search platform does not require
touching Gerrit, and vice versa.

The gateway routes by repository ID to shard groups and sends each query
only to groups that can contain in-scope repositories. Each shard group can
have multiple replicas; the gateway chooses a healthy replica from its
cached routing snapshot and marks results incomplete if a needed group has
no live replica. This preserves correctness under partial failure: missing
capacity can hide matches temporarily, but it cannot add out-of-scope
matches.

The index rollout path is eventually consistent by design. New generations
are published once, then sync agents activate them independently on each
serving node. This avoids a coordinated fleet-wide restart and lets a node
keep serving its previous validated shards if it cannot fetch or validate a
new generation.

The visibility-awareness component scales with the number of Gerrit access
groups and projects, not with the number of users or the rate of search
requests, since it computes and caches an answer per group rather than per
user or per request.

The largest scale risk for any given deployment is how many branches it
chooses to index — a large or unevenly distributed branch count drives
indexing, storage, and access-derivation cost independently of query
volume, which is why branch coverage is treated as a deployment policy
decision to be measured, not a fixed default (see
[Branch Policy](#branch-policy)).

Visibility-derivation cost and refresh interval must be tuned per
deployment: measure the cost of deriving allowed scope from Gerrit's access
rules, and tune how often it is refreshed against that measurement, rather
than assuming one interval fits every installation. A new or previously
unseen account/group adds a bounded, synchronous derivation cost to its
first query — trading a slower first request for not returning empty
results to a new user — and that timeout should be tuned per deployment
as well.

The control plane should also be kept off the per-query hot path. Gateways
should watch routing and repository-ID snapshots and serve from memory.
Losing the control plane temporarily makes those snapshots stale; it should
not fail every query.

## <a id="alternatives-considered">Alternatives Considered</a>

**Expose the underlying search engine directly to users**

Simpler to deploy, but rejected outright: a general-purpose search engine
has no concept of Gerrit sessions or access rules, so exposing it directly
would mean either no access control on search results, or duplicating
Gerrit's access model inside a system that was never designed to hold it.

**Have the search platform enforce Gerrit's access rules itself**

Would require the search platform to understand Gerrit's permission model
in depth, risking the two implementations drifting apart over time, and
tightly coupling a platform that should be able to serve any caller to one
specific host application's security model. Keeping all access-control
knowledge on the Gerrit side, and having the search platform simply
enforce whatever scope it's handed, keeps the two systems cleanly
separated.

**Fork Zoekt to add Gerrit-specific authorization**

Would put Gerrit-specific concepts into the search engine and make future
Zoekt upgrades harder. Stock Zoekt already has the query-level primitives
needed to constrain searches by repository ID and branch, so the safer
integration point is a gateway that constructs scoped Zoekt queries before
fan-out.

**Check every result against Gerrit after search**

Would reduce the risk of stale visibility data, but it would also make
search latency and load proportional to result count and Gerrit's live
permission-check cost. It also does not prevent leaking aggregate
information unless the search platform still avoids exposing raw match
counts before filtering. The proposed design filters before search and
accepts a documented, bounded staleness window for access changes.

**Off-the-shelf commercial or hosted code search products**

Worth evaluating independently on their own merits (Gerrit integration,
access-control parity, scale, operational fit), but out of scope for this
design, which assumes building and operating the search platform
in-house.

## <a id="pros-and-cons">Pros and Cons</a>

Pros:

* Because the search platform's gateway only ever consumes a
  caller-supplied scope, it is not limited to serving the Gerrit plugin —
  any future caller that can supply a valid scope could reuse the same
  platform without new Gerrit-specific work on the search platform side.
* The gateway can be extended to route to other code-search provider nodes,
  not only Zoekt webservers, as long as the provider can enforce an
  explicit project/ref scope before returning results.
* The search platform uses stock Zoekt webservers and Zoekt's normal
  indexing path, so it avoids maintaining a Gerrit-specific fork of the
  search engine.
* Gerrit and the search platform can each be upgraded, scaled, or rolled
  back on their own schedule, without coordinating a joint release.

Cons:

* Debugging a bad result is harder than with a single embedded system: a
  wrong or missing result could stem from a stale visibility scope, a
  gateway routing issue, or an indexing problem, and diagnosing it means
  correlating state across two independently operated systems.
* Every query takes on an extra network hop (plugin to gateway to Zoekt
  webservers) that a search engine embedded directly in Gerrit would not
  have.
* Repository ID allocation becomes correctness-critical. The system must
  guarantee stable, non-zero, non-reused IDs before indexing.

## <a id="implementation-plan">Implementation Plan</a>

1. Land this design.
2. Build the Gerrit-side search plugin and visibility-awareness component.
3. Build the search gateway against stock Zoekt webservers, including
   scoped query construction, shard-group fan-out, result merging, and
   scrubbed empty-scope behavior.
4. Build the indexer, artifact-store publication, and per-node sync-agent
   activation path.
5. Build the control plane for repository ID allocation, routing snapshots,
   and node health, keeping it off the query hot path.
6. Validate against a subset of real repositories.
7. Roll out search starting with default-branch coverage.
8. Measure real branch activity, indexing cost, and access-derivation cost,
   and expand branch coverage per [Branch Policy](#branch-policy) based on
   those measurements.

## <a id="time-estimation">Time Estimation</a>

Rough implementation phases:

* Gerrit plugin, search UI/API, and visibility caching: 4-6 weeks.
* Scoped gateway, Zoekt fan-out, result merge, and coverage API: 3-5 weeks.
* Indexer, artifact publication, and per-node sync agents: 3-5 weeks.
* Control plane, repository ID allocation, routing snapshots, and node
  health: 4-6 weeks.
* Production hardening, rollout automation, metrics, and staged deployment:
  4-8 weeks.
