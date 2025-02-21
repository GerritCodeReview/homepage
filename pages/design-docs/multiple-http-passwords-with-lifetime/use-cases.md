---
title: "Design Doc - Multiple HTTP Passwords with Limited Lifetime - Use Cases"
permalink: design-docs/multiple-http-passwords-with-lifetime-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="definitions"> Definitions

* **HTTP password:** When `auth.gitBasicAuthPolicy` is set to `HTTP` or `HTTP_LDAP`,
  Gerrit will authenticate git- and REST API-requests using basic authentication,
  where the password has to be generated within Gerrit, i.e. it is not the
  password in the Identity Provider (IDP) used for authenticating in the Gerrit
  UI. This password has an unlimited lifetime and only a single password can
  exist per account at a time.

* **Token:** A token refers to a generated random String that can be used like
  a password during basic authentication, but potentially has a limited lifetime.


## <a id="primary"> Use Cases

* Rotation of passwords or tokens reduce the risk of unauthorized access by
  reducing the time during which the credential is valid and can be used by a
  potential attacker. Enforcing the rotation of passwords/tokens ensures that
  users comply with security policies.

* Exposure is significantly reduced if users can request short-lived tokens
  for development, proof-of-concepts etc. instead of using their long lived
  credentials outside of their local environment.

* Replacing an old password/token with a new is less disruptive if both credentials
  can be valid simultaneously so as to not break automated processes between
  requesting a new password/token and replacing the old.

## <a id="acceptance-criteria"> Acceptance Criteria

* Accounts can have multiple tokens associated with them.

* During authentication, the provided token has to match one of the stored
  token hashes.

* Tokens can be configured to have a limited lifetime, starting from the
  time of creation.

* During authentication, stored tokens are only considered within their
  lifetime. If no such token exists, or the provided token does not match
  with the available valid tokens, authentication will fail.

* Rotation of tokens has to be a seamless experience, i.e. clients using an
  existing token have to continue to work (if the token is still valid).

* Gerrit administrators can configure whether to enable and also whether to enforce
  a limited lifetime of tokens.

* Gerrit administrators can configure the maximum lifetime of tokens that
  can be configured by users.

* A migration path has to exist, allowing admins to migrate from the old HTTP
  password to the new token approach.

## <a id="out-of-scope"> Out Of Scope

* Tokens will not have a limited scope, but as before will allow access to all
  resources the associated account has access to. This feature will be subject
  to a separate design document in the near future.

## <a id="background"> Background

Single-Sign On (SSO) is commonly used by a lot of services/tools. This provides
a great user experience, since users will have to authenticate manually less
often and have to manage less credentials. However, having only a single or handful
of passwords, increases the risk, since if it is compromised not only one but
multiple services will be compromised. For that reason, a lot of tools provide
a feature to generate tokens that have a limited lifetime and can be used when
authenticating from scripts or command line. That way the SSO password of a user
is not exposed on machines running automated scripts for example. Generated
tokens are further required, since some authentication methods, e.g. OAuth,
require login via a browser, which is not suitable for automated tools.

Gerrit provides the functionality to generate such passwords. These generated
passwords do however always have an unlimited lifetime. Thus, if such a password
is compromised and the owner does not manually regenerate it, the attacker will
be able to use it for a long time.

Since only a single HTTP password per account is allowed at the moment, no seamless
rotation of the password is possible at the moment, since clients won't be able
to authenticate anymore as soon as a new HTTP password has been generated. This
keeps a lot of users from rotating passwords regularly.

## <a id="related-feature-requests"> Related Feature Requests

* https://issues.gerritcodereview.com/issues/40015451
* https://issues.gerritcodereview.com/issues/40014088
