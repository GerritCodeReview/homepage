# Use-case

Primary use case: Users should be able to revert multiple changes that were
submitted together.

Secondary use cases:

1. Show progress of reverts to user.
2. Show submission id of changes in ChangeInfo, and expose it in the UI.
3. Add query operator to search by submission id.

Need to decide which of the secondary use cases are necessary.

## <a id="acceptance-criteria"> Acceptance Criteria

Users can revert an entire submission.

## <a id="background"> Background

Android users have reported using the *topic* feature often for submitting
multiple changes together and across repositories. Submission of multiple
changes simultaneously is useful, but sometimes they also need to revert
multiple changes simultaneously for the project to build, and also for the
comfort of not reverting one by one. The necessary feature is implementing a
button that searches all the changes of a specific submission id, and reverting
all changes of that submission id.

If we have the following example:

repo R1: change *T1* (topic "t1") -> change *D1*

repo R2: change *T2* (topic "t1", "t2")

repo R3: change *T3* (topic "t2")

And the user wants to submit all changes of topic “t1”, they will also
automatically submit *D1* and *T3* additionally (*T1* depends on *D1*, and *T3*
share a topic with *T2*, and they shouldn’t be split).

#### <a id="questions"> Questions

1. What if a user adds a topic to an already merged change? It will have a
different submission id.
2. What if a user submits (in the example above) T2 without submitting the
rest of the changes? It will have a different submission id.
3. What if some reverts succeed and then another one fails? Can this happen?
If a part of the revert of the topic succeeds and other part fails it might
cause serious issues.
4. Topic names are not unique. Do we need to address that?
5. What happens if a user doesn't have permission to see all changes of a
topic/submission?
6. Suppose a user submitted a few changes together, and some of them were
topic T1 and some of them were topic T2. Now suppose the user wants to revert
this submission, but the user enabled the option submitWholeTopic just now.
What should happen? Should this corner case even be considered?
