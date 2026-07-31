---
title: "Design Doc - Zoekt-Based Code Search for Gerrit - Use Cases"
permalink: design-docs/zoekt-search-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/zoekt-search
---

# Zoekt-Based Code Search for Gerrit - Use Cases

## <a id="objective">Objective</a>

Gerrit has no built-in way to search code content across repositories and
branches. Users need to search across the repositories and branches they
are allowed to read, with results respecting Gerrit's existing project and
branch/ref access rules, including private or restricted refs, and the
solution must work for installations whose code corpus is larger than a
single search engine instance should own.

## <a id="background">Background</a>

A dedicated code search engine is good at answering "which files across many
repositories match this query" quickly, but on its own it has no concept of
Gerrit users, sessions, or access control — it will return whatever a query
matches unless something tells it, per request, which projects and
branches that particular request is allowed to touch.

Gerrit, conversely, already knows exactly this: whether a given user can
read a given project and ref, using its own existing permission model. What
is missing is the piece that sits between the two — something that lives
inside Gerrit, knows who is asking, derives what they may read, and is the
only thing trusted to make that decision.

At any real scale, deriving a user's allowed scope by re-checking Gerrit's
access rules synchronously on every keystroke-driven search request does
not work — it would make search slow in proportion to how complex an
installation's access rules are, independent of how good the underlying
search engine itself is. The design is built around computing and
caching that allowed scope ahead of time, and accepting a small, bounded
staleness window in exchange for search staying fast.

Because a single search engine instance cannot practically hold and serve
an arbitrarily large, constantly-changing code corpus, the design also
needs a way to spread the indexed content and query load across many
search instances, and to keep that fleet rebalanced and up to date without
service interruption — none of which the search engine provides on its
own.

## <a id="use-cases">Use Cases</a>

Primary use cases:

* A logged-in Gerrit user searches code from the Gerrit UI and sees only
  project/ref results they are allowed to read.
* A logged-in Gerrit user can see which of the projects and branches they
  are allowed to read are currently indexed, so they can tell whether an
  empty result means "no match" or "not indexed yet."
* The solution works for large Gerrit installations — many projects, many
  branches, and a code corpus and query load larger than a single search
  engine instance should own — and scales horizontally as an installation
  grows, rather than being limited to small deployments.

## <a id="non-goals">Non-Goals</a>

* Replacing Gerrit's access control model with a separate authorization
  system.
* Exposing the underlying search engine directly to end users.

## <a id="acceptance-criteria">Acceptance Criteria</a>

* Users access search only through Gerrit, never directly against the
  underlying search engine.
* A Gerrit user's search results are always limited to projects and refs
  that user is allowed to read under Gerrit's real access control rules.
* A missing or invalid identity returns no matches, and never leaks match
  counts or the names of repositories/branches the caller cannot see.
* Because the set of readable projects/refs is derived ahead of time rather
  than checked synchronously on every query, there is a bounded, tunable
  delay between a Gerrit access-control change and that change taking
  effect in search results. Enforcement is pre-filter only — scope is
  computed and applied before search runs, not by re-checking each
  individual result against live Gerrit afterward — so this is a
  deliberate tradeoff, not a correctness gap (see
  [Background](#background)).
* The solution scales horizontally to large Gerrit installations, and
  growing or maintaining search capacity does not require downtime or a
  full rebuild of the index.
* A user can view which of their readable projects and branches are
  currently indexed, filtered the same way search results are — this
  listing never reveals projects/branches the user cannot read.
