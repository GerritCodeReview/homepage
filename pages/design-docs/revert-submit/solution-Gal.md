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
and fail all the reverts. Although this should not happen, it might still happen
in unique cases, such as storage exception. To solve this, we can retry the
individual reverts. This will increase the success rate, while not providing any
guarantee.
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

1. Create a new backend endpoint that gets changeId and finds the submissionId
using that changeId, and then queries for all the changes using that submissionID.
2. That backend endpoint should revert all the submissions of that topic one by
one, in reverse order of submission.
3. Check permissions, check that the change is found and merged, check that all
repositories are found. Also need to make sure that there is no change that is 
merged, not going to be reverted, and is depandant on a change that is going to
be reverted.
4. Once the backend is ready we can add a UIAction that does the revert to the
entire submission. We will show the button only when the change is merged. It
will not take long to compute whether to show the button, but it might take long
to compute once the button is pushed. 
5. Also, we may need to expose the query by submission to the user.
6. If we implement 4, we may need to reveal the submission id through the UI, and
through ChangeInfo.

## <a id="time-estimation"> Time Estimation

1-3 can take a week.

4-6 can take a week.

