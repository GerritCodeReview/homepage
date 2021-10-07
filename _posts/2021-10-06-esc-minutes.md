---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-10-06-esc-minutes.html
summary: "Minutes from the ESC meeting held on Oct 6, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---



## Engineering Steering Committee Meeting, Oct 6, 2021

### Attendees

Full meeting: Han-Wen Nienhuys, Luca Milanesio, Saša Živkov, Patrick Hiesel, Simply Chris

Discussion about ref caching: Matthias Sohn, Gal Paikin, Jacek Centkowski

### Place/Date/Duration

Online, Sep 9, 11:15 - 12:00 CET

### Next meeting

Nov 3, 2021

## Minutes

### Action items

Matthias, Patrick, Jacek and Luca will further evolve the ref cache change.

### RefCache to solve slow account loading and enable draft migration

We discussed https://bugs.chromium.org/p/gerrit/issues/detail?id=14945 and agreed that
the RFC in https://git.eclipse.org/r/c/jgit/jgit/+/186205 is the preferred solution.

There are remaining unknowns to be sorted out:
1) Is the JGit API thread safe in all implementations
2) How can the cache be evicted from the outside?
3) How can we ensure atomic cache updates for BatchRefUpdates?

Matthias, Patrick, Jacek and Luca will help resolve these issues and get the change submitted
within a target of 4 weeks.

The slow account loading problem affects all installations with being a real problem just for
installations that use NFS (trustFolderStat=false).

### Chris/Albert Swap

Chris will take over one of Google's ESC seats from Albert.

### Virtual User Summit 2021

Luca shared a draft proposal for a 2021 virtual user summit. The consensus was that we find
it a good idea to do a summit this year. Patrick noted that it would be good to cut down the
agenda to fit into 2x3hrs instead of 2x4hrs.

### Roadmap

Google will publish their quarterly objectives soon.

### Design/Open bugs

We pinged the cross-plugin proposal once more to see if there is progress or it should be
abandoned.
