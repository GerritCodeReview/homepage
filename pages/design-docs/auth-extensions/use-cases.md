---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="primary"> Primary Use Cases

* authenticate user through the external system without
  adding yet another auth implementation to the Gerrit core. 

  At present Gerrit offers several auth types (HTTP, LDAP, OAuth, etc...)
  that can be used in order to authenticate user within the system but one
  cannot integrate it with 3rd party system that doesn't rely on them.

## <a id="secondary"> Secondary Use Cases

* Take away a burden of maintaining user's display name,
  email addresses and SSH keys in multiple systems. Ideally 3rd party auth
  implementation should also provide this information upon successful
  login. It should be up to the implementation if that information gets
  stored in Gerrit (under existing and/or dedicated scheme) or is just
  cached and reached from the external system upon the request.
* Have multiple auth/user data providers so that account (or different
  accounts) could be authenticated via different external system.

## <a id="acceptance-criteria"> Acceptance Criteria

User can authenticate against the 3rd party system without Gerrit core
changes.

## <a id="background"> Background

Gerrit is built on the top of quite powerful plugin architecture but up
to now it doesn't allow for tight integration with 3rd party systems that
provides not only Web UI and Git CLI authentication but also user's full
name, emails and SSH keys. At current state
[AuthBackend](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/server/auth/AuthBackend.java)
extension point is introduced but it doesn't allow for introduction of any
new auth type (auth type is limited to
[AuthType](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/extensions/client/AuthType.java)
enum). And is literally not used anywhere in the code.
Note that `CUSTOM_EXTENSION` is so far partially implemented (per
comments to
[CUSTOM_EXTENSION](https://gerrit-review.googlesource.com/q/CUSTOM_EXTENSION))
and doesn't allow for plugin based auth introduction. What is more built-in
`Realm` (handles authentication and various account properties like emails,
etc) cannot be used as extension point to deliver that data from the external
system.

Note that initial attempt to introduce
[AuthBackend](https://gerrit-review.googlesource.com/c/gerrit/+/39442)
was performed back in `2012`. It brings `AuthBackend` and exception
definitions and initial implementation for internal and LDAP backends
handled through the `UniversalAuthBackend`.

Current document is based on
[Gerrit AuthBackend](https://docs.google.com/document/d/17LSVzzqoRhpPAnd_fGm3p0_nuPDUA22Kz6Mvx4x3ous)
that was initially discussed back in 2018. POC implementation was created
back then under
[auth-backend](https://gerrit-review.googlesource.com/q/+topic:auth-backend)
topic.
