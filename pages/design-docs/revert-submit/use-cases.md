---
title: ""
permalink: design-docs/revert-submit-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use-case

Primary use case: Users should be able to revert multiple changes that were
submitted together.

Secondary use cases:

1. Show submission ID of changes in ChangeInfo, and expose it in the UI.
2. Add query operator to search by submission ID.

Need to decide which of the secondary use cases are necessary.

## <a id="acceptance-criteria"> Acceptance Criteria

Users can revert an entire submission.

## <a id="background"> Background

When reverting changes that were submitted together, it is important for users
to revert them together for the project to build, and also for the comfort of
not reverting one by one. The necessary feature is a button that searches all
the changes of a submission id, and reverting all changes of that submission id.

If we have the following example:

repo R1: change *T1* (topic "t1") -> change *D1*

repo R2: change *T2* (topic "t1, "t2")

repo R3: change *T3* (topic "t2)

The user submitted all of them together because they are dependant. The user will
also want to revert them together, if he wants to revert any of them.
The problem here is that revertion by topic id would not work since there are two
topics. Also, topics can be added post-submit, or reused for sets of changes.

#### <a id="questions"> Questions

1. What if some reverts succeed and then another one fails? Can this happen?
If a part of the revert of the topic succeeds and other part fails it might
cause serious issues.
2. What happens if a user doesn't have permission to see all changes of a
topic?
