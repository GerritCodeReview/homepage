---
title: "Design Doc - Attention Set - Solution 1 - Workflow"
sidebar: gerritdoc_sidebar
permalink: design-doc-attention-set-solution-1-workflow.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/attention-set
---

# Solution 1 - Workflow

## <a id="overview">Overview

We propose to extend the “Assignee” feature into an “Attention Set” and drop the “Reviewed” feature.

## <a id="detailed-design">Detailed Design

The attention set is a set of account IDs along with some additional metadata (e.g. timestamp of
last change, reason for being added, conditions for future change). Only the owner, reviewers and
ccs can be in the attention set.

We are establishing the attention set as a first class citizen of the review process by building a
user interface that emphasizes its importance, e.g. adding a “needs attention” dashboard section. We
are phasing out the term “assignee” and we are dropping support for the
[Reviewed](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#mark-as-reviewed)
feature and its
[associated bolding](https://gerrit-review.googlesource.com/Documentation/dev-stars.html#reviewed-star)
of dashboard rows. The user interface design is refined in
[Solution 1 - User Interface](solution-1-user-interface.md).

The attention set can be changed manually at any time by anyone. When adding to or removing from the
attention set you have to provide a reason.

The owner and the reviewers that are not in the attention set have conditions associated when they
will be added back to the attention set. Some of these conditions are checked automatically, for
example all reviewers are added when the owner publishes a comment. The design of rules and
conditions is refined in [Solution 1 - Rules and Conditions](solution-1-rules-conditions.md).

The upload of a new patchset is not considered a signal for changing the attention set in any way.
Also email notifications for new patch sets will be not be sent by default anymore.

## <a id="alternatives-considered">Alternatives Considered

We could have tried to write the attention set as a plugin, but we believe that tracking whose turn
it is is so fundamental to the code review process that we need to build the fundamental concepts
into core.

## <a id="pros-and-cons">Pros and Cons

TBD (suggestions welcome)

## <a id="implementation">Implementation Plan and Time Estimation

Will be implemented by Google and be ready for the 3.2 release.
