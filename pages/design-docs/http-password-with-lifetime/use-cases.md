---
title: "Design Doc - HTTP Passwords with Limited Lifetime - Use Cases"
permalink: design-docs/http-password-with-lifetime-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="definitions"> Definitions

* HTTP password: When `auth.gitBasicAuthPolicy` is set to `HTTP*`, Gerrit will
  authenticate git- and REST API-requests using basic authentication, where the
  password has to be generated within Gerrit, i.e. it is not the password in the
  IDP used for authenticating in the Gerrit UI.

## <a id="primary"> Primary Use Cases

* Rotation of passwords reduce the risk of unauthorized access by reducing the
  time during which the password is valid and can be used by a potential attacker.
  Enforcing the rotation of passwords ensures that users comply with security
  policies.

## <a id="secondary"> Secondary Use Cases

* Password rotation requires to allow users to have multiple passwords at the
  same time. This would allow users to create more short-lived passwords without
  having to change their main passwords, e.g. for working on shared systems.

## <a id="acceptance-criteria"> Acceptance Criteria

* Accounts can have multiple passwords associated with them.

* During authentication, the provided password has to match one of the stored
  password hashes.

* HTTP passwords can be configured to have a limited lifetime, starting from the
  time of creation.

* During authentication stored HTTP passwords are only considered within their
  lifetime. If no such password exists, or the provided password does not match
  with the available valid passwords, authentication will fail.

* Rotation of passwords has to be a seamless experience, i.e. clients using an
  existing password have to continue to work (if the password is still valid).

* Gerrit administrators can configure whether to enable or also whether to enforce
  a limited lifetime of HTTP passwords.

* Gerrit administrators can configure the maximum lifetime of HTTP passwords that
  can be configured by users.

* A migration tool will be provided to do the notedb schema upgrade and to set a
  lifetime for existing passwords.

## <a id="out-of-scope"> Out Of Scope

* Generated passwords will not have a limited scope, but as before will allow
  access to all resources the associated account has access to.

## <a id="background"> Background

Single-Sign On (SSO) is commonly used by a lot of services/tools. This provides
a great user experience, since users will have to authenticate manually less
often and have to manage less credentials. However, having only a single or handful
of passwords, increases the risk, since if it is compromised not only one but
multiple services will be compromised. For that reason a lot of tools provide
a feature to generate tokens that have a limited lifetime and can be used when
authenticating from scripts or command line. That way the SSO password of a user
is not exposed on machines running automated scripts for example. Generated
passwords are further required, since some authentication methods, e.g. OAuth,
require login via a browser, which is not suitable for automated tools.

Gerrit provides the functionality to generate such passwords. These generated
passwords do however always have an unlimited lifetime. Thus, if such a password
is compromised and the owner does not manually regenerate it, the attacker will
be able to use it for a long time.

Since only a single password per account is allowed at the moment, no seamless
rotation of the password is possible at the moment, since clients won't be able
to authenticate anymore as soon as a new password has been generated. This keeps
a lot of users from rotating passwords regularly.
