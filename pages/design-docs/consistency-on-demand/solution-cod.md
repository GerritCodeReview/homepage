---
title: "Consistency on Demand"
permalink: design-docs/consistency-on-demand-solution-cod.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Consistency on Demand

## <a id="overview"> Overview

To ensure consistency we will use the Git commit graph for ordering.
If within a datacenter, a given SHA-1 exists in the history for a given ref,
that means the data replicated to the datacenter.

## <a id="detailed-ideas"> Design Ideas

### <a id="generic-cod"> Generic CoD
Consistency-on-Demand in Gerrit takes the following form:
1. Each outgoing write request will contain headers, reflecting all refs that
were updated: `X-Gerrit-UpdatedRef: REPONAME~REFNAME~SHA-1`.
1. Each incoming request may specify multiple headers:
`X-Gerrit-NeedRef: REPONAME~REFNAME~SHA-1`.
1. The header may only be used on authenticated requests.
1. The SHA-1 must have been involved in a ref transaction; all the SHA-1s
returned from `X-Gerrit-UpdatedRef` qualify.
1. When specified, the serving task ensures that the given SHA-1 parameter was
part of a ref transaction, through a sequence of fast-forward updates to the
ref. If SHA-1 was not seen, we return status 412, or 404 if SHA-1 was
overwritten a transaction through a non-FF update. If the client receives 412,
it should wait and retry.
1. For diagnostics, we emit an error message describing the failing requirement:
`X-Gerrit-NeedRef-Failed: REPONAME~REFNAME~SHA-1`.
1. For a refs/changes ref, we do not check the ST-BTI document for staleness.
This is a possible future extension.
1.  A client that wants to execute a sequence of write actions, can pass
`X-Gerrit-UpdatedRef` of the previous action into `X-Gerrit-NeedRef` of the next
action.
1. A deletion results in a UpdatedRef SHA-1 of 00000000...
1. A NeedRef of 000000.. should be interpreted as “the ref must not exist”.

### <a id="submission-cod"> Submission CoD

Gerrit will offer a batch submit endpoint to submit any number of changes in a
batch.
This batch submit endpoint will be similar to the original submit method.
Same as the submit method, It will include a common submission_id to ensure
submodule updates are grouped, and allow reverting a batch submission.

Some differences / reasons this endpoint is needed:
1. Topics will be disregarded (even when submitWholeTopic = true on the host),
to make ST-BTI replication lag irrelevant for submissions. Currently, we query
ST-BTI for a list of changes to submit using topic query, which is prone to
replication lags.
1. If trying to submit change 1 which depends on change 2, but change 2 is not
part of the input, the batch submission should fail; we shouldn’t submit changes
that are not part of the input.
1. The batch submission endpoint can specify an arbitrary number of
preconditions in the request body (see Input below) as opposed to the request
header for all other endpoints. This is needed because of size limitations of
request headers (at Google we have a limitation of 16 KiB).

#### <a id="submission-cod-path"> Path
'POST /changes/batch_submit'

#### <a id="submission-cod-input"> Input
BatchSubmitInput entity that will be the same as SubmitInput except that it
would also have:
1. List of changes that should be submitted.
1. List of preconditions that must be true. If any condition isn’t true, the
submission will fail similarly as for the generic CoD.

#### <a id="submission-cod-output"> Output
BatchSubmitInfo entity that will contain:
1. onBehalfOf (similar to SubmitInfo).
1. Mapping of change ids that were attempted to be submitted or submitted to
their status.
1. List of exceptions with their messages that were thrown while trying to
submit the changes.
1. List of updated refs, similar to the response in the header for all other
responses as described in the generic CoD section.


## <a id="detailed-design"> Detailed Design

Take all code in [I3e323bcc2](https://gerrit-review.googlesource.com/c/gerrit/+/245329)
and its related changes, and move that code into a plugin named "Delete Groups".
Essentially, the plugin will have an endpoint that deletes a group.

It is only possible to delete a group if the following prerequisites are met:

1. The calling user is an administrator
1. The given group is not a system group
1. The given group is an internal group (it is assumed that we will not allow
to delete external groups)
1. The given group is not the owner of any other group(s)
1. The given group is not a member of any other group(s)
1. The given group is not mentioned in any project's ACLs

If prerequisites are not met error message describing the root cause will be
presented to the user e.g. _Group "foo" cannot be deleted since it owns groups
"bar", "pub"_.

### <a id="scalability"> Scalability

There is no limitation on scale here.

## <a id="alternatives-considered"> Alternatives Considered

1. Write a script that deletes the groups. Not very clean but it is an option.

1. Plugin REST endpoint that deletes the group. By default, the endpoint should
move the group to `refs/deleted-groups` and also ensure that the deletion
shows up in the audit log. We could also add a configuration option that allows
deleting the group completely. One problem with this is the time for implementing this
option. It requires adding some functionality that nobody asked for, and also editing the
creation of a new group (if the group is in `refs/deleted-groups`, move it from
`deleted-groups` and connect it to the audit log of the previously created group).

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Simple and fast to implement.
1. Doesn't break the functionality of groups such as audit log and always being
able to restore groups.

Cons:

1. It is a plugin, and it requires maintenance.
1. Before it could become a core plugin group deletion operation would have to
be recorded in the audit log.

## <a id="implementation-plan"> Implementation Plan

Since most of the code is already written and proposed for review as a core REST
API, the plan is to migrate that code into a plugin. Also, need to just add documentation.

## <a id="time-estimation"> Time Estimation

This should not take more than a few days to implement, since most of the code is
already written.
