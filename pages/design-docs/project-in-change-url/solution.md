---
title: ""
permalink: design-docs/project-in-change-url-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Overview

The proposed solution is an evolution of what has been already implemented
in Gerrit towards the identification of changes with a project-specific URL.

## Data changes

The unique identifier of Change is changed from **Change-Number** to the **Project-Name**/**Change-Num**.

This impacts the following stores:

- `All-Projects:refs/sequences/changes` keeps on counting the changes created on the
  `All-Projects` repository. All other repositories have a `refs/sequences/changes` that
  keeps the counter of the changes inside the repository.

- `open` and `closed` indexes in Lucene use **Project-Name**/**Change-Num** pair as
  **Document-Id** and the index version number is bumped for triggering a migration.

## TODOS

1. `refs/starred-changes` in `All-Users` references **Change-Number** without the **Project-Name**.
   Example: `refs/starred-changes/DD/NNNDD/AAAAAAA` where `NNNDD` is the **Change-Number** and **AAAAAAA**
   is the **Account-Number**.

2. `refs/draft-comments` in `All-Users` references **Change-Number** without the **Project-Name**.
   Example: `refs/draft-comments/DD/NNNDD/AAAAAAA` where `NNNDD` is the **Change-Number** and **AAAAAAA**
   is the **Account-Number**.

3. Reindexing changes by **Change-Number**-only won't be possible anymore: did that make any sense
   before?

   Reindexing changes by Change-Number only was already inherently broken since v3.0.
   The reason is that the Change-Number alone does not allow to identify the Project-Name associated
   since the removal of ReviewDb in Gerrit v3.0.

   Gerrit relies on the index to lookup by __legacy_id__, populated with the Change-Number, and find
   out the Project-Name. However, the purpose of reindexing a change is to create a brand-new entry
   which may not exist in the first place. How could therefore this API work without providing the
   Project-Name? Effectively, it was not working most of the times, unless the index already existed
   and the reindex was just about the other fields to be refreshed.

## <a id="implementation"> Implementation

**TBC**