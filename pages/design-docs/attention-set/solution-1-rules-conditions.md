---
title: "Design Doc - Attention Set - Solution 1 - Rules and Conditions"
sidebar: gerritdoc_sidebar
permalink: design-doc-attention-set-solution-1-rules-conditions.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/attention-set
---

# Solution 1 - Rules and Conditions

## <a id="overview">Overview

Users are added to and removed from the attention set based on rules and conditions.

## <a id="detailed-design">Detailed Design

#### Fundamental Rules

These rules cannot be changed or configured.

*   No rules are applied to WIP or merged changes, but you can still manually add users to the
    attention set even for WIP and merged changes.
*   Only the owner, uploader, reviewers and ccs can be in the attention set.
*   If a reviewer is added, then they are added to the attention set. This also applies to all
    reviewers of a newly uploaded change or of a change that leaves the WIP state.
*   The attention set is cleared when the change gets merged.
*   Publishing a change message (with or without comments or votes) will by default remove the user
    from the attention set, but a checkbox (boolean in the REST API) allows the user to override
    this and stay in the attention set.

Owners and reviewers can add or remove themselves and others to or from the attention set at any
time. They have to provide a reason.

#### Configurable Conditions

Being automatically added to the attention set is based on configurable rules with these simple
defaults:

*   Add the owner to the attention set whenever a reviewer publishes a change message (with or
    without comments or votes).
*   Add all reviewers to the attention set whenever the owner publishes a change message (with or
    without comments or votes).

If an owner or reviewer is removed from the attention set, then they get a list of rules attached to
them for being added back, which is configurable per host. But this list of rules is also editable
by owner and reviewers in the UI.

The following additional rules could be available for configuration and for UI changes. The list
might be extended or shortened during the implementation phase, e.g. if a condition is technically
hard to implement and a first version of the attention set can be successfully launched without it.

*   Time based conditions like "add this reviewer in 9h".
*   Vote based conditions like "add this reviewer when this other reviewer has granted a positive CR
    vote".
*   Change based conditions like "add the owner when all changes in the relation chain are ready to
    submit".
*   Checks based conditions like "add the owner/reviewer when all checks for the latest patchset
    have passed".

More conditions can be provided by plugins by hooking up into a new plugin endpoint (needs to be
defined in [implementation](solution-1-implementation.md)).

Conditions will likely be represented as strings, which need to parsed and interpreted (needs to be
refined in [implementation](solution-1-implementation.md)).

## <a id="alternatives-considered">Alternatives Considered

TBD (suggestions welcome)

## <a id="pros-and-cons">Pros and Cons

TBD (suggestions welcome)

## <a id="implementation">Implementation Plan and Time Estimation

Will be implemented by Google and be ready for the 3.2 release.
