---
title: "Design Doc - Attention Set - Solution 1 - Implementation"
permalink: design-docs/attention-set-solution-1-implementation.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/attention-set
---

*Please read these other parts of the solution before this doc:*

*   [Use Cases](/design-docs/attention-set-use-cases.html)
*   [Workflow](/design-docs/attention-set-solution-1-workflow.html)
*   [User Interface](/design-docs/attention-set-solution-1-user-interface.html)

# Solution 1 - Implementation

We believe that the implementation of the solution is either straightforward or warrants a separate
design doc, so we are not proposing any technical implementation details here, but instead collect a
list of technical questions that will have to be answered:

*   Where is the attention set stored?
*   Scalability, replication and multi-site consistency of the attention set storage.
*   Will updates be atomic with other metadata changes (reviewer and cc changes)?
*   What is the data structure for the attention set and its entries?
*   How does the REST API look like for attention set related operations?
*   Will there be dedicated plugin extension points for the attention set?
*   How is the attention set indexed and what are the supported search operators?
*   How are hosts migrated from assignee/reviewed based workflow to being attention set based?
*   Who should be allowed to change the attention set? Do we need another permission?
*   How can we support tools like
    [Go's maintner tool](https://godoc.org/golang.org/x/build/maintner) that rely on email
    notifications about uploaded patchsets?

## <a id="alternatives-considered">Alternatives Considered

We could have tried to write the attention set as a plugin, but we believe that tracking whose turn
it is is so fundamental to the code review process that we need to build the fundamental concepts
into core.

## <a id="implementation">Implementation Plan and Time Estimation

Will be implemented by Google and be ready for the 3.2 release.
