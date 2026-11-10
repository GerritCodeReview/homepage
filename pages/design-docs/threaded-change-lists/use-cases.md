---
title: "Design Doc - Change Dependency Threads - Use Cases"
permalink: design-docs/threaded-change-lists-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/threaded-change-lists
---

# Change Dependency Threads - Use Cases

## <a id="summary"> Summary

Gerrit's review model encourages small changes stacked on one another. For
people and communities that work this way, the stack is the unit of work, but
Gerrit's change lists show a flat table ordered by update time. The structure
that tells an author what is blocked, and a reviewer what to read first, is
only visible one change at a time on the change page.

Communities that gate with Zuul add a second dependency kind, the `Depends-On`
footer, which crosses projects and branches and which Gerrit does not display
as a relationship at all.

We want dependency structure to be visible wherever changes are listed.

## <a id="background"> Background

### What Gerrit shows today

* **Change lists** (dashboards, search results) are flat. Rows are ordered by
  last update, so the members of one stack are interleaved with unrelated
  changes and with each other. Updating the third change of a five-change
  stack moves that row to the top and leaves the other four where they were.
* **The relation chain** on the change page shows Git ancestry for one change,
  tip first. It is computed per change by walking Git, which is appropriate
  for a single change page and too expensive for a list.
* **Topics** are shown as a column and in the "Same topic" and "Submitted
  together" panels. With `change.submitWholeTopic` a topic means "submit
  together", which is a different statement from "depends on".
* **Cross-project dependencies** have no representation. A `Depends-On` footer
  is text in a commit message.

### Dependency kinds

| Kind | Declared by | Scope | Known to Gerrit core |
|------|-------------|-------|----------------------|
| Git ancestry | The commit's parent | One project and branch | Yes, per change |
| Topic | Change metadata | Any | Yes, as a label; as submission unit when `submitWholeTopic` is on |
| `Depends-On` footer | Commit message | Any project or branch, including other servers | No (Zuul convention) |

`Depends-On` dependencies can form cycles, which Zuul supports deliberately for
changes that must land together across projects.

### How Zuul discovers dependencies

Zuul has to know the complete dependency network of a change before it can
enqueue it. Its Gerrit driver builds that network from outside by querying
Gerrit change by change: Git parents, footers, and reverse searches for
changes that name this one. The work is repeated as changes update. Gerrit
holds all the inputs and is better placed to answer the question once.

### Why now

Stack-heavy workflows are becoming more common, and stacks are getting longer.
Coding agents in particular produce well-factored series of many small changes
quickly, and people increasingly triage them from a phone. A flat list of
forty rows that is really six stacks is hard to work with at any width.

## <a id="use-cases"> Use cases

### Primary: authors and reviewers working with stacks

1. **See my stacks as stacks.** As an author with several stacks in flight, I
   want my dashboard to show each stack as one visual unit in dependency
   order, so I can tell at a glance which stacks exist and where each stands.

2. **Find what is blocking a stack.** As an author, I want to see the votes
   and status of every member of a stack next to each other in dependency
   order, so I can find the lowest change that is not yet approved or passing.

3. **Review in the right order.** As a reviewer, I want incoming changes shown
   base first, so I start with the change the rest depend on rather than the
   one most recently updated.

4. **See forks in a series.** As an author or reviewer, when two changes share
   a parent, I want to see them as siblings rather than as an ambiguous linear
   list.

5. **Consistent ordering on the change page.** As a user, I want the relation
   chain on the change page to read in the same direction as the change list,
   so that I do not have to mentally reverse one of them.

6. **See the whole stack from a search hit.** As a user whose search matches
   one member of a stack (for example a reviewer added to only one change, or
   a search by file or hashtag), I want to see the rest of that stack as
   context without running a second query.

7. **Work on a narrow screen.** As a user reading Gerrit on a phone, I want the
   dependency structure to remain legible and not consume the row.

8. **Act on a stack.** As a user, I want keyboard navigation and bulk selection
   to follow the order I see, so that selecting a run of rows selects a run of
   the stack.

9. **Do not conflate topics with dependencies.** As a user in a community that
   uses topics for "submit together", I want topic membership to be shown as
   its own thing, distinguishable from Git dependency. As a user in a
   community that puts a whole stack in one topic, I do not want topic display
   to hide the stack's structure.

### Primary: projects using cross-project dependencies

10. **See cross-project dependencies.** As an author or reviewer in a project
    using `Depends-On`, I want the change list and the change page to show that
    a change in one project depends on a change in another, so I know why it
    cannot merge yet without reading commit messages.

11. **See dependents, not only dependencies.** As the author of a change that
    other changes depend on, I want to see those dependents, including ones in
    other projects, so I know what my next patch set will affect.

12. **See cycles and broken references.** As a user, I want a dependency cycle
    or a `Depends-On` that does not resolve to be visible as such, because
    both change whether and how the change can merge.

### Secondary: tools and integrators

13. **One answer for the dependency network.** As a CI system (Zuul), an agent
    or a command-line tool, I want to ask Gerrit for the full dependency
    network of a change in one request, with typed edges, instead of
    reconstructing it through many queries. The answer should match what the
    UI shows.

14. **Other dependency sources.** As a plugin author for a different CI system
    or integration, I want to contribute my own dependency relationships to
    the same display without reimplementing list rendering.

15. **Dependencies on changes from another server.** As a user of a Gerrit that
    mirrors or tracks changes from another Gerrit, I want a `Depends-On` URL
    naming the upstream server to resolve to the local copy of that change.

### Constraints from operators and maintainers

16. **No cost for people who do not use it.** As an administrator, I need
    change list queries to stay on the index-only path, with no Git or NoteDb
    access per row, for all users and regardless of whether the feature is
    enabled. Dashboard preloading must keep working.

17. **Safe rollout.** As an administrator of a multi-node site, I need to
    deploy this across a rolling upgrade and a reindex without the UI
    requesting something a backend cannot serve.

18. **Optional.** As a user or a host that does not work in stacks, I do not
    want the default change list to change.

19. **Permissions.** As an administrator, I need dependency display to reveal
    nothing about changes the caller cannot see, including their existence.

## <a id="acceptance-criteria"> Acceptance Criteria

* A user can opt in to seeing change lists as dependency threads, base first,
  with members of a stack contiguous. The default list is unchanged.
* The relation chain follows the same orientation when the user has opted in.
* Enabling the feature adds no Git or NoteDb reads to change list queries.
  Existing tests asserting index-only list queries continue to pass with the
  feature enabled, and dashboard preload URLs match the runtime requests.
* Changes not visible to the caller never appear, and never influence what is
  displayed.
* Keyboard navigation and bulk actions follow display order. Result counts and
  pagination remain correct: no query match is skipped or double counted.
* Topic grouping and dependency threading can be enabled independently.
* A plugin can supply additional typed edges, and a slow or failing plugin
  does not block or break the native display.
* With a suitable plugin installed, `Depends-On` relationships between changes
  on the same server appear in the change list and the relation chain,
  including across projects.
* A client can retrieve the dependency network of a change, including reverse
  dependencies, in a single request.
* The feature can be rolled out on a multi-node installation without a window
  in which frontends request data that backends cannot provide.

## <a id="non-goals"> Non-goals

* Changing submit semantics, submit order enforcement, or `submitWholeTopic`.
* Teaching Gerrit core the meaning of `Depends-On`. The footer remains a
  convention owned by whoever interprets it.
* Scheduling or gating. Gerrit reports the network; CI decides what to do.
* Replacing the relation chain or the "Submitted together" panel.
* Computing transitive closures or branch reachability in list queries.
