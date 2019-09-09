# Use-case

1. Create comprehensive permission tests for all the existing REST endpoints.
2. Allow to simply add permission tests for new REST endpoints.

## <a id="acceptance-criteria"> Acceptance Criteria

Each REST endpoint that requires permissions X,Y,Z has the following tests:

1. A REST request succeeds for a user with permissions X,Y,Z.
2. A REST request fails for a user who lacks any of the required permissions
(e.g {X,Y}, {X,Z}, {Y,Z}).

Suppose a developer creates a new REST endpoint, that developer should add
corresponding permission test coverage for the new REST endpoint with one of the
following setups:

#### Simple setup

Those tests will check for permissions in the manner specified above. We will
create an initial setup that would be reused for all simple REST endpoints.

#### Additional setup

Here the developer will need to perform the additional setup required, and then
run the same tests as the ones implemented for the simple setup.

## <a id="background"> Background

Currently there exist permission tests for CCR, those tests ensure that each
REST endpoint checks all the required permissions, and makes sure that the request is
rejected if the user lacks any of those permissions.

To add the similar tests for upstream Gerrit, we need to tackle the following
problems:

1. The permission system in Gerrit is more complicated: Sometimes there are many
Gerrit permissions that map to the same IAM permission, it might be complicated
to learn which Gerrit permission checks should be done by using the tests for
CCR, since we will have to translate the IAM permission into Gerrit permissions.
2. It is not that convenient to manage user permissions in upstream Gerrit for
both production and tests.
Currently, in upstream Gerrit it is difficult to check permissions because
there are only a few users: "Admin" that has many permissions, and "user" that
has only a few permissions. Every test needs to manually add permissions to the
user and then check if the REST endpoint is successful. It is possible to
improve it; it may be necessary to create a simple class that grants permissions
to a user, for the purpose of the tests.
3. Some endpoints require special setup, but luckily it is possible to reuse the
code written for CCR.
