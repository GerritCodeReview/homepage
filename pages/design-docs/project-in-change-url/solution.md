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

## <a id="implementation"> Implementation

**TBC**