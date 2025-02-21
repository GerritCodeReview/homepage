---
title: "Design Doc - Multiple HTTP Passwords with Limited Lifetime - Solution"
permalink: design-docs/multiple-http-passwords-with-lifetime-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Multiple HTTP Passwords with Limited Lifetime

## <a id="overview"> Current Design

* Only a single HTTP password can be used at a time. Generating a new HTTP
  password will replace the previous one.

* Generated HTTP passwords have an unlimited lifetime.

* The HTTP password is currently stored as part of the `username:` external ID:

```
[externalId "username:admin"]
	accountId = 1000000
	password = bcrypt0:4:Dd2OxFM73ALnECduYqYQEQ==:QnQIFibB/Y04HvIY4UstiJhWagTtk6gN
```

* In addition to updating `refs/meta/external-ids` ref in `All-Users`, an empty
  commit is created in `refs/users/xx/1xxxxx` to document the password generation.

## <a id="detailed-design"> Detailed Design

* The current way of storing password hashes is not ideal to store multiple
  tokens, since it does not provide an ideal way to add additional parameters
  like an identifier or expiration time.

* Similar to SSH keys, tokens should be stored under the user ref using a file
  named `tokens` with the following format:

```
[token "token-id-1"]
  hash = bcrypt0:....
  expires = 2025-06-01T14:30Z

[token "token-id-2"]
  hash = bcrypt0:....
  expires = 2025-06-30T15:45Z

[token "never-expires"]
  hash = bcrypt0:....
```

* This might break custom authentication implementations that also use the
  password parameter of external IDs (other than in `username:`). To avoid this,
  the external ID key could be a property of the password entry:

```
[token "token-id-2"]
  extIdKey = username:admin
  hash = bcrypt0:....
  expires = 2025-06-30T15:45Z
```

* The API to access tokens will be similar to accessing SSH keys, i.e. it will
  be fully decoupled from the `AccountState`. To access tokens from `All-Users`
  a class extending `VersionedMetaData` will be used. The advantage of this
  implementation is that the support for tokens is completely optional, i.e.
  Gerrit installations that use for example LDAP or custom implementations will
  not make use of it at all.

* Users can reference tokens by an ID that they themselves can set or which
  alternatively is generated based on the time of generation.

* Tokens can be deleted before and after expiration.

* A scheduled job can be used to clean up old expired tokens.

* A scheduled job will send out reminder emails some time before the token
  expires.

* The number of tokens a user can generate and have at a time can be limited to
  avoid denial of service by bloating the All-Users project with millions of
  token entries.

* As is already the case, token hashes will be cached to keep lookup times
  as short as possible. Similar to the SSH key cache, the tokens should be
  cached in a dedicated cache. The cache will only be installed in the Guice
  environment, if the use of tokens is enabled. The cache will map `Account.Id`
  to a list of tokens in teh account.

* A tool will be made available to update the notedb to the new schema, i.e.
  it will copy the HTTP password to the new token format and delete it from the
  external ID. This tool will be available for offline and online use.

* The tool can also be used to set an expiration date for all tokens
  in a Gerrit instance. If an existing expiration date is earlier than the
  provided one, it is not updated. This tool should be used, when a new lifetime
  will be enforced in the future.

* Both schemas (HTTP password and tokens) will be supported as long as no limited
  lifetime is being enforced. In that case, the schema will be updated for an
  account, when a new token is being generated. Note, that accounts that do
  not rotate their token during that time will have to generate a new token
  after the old storage behavior was fully removed to be able to continue to use
  git over HTTP and the REST API.

* Since the naming of the existing REST API endpoints to manipulate the HTTP
  password does not fit the token terminology, new REST API endpoints will be
  created to manage tokens for an account. For an interim period the old REST API
  endpoints will stay in place, but work as aliases for the new endpoint, i.e.
  they will lead to creation/deletion of a token. This will provide backwards
  compatibility for existing scripts.

* The email notifications about a password generation will be adapted to provide
  more detail about how tokens of an account are being updated.


## <a id="alternatives-considered"> Alternatives Considered

* The data could be stored in the current schema by appending the additional
  properties using a delimiter. However, that would not scale well and would
  not be well readable even by machines (the hash would have to be loaded into
  memory even to check whether it is expired).

* An ordinal ID could be appended to keys related to tokens. That way they could
  still be stored as part of the external ID. However, that would require some
  custom code to access the data, since this is not foreseen by the git config
  format and jgit's APIs to access these files.

* The `token` sections could be stored in the same file as the external ID,
  thereby keeping a link to the external ID to avoid compatibility issues.
  However, this would break the format of externalIDs, which are meant to be
  stored as a git config file with just a single section.

## <a id="implementation-plan"> Implementation Plan

1) Implement the new schema, while still allowing only a single password and no
   expiration.

2) Implement tool to migrate to the new schema.

3) Optionally, allow the read-only use of both schemas.

4) Allow to name generated tokens.

5) Allow to generate multiple tokens.

6) Change the UI accordingly.

7) Allow users to configure a lifetime for tokens.

8) Add option for admins to enforce a maximum lifetime for tokens.

9)  Add tool to set the lifetime for existing tokens.

10) Change the UI accordingly.


## <a id="time-estimation"> Time Estimation

This feature is planned for Gerrit 3.12 or 3.13.
