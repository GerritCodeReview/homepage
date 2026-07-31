---
title: "Design Doc - Zoekt-Based Code Search for Gerrit - Use Cases"
permalink: design-docs/zoekt-search-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/zoekt-search
---

# Zoekt-Based Code Search for Gerrit - Use Cases

Gerrit has no built-in way to search code content across repositories and
branches. Users need to search across the repositories and branches they
are allowed to read, with results respecting Gerrit's existing project and
branch/ref access rules, including private or restricted refs, and the
solution must work for large installations with many repositories and
branches.

## <a id="use-cases">Use Cases</a>

Primary use cases:

* A logged-in Gerrit user searches code from the Gerrit UI and sees only
  project/ref results they are allowed to read.
* A logged-in Gerrit user can see which of the projects and branches they
  are allowed to read are currently indexed, so they can tell whether an
  empty result means "no match" or "not indexed yet."
* A site administrator can enable code search for a large Gerrit
  installation with many projects, many branches, and growing query load,
  without limiting the feature to small deployments.

Secondary use cases:

* A logged-in Gerrit user can access code search through an API, with the
  same authentication, authorization, and visibility behavior as the UI.
  This supports higher-level tools such as automation and coding agents.
* A logged-in Gerrit user can search or page through the indexed
  project/branch coverage that they are allowed to see, so installations
  with many indexed repositories remain usable.
* A logged-in Gerrit user can see whether a readable project/branch is
  indexed from repository and branch views where that status is relevant.
* Administrators or project owners can configure which projects and
  branches are indexed.

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
* There is a documented, bounded delay between a Gerrit access-control
  change and that change taking effect in search results.
* There is a documented, bounded delay between a branch update and updated
  content appearing in search results.
* The solution scales horizontally to large Gerrit installations, and
  growing or maintaining search capacity does not require downtime or a
  full rebuild of the index.
* A user can view which of their readable projects and branches are
  currently indexed, filtered the same way search results are — this
  listing never reveals projects/branches the user cannot read.
* Indexed project/branch coverage can be searched or paginated so the
  listing remains usable for large installations.
* Administrators or project owners can configure indexed project/branch
  coverage without requiring code changes.

## <a id="background">Background</a>

A dedicated code search capability is useful only if users can trust that
it follows the same visibility rules as the rest of Gerrit. Search must not
become a side channel for discovering private repositories, restricted
branches, file paths, match counts, or recently removed access.

Users also need to understand what search coverage exists. If a repository
or branch has not been indexed, an empty result should not be confused with
"there are no matches." This matters especially while rolling search out
incrementally across a large installation.

For administrators and project owners, search coverage needs to be
manageable. They need a way to configure which projects and branches are
indexed, understand current indexing status, and roll out broader coverage
without disrupting users.
