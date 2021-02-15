---
title: ""
permalink: design-docs/inter-plugin-communication-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Background

At Qualcomm we track non-git dependencies using change comments prefixed with
"Depends-on:" and a list of changes. We have a plugin ("depends-on") that can
read these comments during change queries and output a list of changes for CI
systems and other users to consume. CI systems want to ensure they include all
of a change's dependencies when validating the change.

When propagating changes across branches, we do not want to lose dependency
information. To ensure it is retained with the change, the depends-on plugin
listens for cherry-pick events and copies the change comment from the source to
the destination change. Because the comments can refer to a specific change #
and that change # is unlikely to satisfy the dependency on the destination
branch (due to which branches are included in manifests, etc), the depends-on
plugin converts the change numbers into Change-Ids (Iabc...). When a change with
a Change-Id dependency is returned in query results, CI systems consider the
change to have unresolved dependencies; i.e. a dependency on a logical change
that has yet to be propagated to the appropriate destination(s).

To unblock those changes with unresolved dependencies, we want to find the
equivalent propagated change for each logical change. When each change is found,
we want the Depends-on comment updated with the change number (potentially
replacing the Change-Id). We only want to remove the Change-Id once a change has
been found for each appropriate destination, thus unblocking the propagated
change and its propagated dependencies for CI.

Since non-git dependencies are not restricted to changes on the same branch or
project, they only make sense in the context of some grouping at a higher level
than a single git repo. A repo manifest file or git submodule superproject are
examples of ways to define a set of projects and branches that go together. That
set definition can be considered a deliverable. When considering the concept of
an appropriate destination, we think about sets of deliverables.

# Use-cases

## Use-case 1:

We want to create and use functionality specific to 3 areas: 1) understanding
and manipulating the "Depends-on" comments, 2) understanding and manipulating
manifest XML files in git repos on Gerrit servers, and 3) interacting with
proprietary systems that choose specific manifest repos/branches/files as
interesting.

#1 and #2 contain generic logic that is suitable for open source plugins. #3 has
logic that only makes sense in the context of one company. As such, we want to
publicly share 1 and 2, while keeping 3 internal to Qualcomm.

# Acceptance Criteria

Can share generic plugins with the community without sharing confidential
business logic.

No need for admins or plugin devs to perform any steps beyond "regular plugin
development".
