---
title: "Design Doc - Attention Set - Solution 1 - Implementation"
sidebar: gerritdoc_sidebar
permalink: design-doc-attention-set-solution-1-implementation.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/attention-set
---

*Please read these other parts of the solution before this doc:*

*   [Use Cases](use-cases.md)
*   [Workflow](solution-1-workflow.md)
*   [User Interface](solution-1-user-interface.md)

# Solution 1 - Implementation

TBD.

List of technical questions that this design has to answer (suggestions for more are welcome):

*   Where is the attention set stored?
*   Will there be a config option to turn Attention Set off?
*   Will updates be atomic with other metadata changes (reviewer and cc changes)?
*   What is the data structure for the attention set and its entries?
*   How does the REST API look like for attention set related operations?
*   Will there be dedicated plugin endpoints for the attention set?
*   What is the data structure for specifying snoozing conditions?
*   How are we hooking up into relevant events for snoozing?
*   How is the attention set indexed and what are the supported search operators?
*   How are hosts migrated from assignee/reviewed based workflow to being attention set based?

## <a id="overview">Overview

## <a id="detailed-design">Detailed Design

## <a id="alternatives-considered">Alternatives Considered

We could have tried to write the attention set as a plugin, but we believe that tracking whose turn
it is is so fundamental to the code review process that we need to build the fundamental concepts
into core.

## <a id="pros-and-cons">Pros and Cons

## <a id="implementation">Implementation Plan and Time Estimation

Will be implemented by Google and be ready for the 3.2 release.
