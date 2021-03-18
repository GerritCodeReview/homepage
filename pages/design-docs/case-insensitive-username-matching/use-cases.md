---
title: "Design Doc - Case Insensitive Username Matching - Use Cases"
permalink: design-docs/case-insensitive-username-matching-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use Cases

## <a id="definitions"> Definitions

* duplicate usernames/accounts: Usernames that are only different in their
  capitalization or their accounts respectively.
  E.g.: `johndoe` and `JohnDoe`. While no true duplicates, they will be referred
  to as duplicates for readability.

## <a id="primary"> Primary Use Cases

* Gerrit administrators can migrate between authentication methods and account
  type without disrupting users.

## <a id="secondary"> Secondary Use Cases

* Prohibit duplicate usernames that make it harder for users to identify such an
  user.

## <a id="acceptance-criteria"> Acceptance Criteria

* It should be impossible to create accounts with duplicate usernames.
* A tool that allows Gerrit administrators to identify existing duplicate
  accounts should be available
* Account deletion should be possible for administrators via SSH command and/or
  REST API.
* Clients should be able to login with a username using any capitalization they
  prefer, i.e. username matching during authentication should be case insensitive.
* Display names should show the username as presented during account creation.
  E.g. if `JohnDoe` is used during account registration this form should appear
  if mentioned in the UI, regardless of how the username is represented internally.
* Existing accounts should not be disrupted by introducing this change.
* Gerrit administrators should have a straightforward way of migrating to other
  identity providers without disrupting users.

## <a id="background"> Background

Gerrit by default treats usernames case sensitive, i.e. there can be the accounts
of `johndoe` and `JohnDoe` at the same time. There are currently options in
Gerrit's configuration influencing that aim to achieve case insensitivity
by storing and matching usernames in all lowercase, regardless of the capitalization
used by the client. However, these options don't allow to handle accounts with
mixed- or uppercase usernames created before being set and do currently do not
handle all ways to create accounts in Gerrit.

Gerrit currently uses three different externalIds that (potentially) contain the
username: `gerrit` for LDAP-based authentication types, e.g. `LDAP` or `HTTP_LDAP`;
`username` for all accounts in Gerrit, including accounts created internally (i.e.
with the create-account SSH command); `external` for external authentication
types, e.g. used by the saml-plugin. The former externalId not necessarily contains
the username.

The existing behavior can lead to issues, when trying to migrate to a different
identity provider. The scenario encountered by SAP can be taken as an example:
The identity provide is supposed to be switched from LDAP to SAML. This has to
happen with minimal disruption for the users, i.e. the username should not change.
The Gerrit instance has four types of users:

* Internal technical users (created via REST API or SSH command)
* Service users (serviceuser-plugin)
* Technical users managed by LDAP
* Human users managed by LDAP

Usernames of accounts managed by LDAP are stored in all lowercase
(`ldap.localUsernameToLowerCase = true`). Other account types are allowed to
use uppercase letters in the username stored in NoteDB. Some usernames are
duplicates. The new identity provider does not allow technical users, thus
technical users managed by LDAP were registered as service users, so that they
can be used as internal accounts managed by the serviceuser plugin.

The saml-plugin uses the `auth.userNameToLowerCase`-option to convert the username
used to login to lowercase. Doing so would does block all internal technical users
and service users with uppercase letters in the username. This can be fixed by
adding an option complimentary to `ldap.localUsernameToLowerCase`. However, the
newly registered service users are not able to log in, if the usernames have
uppercase letters, since this does not match the username in NoteDB that is all
lowercase.

While this example uses non-core plugins and is very specific, it shows that
having different accounts with usernames only different in capitalization can
lead to hard to resolve issues or disruption of users. Further, there is likely
no good use case to support duplicate usernames. These duplicates might rather
lead to confusion in identifying a user. Thus, account data could be made easier
to manage by matching accounts case insensitive during authentication.
