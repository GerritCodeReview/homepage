---
title: "tree API endpoint"
sidebar: gerritdoc_sidebar
permalink: design-docs-tree-api-endpoint-doc.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/tree-api-endpoint
---

*Author: hammad.afzali@gmail.com - Last updated: 2019-07-19*

## Objective

Add a new REST API to retrieve Git tree objects from the Gerrit server.
This will be essential to efficiently support client-side commit/review
signing, and thus to provide an important security feature in Gerrit.

## Background

Gerrit does not support user digital signing for commits/reviews
done through the Web UI, a feature that is desirable in order to combat
many recent cybersecurity incidents that have plagued the various
steps of software development chains.

Such a feature can be implemented with no changes to Gerrit,
i.e. as a browser extension. As a matter of fact, the author of this
document has already designed and implemented
[le-git-imate](https://dl.acm.org/citation.cfm?id=3196523), a browser
extension to provide user commit signatures for web-based Git
repository hosting services such as GitHub and GitLab.

For seamless interaction with the API, the extension would require a
tree API endpoint. However, Gerrit does not provide any APIs to
retrieve the contents of a directory in a repository. Note that the
proposed API is standard in web-based Git hosting repositories such as
GitHub and GitLab.
The ability to efficiently retrieve the directory structure of a Gerrit
(i.e., Git) repository is essential in order to add security
functionality for such repositories.

The proposed API also helps any project that seeks to retrieve the
directory structure of a repository on Gerrit. For example, there are
discussions on a google discussion forum and also on Stackoverflow in
which people asking for such a tree API to list files in a directory,
or to retrieve a directory structure.

## Design

The new REST API endpoint will allow users to fetch trees through:
`GET /changes/{change-id}/revisions/{revision-id}/tree`.

The API provides two options: (1) recursive, (2) path.
With the first option, trees of a revision can be retrieved
recursively. The latter one allows to get the trees of a specific
path in the repository.

As a future plan, retrieving trees by tree-id could be added
to this API, if existing APIs like
`/projects/{project-name}/commits/{commit-id}` or
`/changes/{change-id}/revisions/{revision-id}/commit`
include the tree-id in their response.

## Alternatives Considered

One alternative solution is to connect directly to the Git server
underneath the Gerrit server. Doing so, we can retrieve the tree
objects and therefore the directory structure for a project. However,
this approach lacks the good performance. Our analysis shows this
approach could be 10 times slower than a similar REST API.
That happens because Git retrieves many unnecessary objects
via the git pack protocol. Depending on the repository and the
information provided on the client side, we may end up fetching
hundreds of objects to read only one tree object.

Another alternative is to use an existing Gerrit plugin, called
[gitiles](https://gerrit.googlesource.com/plugins/gitiles/). Having
gitiles installed on the Gerrit server, it is possible to get the
directory structure of a repository. However, relying on a server-side
plugin, we have to consider the following challenges:
- Retrieving a tree object needs only a small part of the gitiles
plugin. Thus, it may be overkill to have to install a plugin with
complex functionality just for one simple API.
- Users would need to have admin privileges in order to make
server-side changes (i.e., install the server-side gitiles plugin).
This assumption may not always be true.

## Implementation Plan

The author of this document will implement the new tree API. This
feature has a high priority for his project, which seeks to incorporate
digital signatures for commits/reviews done though the web UI.

## Time Estimation

The project will be done in four phases : Design, Implementation, Test,
and Integration. Each phase will take approximately one week to be
completed.

## Done Criteria

- Code implemented
- Unit tests passed
- Code compiled and verified in CI
- Documentation completed
- Code peer reviewed and accepted
