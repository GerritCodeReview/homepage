# Solution - Gal

## <a id="overview"> Overview

This solution suggests writing a simple plugin that deletes the groups.

## <a id="detailed-design"> Detailed Design

Take all code in I3e323bcc2 and its related changes, and move that code into
a plugin named "Delete Groups".
Essentially, the plugin will have an endpoint that deletes a group.

It is only possible to delete a group if those are true:

1. The calling user is an administrator
2. The given group is not a system group
3. The given group is an internal group (it is assumed that we will not allowed
to delete external groups)
4. The given group is not the owner of any other group(s)

### <a id="scalability"> Scalability

There is no limitation on scale here.

## <a id="alternatives-considered"> Alternatives Considered

1. Write a script that deletes the groups. Not very clean but it is an option.

2. REST endpoint that deletes the group. By default, the endpoint should move the
group to refs/deletedGroups and also ensure that the deletion shows up in the
audit log. In order to create the usecase of this design, we can also add a
special option and a special gerritConfig that allows deleting the groups
completely. One problem with this, is the time for implementing this option. It
requires adding some functionallity that nobody asked for, and also editing the
creation of a new group (if the groups is in refs/deletedGroups, move it from
deletedGroups and connect it to the audit log of the previously created group).

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Simple and fast to implement.
2. Doesn't break the functionallity of groups such as audit log and always being
able to restore groups.

Con:

It is a plugin, and it requires maintenance.

## <a id="implementation-plan"> Implementation Plan

Since most of the code is already written, the plan is to migrate the current
code into a plugin. Also, need to just add documentation.

## <a id="time-estimation"> Time Estimation

This should not take more than a few days to implement, since most of the code is
already written.
