---
title: ""
permalink: design-docs/project-in-change-url-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Glossary

- **Change-Number**: the number assigned by a __Gerrit Primary node__
  to an incoming new change created on a repository.

- **Change-Id**: the SHA1 assigned by a __Git client__ (or __Gerrit Primary node__
  when changes are created online) to a new change created on a repository.

- **Document-Id**: the unique identifier assigned to a new Lucene entry
  created on an index.

# Problem: How to refer to a change in a globally unique way?

Back in the pre-NoteDb times, Gerrit changes were identified by a single
incremental number associated to a sequence in ReviewDb. There was at that
time only one *source of truth* which was the database; the sequence of
the change numbers was a *unique numbering source* for every change created.

The current behaviour, which is aimed to be preserved, is that changes
keep their Change-Number even when they are moved around to different branches,
because that information is contained in the associated NoteDb entry and
not in the ref-name.

Nowadays, Gerrit stores the Git data and the associated code-review metadata
inside the same data-store, which is the Git repository. The regular Git data
about Changes is stored under the usual `refs/changes/NN/CCCNN/PP` (where
`CCCNN` represents the change number, the `NN` the last two digits of the change
number and `PP` the patch-set) and the code-review metadata under
`refs/changes/NN/CCCNN/meta`. However, we are still tied to the legacy
constraint of having a *unique numbering source*, even if ReviewDb has been
removed a long time ago.

The problem arises when importing changes coming from different Gerrit servers
by leveraging the [`importedServerId` setting in Gerrit v3.7](https://gerrit-documentation.storage.googleapis.com/Documentation/3.7.0/config-gerrit.html#gerrit.importedServerId).

Even though Gerrit would easily __tolerate__ two changes having the same
change number, as showcased during the last [Gerrit User Summit 2022 in London](https://youtu.be/Su1OpJ_s850),
there are still some disruptions:

1. If the latest `refs/sequences/changes` number is smaller than the imported
   change numbers, the creation of new changes may clash with the existing
   imported changes, if created on the imported project.

2. The change numbers are used as __unique id__ in Lucene, which would
   make the searching of changes by id problematic. If two changes have the
   same number `CCCNN` then the Lucene search will be able to find only
   one of them.

The general problem can be formulated as:
__"How can we identify one Change in a way that is independent from where
it was created in the first place?"__

# Background

The Gerrit project decided back in 2016 to move away from a __change-number-only__
URL style and ported the REST-API and the GUI to consume the changes using a __project/change__
scheme, as you can see from [Change-Id: Ie3feee2e3](https://gerrit-review.googlesource.com/c/gerrit/+/108592).

The support for legacy __change-number-only__ URL style was left in the backend for
two reasons:

- Support older links posted to issue-tracking tools
- Give time for the frontend team to get rid of all references to __change-number-only__ URLs
  in the front-end.

# Use-case `UC1`

> *AS* A Gerrit user
> *GIVEN* A Gerrit server contains projects `P1`, and `P2` is imported from
> another server with a different `serverId`, having change numbers higher than
> the maximum one in `P1`
> *WHEN* A new change `C1` is created in `P1`
> *THEN* The change `C1` will not clash with any of the existing ones in `P1` or `P2`
> *AND* the Gerrit user will be able to perform any operation on it as usual

# Use-case `UC2`
> *AS* A Gerrit user
> *GIVEN* A Gerrit server contains projects `P1`, and `P2` is imported from
> another server with a different `serverId`, having change numbers higher than
> the maximum one in `P1`
> *WHEN* A new change `C2` is created in `P2`
> *THEN* The change `C2` will not clash with any of the existing ones in `P1` or `P2`
> *AND* the Gerrit user will be able to perform any operation on it as usual

# Use-case `UC3`
> *AS* A Gerrit user
> *GIVEN* A Gerrit server contains projects `P1`, and `P2` is imported from
> another server with a different `serverId`, having change numbers in common with `P1`,
> for example `C1` (from `P1`) and `C2` (from `P2`) have both change number `CN`
> *WHEN* the Gerrit user search for changes with the query `q=CN`
> *THEN* The result will contain both `C1` and `C2`

# Non-requirements

The current reverse lookup of `CN` to the tuple `Project`/`CN` may not return a unique
entry anymore, because of the possibility to have multiple projects with the same
change numbers.