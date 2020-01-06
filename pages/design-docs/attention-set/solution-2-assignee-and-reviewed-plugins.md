---
title: "Solution 2 - Assignee and Reviewed Plugins"
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution 2 - Assignee and Reviewed Plugins

## <a id="overview"> Overview

1) Add an auto-assignee plugin which listens to Gerrit events and use the assignee APIs to alter the
current assignee.

2) Add a assignee-unreviewed plugin which listens to Gerrit events and use the reviewed APIs to mark a change unreviewed when a user is assigned to it, and to mark it reviewed when the user is unassigned the change.

3) Add assignee editing to dashboards.

4) Enhance the assignee feature to be able to support more than one user and make it configurable whether assignee must be only one user or not.

5) Address many of the same "Deferred Enhancements" (Expectations, Snoozing...) from Solution 1

## <a id="detailed-design"> Detailed Design

Add an auto-assignee plugin with the following default rules:

In order to help the user, we propose to apply useful default modifications to the assignee when standard review events happen. Each of the following defaults can be overridden when executing
the action in the user interface:

*   When the first reviewer is added they are assigned to the change
*   When someone other than the owner uploads a patchset the owner is assigned to the change.
*   When a change is submitted or abandoned the change is unassigned.
*   Replying (commenting, voting or just writing a change message) will assign the change to a new
    user if the replying user was currently assigned the change.
    *   When a *reviewer* replies assign the owner to the change. Refinements:
        * If the reviewer is replying with a positive vote, assign the change to the reviewer with the lowest oldest vote.
    *   When the *owner* (or uploader) replies assign the change to the reviewer with the lowest
        oldest vote.

The above defaults are also applied when using the API (but can also be overridden). For example if
the reviewers-by-blame plugin adds a reviewer, then that if that is the first reviewer, assign them to the change.

The upload of a new patchset by itself is **not** associated with a default change of the assignee. The owner may want to upload intermediate states or want to wait for CI systems before re-assigning a reviewers.

These simple defaults are not expected to do the right thing in 100% of the cases, just maybe 90%.
The owner of a change is still expected to manage the assignee individually and make sure that
it reflects their expectations.

There are some special cases to be considered:

*   Work in Progress (WIP): When a change leaves WIP state with reviewers, then the reviewer with
    the lowest oldest vote is assigned to the change
    When a change enters WIP state, the change is assigned to the owner.
    While a change is in WIP state the defaults above for assigning changes to users are not applied.
*   Merged and Private Changes: Will be handled with the same defaults as normal changes.

Finally, these rules can be adapted to behave more similarly to the way the do in "Solution 1" when the assignee feature supports more than on assignee.

## <a id="alternatives-considered"> Alternatives Considered

1) Moving the assignee feature to a plugin. This would be even better, however it requires the
extra work of making the change based plugin data storable and searchable from a plugin. This would be a good follow on improvement.

2) Using the same evolutionary approach without plugins. While this would eliminate some cons, it would also eliminate many (likely more) of the pros of the current solution.

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Leverages existing code base
  a. No need to add more core APIs
  b. Does not break existing APIs
  c. No need to add abilities to highlight users on change screen
  d. Does not introduce new confusing icons or decorations to display on/near user names, which
     could detract from the attention they are trying to gather.
  e.  No need to add abilities to highlight changes on dashboards
  f. Bolding a change on a dashboard is a very obvious and well understood way to make it standout
      as needing attention.
  g. Does not add another attention solution (there already are 2: "assignee" and "reviewed")
  h. Improves the assignee and reviewed features without competing or leaving them "behind"
2. Allows for a incremental feature development
  a. Users see improvements right away
  b. Approach can be adjusted easily if required
3. Allows for a incremental feature adoption
  a. May be not installed if desired
  b. May be installed partially only if desired (one plugin without the other)
  c. Can be upgraded or uninstalled without restarting Gerrit.
  d. Can be customized without having to get code submitted to Gerrit core.
4. Does not introduce any new confusing terminology to the user
  a. Assignee means something to users, even if they've never used Gerrit.
  b. Assignee reflects accurately the intent of the feature

Cons:

1. Is not one size fits all
2. Usage may not be consistent across all sites

## <a id="implementation-plan"> Implementation Plan


## <a id="time-estimation"> Time Estimation

