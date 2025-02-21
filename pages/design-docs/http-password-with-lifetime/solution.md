---
title: "Design Doc - HTTP Passwords with Limited Lifetime - Solution"
permalink: design-docs/http-password-with-lifetime-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - HTTP Passwords with Limited Lifetime

## <a id="overview"> Current Design

* Only a single password can be used at a time. Generating a new password will
  replace the previous one.

* Generated passwords have an unlimited lifetime.

* The password is currently stored as part of the `username:` external ID:

```
[externalId "username:admin"]
	accountId = 1000000
	password = bcrypt0:4:Dd2OxFM73ALnECduYqYQEQ==:QnQIFibB/Y04HvIY4UstiJhWagTtk6gN
```

* In addition to updating `refs/meta/external-ids` ref in `All-Users`, an empty
  commit is created in `refs/users/xx/1xxxxx` to document the password generation.

## <a id="detailed-design"> Detailed Design

* The current way of storing password hashes is not ideal to store multiple
  passwords, since it does not provide an ideal way to add additional parameters
  like an identifier or expiration time.

* Similar to SSH keys, passwords should be stored under the user ref using a file
  named `passwords` with the following format:

```
[password "password-id-1"]
  hash = bcrypt0:....
  expires = 2025-06-01T14:30

[password "password-id-2"]
  hash = bcrypt0:....
  expires = 2025-06-30T15:45

[password "never-expires"]
  hash = bcrypt0:....
```

* This might break custom authentication implementations that also use the
  password parameter of external IDs (other than in `username:`). To avoid this,
  the external ID key could be a property of the password entry:

```
[password "password-id-2"]
  extIdKey = username:admin
  hash = bcrypt0:....
  expires = 2025-06-30T15:45
```

* Users can reference passwords by an ID that they themselves can set or which
  alternatively is generated based on the time of generation.

* Passwords can be deleted before and after expiration.

* A scheduled job can be used to clean up old expired passwords.

* A scheduled job will send out reminder emails some time before the password
  expires.

* The number of passwords a user can generate can be limited to avoid denial
  of service by bloating the All-Users project with millions of password
  entries.

* IDs of active passwords for each account should be cached, but not the hashes
  itself. This will improve the lookup times for passwords, since expired
  password entries do not have to be read from file every time.

* An offline tool should be made available to update the notedb to the new
  schema.

* The offline tool can also be used to set an expiration date for all passwords
  in a Gerrit instance. If an existing expiration date is earlier than the
  provided one, it is not updated. This tool should be used, when a new lifetime
  will be enforced in the future.

* Alternatively, both schemas might be supported as long as no limited
  lifetime is being enforced. In that case, the schema could be updated for an
  account, when a new password is being generated. Note, that accounts that do
  not rotate their password during that time will have to generate a new password
  after the old storage behavior was fully removed.

* This change will require a change in the REST APIs for handling passwords and
  might add additional fields to the account info object.


## <a id="alternatives-considered"> Alternatives Considered

* The data could be stored in the current schema by appending the additional
  properties using a delimiter. However, that would not scale well and would
  not be well readable even by machines (the hash would have to be loaded into
  memory even to check whether it is expired).

* The `password` sections could be stored in the same file as the external ID,
  thereby keeping a link to the external ID to avoid compatibility issues.
  However, this would break the format of externalIDs, which are meant to be
  stored as a git config file with just a single section.

## <a id="implementation-plan"> Implementation Plan

1) Implement the new schema, while still allowing only a single password and no
   expiration.

2) Implement tool to migrate to the new schema.

3) Optionally, allow the read-only use of both schemas.

4) Allow to name generated passwords.

5) Allow to generate multiple passwords.

6) Change the UI accordingly.

7) Allow to configure a lifetime for passwords.

8) Add option to enforce a lifetime for passwords.

9)  Add tool to set the lifetime for existing passwords.

10) Change the UI accordingly.


## <a id="time-estimation"> Time Estimation

This feature is planned for Gerrit 3.12 or 3.13.
