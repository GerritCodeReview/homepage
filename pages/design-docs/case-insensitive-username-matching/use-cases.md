---
title: "Design Doc - Case Insensitive Username Matching - Use Cases"
permalink: design-docs/case-insensitive-username-matching-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="definitions"> Definitions

* duplicate usernames/accounts: Usernames or accounts having usernames that are
  only different in their capitalization.
  E.g.: `johndoe` and `JohnDoe`. While no true duplicates, they will be referred
  to as duplicates for readability.
* external IDs: Gerrit uses (generic) user names in different externalId schemes
  which are used for different authentication systems.

  Currently the following externalId schemes exist (defined in
  [ExternalId.java](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/server/account/externalids/ExternalId.java#114)):

  `gerrit`   (LDAP)
  `username` (authentication REST and git endpoints)
  `external` (external authentication e.g. oauth, saml)
  `gpgkey`   (gpg keys)
  `mailto`   (email addresses)
  `uuid`     (randomly created identities constructed by a UUID)

  Relevant for authentication are the schemes `gerrit`, `username`, `external`,
  of which `external` may or may not contain the username.

## <a id="primary"> Primary Use Cases

* Gerrit administrators can migrate between authentication methods and account
  type without disrupting users.

## <a id="secondary"> Secondary Use Cases

* Prohibit duplicate usernames that make it harder for users to identify such an
  user.

## <a id="acceptance-criteria"> Acceptance Criteria

* It should be impossible to create accounts with duplicate usernames.
* A tool that allows Gerrit administrators to identify existing duplicate
  accounts should be available. Already implemented
  in [change 300308](https://gerrit-review.googlesource.com/c/gerrit/+/300308).
* The process of dealing with duplicates by either deletion of the external IDs
  or changing of the username by the administrator should be properly documented.
* Clients should be able to login with a username using any capitalization they
  prefer, i.e. username matching during authentication should be case insensitive.
* Display names should show the username as presented during account creation.
  E.g. if `JohnDoe` is used during account registration this form should appear
  if mentioned in the UI, regardless of how the username is represented internally.
* Existing accounts, except for duplicates, should not be disrupted by introducing
  this change.
* Gerrit administrators should have a straightforward way of migrating to other
  identity providers without disrupting users.

## <a id="background"> Background

Gerrit by default treats usernames case sensitive, i.e. there can be the accounts
of `johndoe` and `JohnDoe` at the same time. There are currently options in
Gerrit's configuration influencing that aim to achieve case insensitivity
by storing and matching usernames in all lowercase, regardless of the capitalization
used by the client. However, these options don't allow to handle accounts with
mixed- or uppercase usernames created before being set and currently do not
handle all ways to create accounts in Gerrit.

The existing behavior can lead to issues, when trying to migrate to a different
identity provider. The scenario encountered by SAP can be taken as an example:
The identity provider is supposed to be switched from LDAP to SAML. This has to
happen with minimal disruption for the users, i.e. the username should not change.
The Gerrit instance has four types of users:

* Internal technical users (created via REST API or the `create-account` SSH command)
* Service users (created via the serviceuser-plugin)
* Technical users managed by LDAP
* Human users managed by LDAP

Usernames of accounts managed by LDAP are stored in all lowercase
(`ldap.localUsernameToLowerCase = true`). Other account types are allowed to
use uppercase letters in the username stored in NoteDB. Some usernames are
duplicates. The new identity provider does not allow technical users, thus
technical users managed by LDAP were registered as service users, so that they
can be used as internal accounts managed by the serviceuser plugin.

The saml-plugin uses the `auth.userNameToLowerCase`-option to convert the username
used to login to lowercase. This setting blocks all internal technical users
and service users with uppercase letters in the username, e.g. The serviceuser
`JenkinsBuild` will not be able to authenticate, since during authentication the
username is converted to `jenkinsbuild`, which is not present in NoteDB, where
the external ID `username:JenkinsBuild` is present. This can be fixed by
adding an option complimentary to `ldap.localUsernameToLowerCase` to the saml-
plugin. However, with such an option the newly registered service users (former
LDAP-based technical users) would not able to log in, if the usernames have
uppercase letters, since this does not match the username in NoteDB that is all
lowercase.

To illustrate, a list of example scenarios follows:

* LDAP scenario (current state)
  * `ldap.localUsernameToLowerCase = true`
  * `auth.userNameToLowerCase = false`

  | user type        | username used by user | username in NoteDB | username used in DB lookup | login successful |
  |------------------|-----------------------|--------------------|----------------------------|------------------|
  | serviceuser      | johndoe               | johndoe            | johndoe                    | true             |
  | serviceuser      | JohnDoe               | JohnDoe            | JohnDoe                    | true             |
  | LDAP (human)     | johndoe               | johndoe            | johndoe                    | true             |
  | LDAP (human)     | JohnDoe               | johndoe            | johndoe                    | true             |
  | LDAP (technical) | johndoe               | johndoe            | johndoe                    | true             |
  | LDAP (technical) | JohnDoe               | johndoe            | johndoe                    | true             |
  | internal user    | johndoe               | johndoe            | johndoe                    | true             |
  | internal user    | JohnDoe               | JohnDoe            | JohnDoe                    | true             |

* SAML scenario 1
  * technical users (internal users and LDAP-managed technical users) are registered as serviceusers
  * `auth.userNameToLowerCase = false`

  | user type                 | username used by user | username in NoteDB | username used in DB lookup | login successful |
  |---------------------------|-----------------------|--------------------|----------------------------|------------------|
  | serviceuser               | johndoe               | johndoe            | johndoe                    | true             |
  | serviceuser               | JohnDoe               | JohnDoe            | JohnDoe                    | true             |
  | SAML (human)              | johndoe               | johndoe            | johndoe                    | true             |
  | SAML (human)              | JohnDoe               | johndoe            | JohnDoe                    | false            |
  | formerly LDAP (technical) | johndoe               | johndoe            | johndoe                    | true             |
  | formerly LDAP (technical) | JohnDoe               | johndoe            | JohnDoe                    | false            |
  | internal user             | johndoe               | johndoe            | johndoe                    | true             |
  | internal user             | JohnDoe               | JohnDoe            | JohnDoe                    | true             |

* SAML scenario 2
  * technical users (internal users and LDAP-managed technical users) are registered as serviceusers
  * `auth.userNameToLowerCase = true`

  | user type                 | username used by user | username in NoteDB | username used in DB lookup | login successful |
  |---------------------------|-----------------------|--------------------|----------------------------|------------------|
  | serviceuser               | johndoe               | johndoe            | johndoe                    | true             |
  | serviceuser               | JohnDoe               | JohnDoe            | johndoe                    | false            |
  | SAML (human)              | johndoe               | johndoe            | johndoe                    | true             |
  | SAML (human)              | JohnDoe               | johndoe            | johndoe                    | true             |
  | formerly LDAP (technical) | johndoe               | johndoe            | johndoe                    | true             |
  | formerly LDAP (technical) | JohnDoe               | johndoe            | johndoe                    | true             |
  | internal user             | johndoe               | johndoe            | johndoe                    | true             |
  | internal user             | JohnDoe               | JohnDoe            | johndoe                    | false            |

* SAML scenario 3
  * technical users (internal users and LDAP-managed technical users) are registered as serviceusers
  * `auth.userNameToLowerCase = true`
  * `saml.localUsernameToLowerCase = true` (not yet implemented)

  | user type                 | username used by user | username in NoteDB | username used in DB lookup | login successful |
  |---------------------------|-----------------------|--------------------|----------------------------|------------------|
  | serviceuser               | johndoe               | johndoe            | johndoe                    | true             |
  | serviceuser               | JohnDoe               | JohnDoe            | johndoe                    | false            |
  | SAML (human)              | johndoe               | johndoe            | johndoe                    | true             |
  | SAML (human)              | JohnDoe               | johndoe            | johndoe                    | true             |
  | formerly LDAP (technical) | johndoe               | johndoe            | johndoe                    | true             |
  | formerly LDAP (technical) | JohnDoe               | johndoe            | johndoe                    | true             |
  | internal user             | johndoe               | johndoe            | johndoe                    | true             |
  | internal user             | JohnDoe               | JohnDoe            | johndoe                    | false            |

* SAML scenario 4
  * technical users (internal users and LDAP-managed technical users) are registered as serviceusers
  * `auth.userNameToLowerCase = false`
  * `saml.localUsernameToLowerCase = true` (not yet implemented)

  | user type                 | username used by user | username in NoteDB | username used in DB lookup | login successful |
  |---------------------------|-----------------------|--------------------|----------------------------|------------------|
  | serviceuser               | johndoe               | johndoe            | johndoe                    | true             |
  | serviceuser               | JohnDoe               | JohnDoe            | JohnDoe                    | true             |
  | SAML (human)              | johndoe               | johndoe            | johndoe                    | true             |
  | SAML (human)              | JohnDoe               | johndoe            | johndoe                    | true             |
  | formerly LDAP (technical) | johndoe               | johndoe            | johndoe                    | true             |
  | formerly LDAP (technical) | JohnDoe               | johndoe            | JohnDoe                    | false            |
  | internal user             | johndoe               | johndoe            | johndoe                    | true             |
  | internal user             | JohnDoe               | JohnDoe            | johndoe                    | true             |


While this example uses non-core plugins and is very specific, it shows that
having different accounts with usernames only different in capitalization can
lead to hard to resolve issues or disruption of users. Further, there is likely
no good use case to support duplicate usernames. These duplicates might rather
lead to confusion in identifying a user. Thus, account data could be made easier
to manage by matching accounts case insensitive during authentication.
