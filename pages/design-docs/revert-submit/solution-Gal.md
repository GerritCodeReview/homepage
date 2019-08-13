# Solution - Gal's initial solution

## <a id="overview"> Overview

This solution suggests that instead of reverting by topic we will simply revert
by submission id. Users should be able to push a button that reverts all
 submissions that were made together.

## <a id="detailed-design"> Detailed Design

Firstly we should implement the query operator that allows querying by
submission id.

Once we have that, it is going to be possible to create a REST API endpoint for
reverting multiple submissions based on the submission id.

Secondary use case 2 requires also adding the information of the submission id
to changeInfo.

## <a id="solution-to-questions"> Solution to questions
1. It doesn't matter since we do not use topics for the reverts.
2. It doesn't matter since we do not use topics for the reverts.
3. This should not happen, reverts may fail but we can find it out in advance
and fail all the reverts.
4. It doesn't matter since we do not use topics for the reverts.
5. If the user does not see all the changes of a specific submission, we should
fail the revert of the entire submission.
6. This is an extreme corner case that doesn't apply to Android. I would
consider ignoring it, worst case scenario the pending changes would not be good.

### <a id="scalability"> Scalability

The solution would be scalable as long as users don't try to revert hundreds of
reviews together. In that case, it would be useful to implement secondary use case 1.

## <a id="alternatives-considered"> Alternatives Considered

Simply reverting by topics would not work since topics are not well defined.
Some changes might have multiple topics, topics can be added post-merge.
We can see the example detailed in the background that reverting a topic there
would not work.

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Simple enough to implement.
2. Intuitive for the users to simply revert all of the submission.

Cons:

1. Questions numbers 3,5,6 are essentially cons.
2. Later on cherry picking a topic would be complicated.

## <a id="implementation-plan"> Implementation Plan

1. Create a method that gets a changeId and returns submissionId.
2. Use that submissionId to query for all the changes of that submissionId. This
requires creating a new query operator.
3. Create a new backend endpoint that gets changeId and uses 1 and 2 to revert
all submissions of that submissionId. (Alternative, the backend endpoint can
also get submissionId directly, it might be less intuitive that way though).
4. That backend endpoint should revert all the submissions of that topic one by
one, in reverse order of submission.
5. That backend endpoint should also implement the solution of questions 3,5,6.
6. Once the backend is ready, there should be a button in every change that
allows reverting all changes of that submission.

## <a id="time-estimation"> Time Estimation

1+2 can take a week.

3-6 can take a couple of weeks.

