# Solution - Gal's initial solution

## <a id="overview"> Overview

This solution suggests that instead of reverting by topic we will simply revert
by submission id. Users should be able to push a button that reverts all
submissions that were made together.

## <a id="detailed-design"> Detailed Design

Firstly we should implement the query operator that allows querying by
submission id. We should implement it on the server-side only, but a it's a
nice-to-have to implement it on the client-side as well.

Once we have that, it is possible to create a REST API endpoint for reverting
multiple submissions based on the change id. This endpoint would find the
submission id of the change, and then query by submission id to get the rest
of the changes that should be reverted.

Secondary use case 2 requires also adding the information of the submission id
to changeInfo.

## <a id="solution-to-questions"> Solution to questions

1. This should not happen, reverts may fail but we can find it out in advance
and fail all the reverts.
2. If the user does not see all the changes of a specific submission, we should
fail the revert of the entire submission.

### <a id="scalability"> Scalability

There are no limitations on the input.

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

1. Later on cherry picking a topic would be complicated.

## <a id="implementation-plan"> Implementation Plan

1. Create a method that gets a changeId and returns submissionId.
2. Use that submissionId to query for all the changes of that submissionId. This
requires creating a new query operator.
3. Create a new backend endpoint that gets changeId and uses 1 and 2 to revert
all submissions of that submissionId.
4. That backend endpoint should revert all the submissions of that topic one by
one, in reverse order of submission.
5. Once the backend is ready, there should be a button in every change that
allows reverting all changes of that submission.

## <a id="time-estimation"> Time Estimation

1+2 can take a week.

3-5 can take a couple of weeks.

