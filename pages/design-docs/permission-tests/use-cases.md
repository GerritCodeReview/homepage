# Use-case

1. Create comprehensive permission tests for all the existing REST endpoints.
2. Allow to simply add permission tests for new REST endpoints.
3. Test permissions that substitute each other.

## <a id="acceptance-criteria"> Acceptance Criteria

Each REST endpoint that requires permissions X,Y,Z has the following tests:

1. A REST request succeeds for a user with permissions X,Y,Z.
2. A REST request fails for a user who lacks any of the required permissions
(e.g {X,Y}, {X,Z}, {Y,Z}).
3. A REST endpoint also succeeds if a user has permissions X,Y and a permission
that substitutes permission Z (e.g, being an owner, or being an admin, etc).

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

The permission system in Gerrit is complicated, and sometimes there are many
permissions that we don't check at all.
It is not that convenient to manage user permissions in Gerrit for
both production and tests.
Currently, in Gerrit tests it is difficult to check permissions because
there are only a few users: "Admin" that has many permissions, and "user" that
has only a few permissions. Every test needs to manually add permissions to the
user and then check if the REST endpoint is successful. It is possible to
improve it.

