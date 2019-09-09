# Solution - Gal's initial solution

## <a id="overview"> Overview

This solution suggests taking some of the useful code written for CCR and rewrite
it in a way that could be used in upstream Gerrit. It requires some significant
changes.

## <a id="detailed-design"> Detailed Design

First, we will create a simple and straightforward way to grant permissions to
a user. Right now, if we would grant or block permissions we need to perform
those actions on groups and then assign the user to be a part of that group. It
would be useful to create simple class that can create a user with a specific set
of permissions without depending on the groups. It may be possible to just use
a plugin: singleusergroup.

Secondly, for each REST endpoint we would create tests that ensure that the
request succeeds iff it has all necessary permissions.

For some endpoints, it would be necessary to add additional setup.

### <a id="scalability"> Scalability

There is no limitation on scale here. It is also possible to add future endpoints
and then test permissions for them efficiently.

## <a id="alternatives-considered"> Alternatives Considered

One alternative is to test the permissions manually for each endpoint, one by one.
This solution is time consuming for the current endpoints and even more so for
future endpoints. Since we have about 200 endpoints and each endpoint can require
around 2-3 permissions, meaning we would need around 3 tests for each endpoint,
it would require over 500 tests.

Second alternative is simply not to check for permissions, and it is clear that
it could expose Gerrit to security leaks.

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Scalable and useful for future permission testing.
2. Could find potential security issues of current and future endpoints.

Cons:

1. Some of the endpoints that will be added in the future might require additional
setup for the test to work (you can't delete a reviewer without setting a reviewer
first).
2. The permission system in Gerrit is more complicated than the IAM permission
system, so it might be more difficult to implement those tests.

## <a id="implementation-plan"> Implementation Plan

### Implement a class that creates a user with a set of permissions

For the purpose of testing, create a class that can create an "anonymous" group
with any set of permissions, and then assign the user to that group.

This way we create a class that can generate a user with any set of permissions.

This implementation point might not be straightforward as it might require
refactoring the permission system currently in place.

It may be possible to use singleusergroup plugin to make the implementation easy.

### Figure out all necessary permissions for each REST endpoint

It is possible to learn the necessary permissions of each endpoint by checking
which IAM permissions are required (this exists in the CCR permission tests) and
then translate the IAM permission to Gerrit permissions. This is not trivial,
since sometimes one IAM permission may translate to many Gerrit permissions.

### Implement a class that tests all endpoints that don't require additional setup

Based on the CCR implementation, the REST endpoints are split into two
categories: those that require additional setup and those who don't.

We can start by running all the necessary permission tests using the class that
creates a user with any set of permissions, and make sure that only the request
with all the necessary permission succeeds. This is possible since the previous
point allowed us to learn which permissions are required for all the endpoints.

### Implement additional setup for some endpoints

Here it would be necessary to manually add a setup for some of the endpoints.
For example, it would necessary to first add a reviewer before checking the for
permissions for the endpoint that deletes a reviewer. Some of that is already
implemented and would be simple to reuse from the CCR permission tests.
After adding necessary setup, we could test the endpoints similarly to the
endpoints tested in the previous implementation point.

## <a id="time-estimation"> Time Estimation

Creating a class that creates a user with any set of permissions might take a week.

Figuring out the necessary permissions can take a week.

Implementing the class that tests all simple endpoints can take 2 weeks.

Implementing the additional setup could take additional 2 weeks.

In total, this project can take around 6 weeks.
