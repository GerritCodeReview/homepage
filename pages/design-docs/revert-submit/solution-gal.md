---
title: ""
permalink: design-docs/revert-submit-solution-gal.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Gal's initial solution

## <a id="overview"> Overview

This solution suggests that instead of reverting by topic we will simply revert
by submission id. Users should be able to push a button that reverts all
submissions that were made together.

## <a id="detailed-design"> Detailed Design

Firstly we should implement the query operator that allows querying by
submission id. We should implement it on the server-side only, but a it's a
nice-to-have to add an opeator for it so that users can use it as well.

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
2. Compared to a topic revert, users can not use this feature to revert any
combination of changes that were not submitted together.

## <a id="implementation-plan"> Implementation Plan

### Add necessary functionality to the original "Revert" endpoint

It is useful for the implementation of the new REST endpoint to add some features
to the original "Revert" endpoint. Those features will be added:

1. Ability to choose the parent commit of the commit that is being reverted (by
passing the SHA1 of the parent commit).

2. Ability to choose a topic name for the reverted commit, rather than take the
same topic as the parent's commit.

### Implement a UIAction to show a "Revert all" button

Implement a UIAction to show a "Revert Submission" button. The action will
perform checks such as permissions, and that the change is merged. This leaves
the possibility for false-positives (button shows but the action fails),
which is the result of a trade-off between performance and correctness.

### Implement a REST endpoint

The REST endpoint reverts all changes with the same submission ID. The endpoint
will first perform a number of checks to see if "Revert submission" is a legal
action on that change.

These conditions have to be met:

1. The change is found and merged.
2. The user has all necessary permissions.
3. All repositories of all changes are found.
4. There does not exist a change that is merged, not going to be reverted, and
dependant on a change that is going to be reverted.

It will then use the index to get all changes that have the same change ID and
run the aforementioned checks also on these changes.

Afterwards, the endpoint will figure out the ordering in which the changes
have to be reverted, by finding the dependancies between the changes and making
sure that the changes that have child changes be reverted first.

The next step is to revert the ordered list of changes one-by-one. This phase
will be retried on a per-change basis to ensure maximum fail-safety.

Each reverted change will be added to a topic with the following name:
"$originalTopicName-revert" if exists for the change. If topic doesn't exist, we
can generate a name based on the submission ID.

Each original change will be updated to link to its revert from the change
messages, similar to a singular revert.

The final HTTP response will contain a list of ChangeInfos that represent the
reverted changes.

(Optional) The endpoint will have a dry-run mode when 'dry-run' is passed as
parameter. It will report back both the status (success, failure) and a list of
changes that will get reverted if the dry run succeeds. This will allow the UI
to show a preview of what the action will do to the user. When dry run is
requested, the endpoint will do all the work required without the final write
action.

### Allow query submission ID (optional)

Also, we may need to expose the query by submission to the user, which means it
would be necessary to also reveal the submission ID in ChangeInfo and the UI.

## <a id="time-estimation"> Time Estimation

1-3 can take a week.

4-6 can take a week.
