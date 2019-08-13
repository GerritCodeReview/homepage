# Use-case

Primary use case: Users should be able to revert multiple changes that were
submitted together.

Secondary use cases:

1. Show submission id of changes in ChangeInfo, and expose it in the UI.
2. Add query operator to search by submission id.

Need to decide which of the secondary use cases are necessary.

## <a id="acceptance-criteria"> Acceptance Criteria

Users can revert an entire submission.

## <a id="background"> Background

When reverting changes that were submitted together, it is important for users
to revert them together for the project to build, and also for the comfort of
not reverting one by one. The necessary feature is a button that searches all
the changes of a submission id, and reverting all changes of that submission id.

#### <a id="questions"> Questions

1. What if some reverts succeed and then another one fails? Can this happen?
If a part of the revert of the topic succeeds and other part fails it might
cause serious issues.
2. What happens if a user doesn't have permission to see all changes of a
topic/submission?