---
title: "Solution 2 - Improving Assignee"
permalink: design-docs/attention-set-solution-2-improving-assignee.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution 2 - Improving Assignee

## <a id="overview"> Overview

This solution will focus on improving the assignee workflow so that it generally meets the
criteria specific by the use case, and so that assignee is generally more useful.

The solution consists of the following primary improvements:

1) Add an auto-assignee features either in core or via a plugin (which listens to Gerrit events and use the assignee APIs) to alter the current assignee.

2) Move the "Assigned reviews" section of the user's dashboard to the top.

3) Add assignee editing to dashboards.

Once the features above are implemented it should be possible to further continue to enhance
the workflows with any of the suggested following enhancements which this solution is not about.
As it does not seem essential to implement more than the features above to address the use case,
delaying further discussion about the details of the follow enhancements gives the community the
opportunity to gain experience with an improved assingee workflow before having to decide
an what is appropriate next.

Potential follow on enhancements:

F1) Eliminate the "reviewed flag"

F2) Add an auto-reviewed plugin to inversely coordinate the reviewed status with the assignee.

F3) Enhance the assignee feature to be able to support more than one user and make it configurable whether assignee must be only one user or not.

F4) Address many of the same "Deferred Enhancements" (Expectations, Snoozing...) from Solution 1

## <a id="detailed-design"> Detailed Design

### <a id="prioritizing attention"> Prioritizing Attention

I believe that vying for people's attention is a relationship of trust and thus it must be
approached carefully to avoid abusing it. I believe that this use case, and the existence of the assignee feature, are testaments to this commonly shared belief. In other words, I believe that the
more the total amount of time that a person's attention is requested can be reduced, the more that
person is likely to prioritize such attention requests.

In order to error on the side of being scarce about who is being asked to give attention to a
change, it can help to try and let a person review a change until that person feels like their concerns have been addressed before asking other people to prioritize reviewing it. While this is
not always the case, I think it makes for a good 90% default objective. I also believe that this helps the change improve in a more focused way as it avoids requesting too many opinions all at
once which could backfire and lead to a slower more chaotic evolution of the change.

Reviewers' votes are meant to indicate whether they think their concerns have been addressed. A +2
is meant to be the highest indication of this, while a -2 would give the lowest indication of this. So if a change has a -2 on it, assigning the change on new patchsets uploads to the reviewer with
the -2 will prevent demanding attention from other reviewers until the change no longer has the -2
on it. If the reviewer with the -2 upgrades their vote to a +1, then I believe it makes sense to try and assign the change to the "first" reviewer with a -1 on it, to see if the change now addresses their concerns, and so forth. Using the age of a vote can be an approximation to help identify the "first" reviewer within a specific voting level. If the user is the first to voice a concern about a change, it seems reasonable to encourage their concerns to be addressed first before before asking other reviewers to prioritize their attention on the change. The "oldest" vote may then be used as tie breaker between reviewers within the same voting level. The policy of assigning a change to the reviewer with the lowest oldest vote is the embodiment of this approach.

As a potential future enhancement, it might make sense to further break ties by first assigning
changes to reviewers with the lowest max voting ability. This would help break ties among those
reviewers have not yet voted and otherwise would likely rank the same within their voting level (no
votes). This would help avoid asking for attention early on from those whose attention is likely
more scare and whose attention is likely more expensive, by assigning changes to those with
approval (+2) abilities last.

## <a id="alternatives-considered"> Alternatives Considered

1) Moving the entire assignee feature to a plugin. This would be even better, however it requires
the extra work of making the change based plugin data storable and searchable from a plugin. This would be a good follow on improvement.

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Leverages existing code base
  a. No need to add more core APIs
  b. Does not remove existing APIs
  c. No need to add abilities to highlight users on change screen
  d. Does not introduce new unfamiliar icons or decorations to display on/near user names, which
     could detract from the attention they are trying to gather.
  e. No need to add abilities to highlight changes on dashboards
  f. Does not add another attention solution (there already are 2: "assignee" and "reviewed")
  h. Improves the assignee feature without competing or leaving it "behind"
2. Allows for a incremental feature development
  a. Users see improvements right away
  b. Approach can be adjusted easily if required
3. Leverages existing "attention prioritizing" terminology
  a. Assignee means something to users, even if they've never used Gerrit.
  b. Assignee reflects accurately the intent of the feature

Additionally if the plugin approach is used:

4. Allows for a incremental feature adoption
  a. May be not installed if desired
  b. May be installed partially only if desired (one plugin without the other)
  c. Can be upgraded or uninstalled without restarting Gerrit.
  d. Can be customized without having to get code submitted to Gerrit core.

Cons:

1. May interfere with current assignee use cases
  a. This is less likely as long as assignee is still a single user.
  b. If this is a case, then using a plugin allows this to not be the installed

Additionally if the plugin approach is used:

1. Is not one size fits all
2. Usage may not be consistent across all sites

## <a id="implementation-plan"> Implementation Plan

Add an auto-assignee features with the following default rules:

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

These rules can be adapted to behave more similarly to the way the do in "Solution 1" when the assignee feature supports more than on assignee.

Finally, whenever the plugin changes the assignee, it will post comments explaining why someone was
been assigned to the change.

## <a id="time-estimation"> Time Estimation

