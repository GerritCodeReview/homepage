---
title: "Design Doc - Case Insensitive Username Matching - Solution"
permalink: design-docs/case-insensitive-username-matching-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Case Insensitive Username Matching

## <a id="overview"> Overview

* When case insensitive username matching is configured, the username is case
  insensitively matched with the username/external ID stored in NoteDB, e.g.
  `johndoe`, `JohnDoe` and `JOHNDOE` can all be used to authenticate against the
  same account.
* Creation of accounts with usernames only different in capitalization is
  prohibited by checking for existing usernames case insensitively, if case
  insensitive username matching is configured. This can also be configured
  separately.
* A migration path is provided, including tooling and documentation for how
  to deal with duplicate usernames.
* Necessary changes in NoteDB are not done as a schema migration but using
  a separate tool packaged in the gerrit.war.
* Next to using an offline tool the migration of NoteDB a way to migrate the data
  online may be provided in the future.
* Usernames are stored preserving the original case.

## <a id="detailed-design"> Detailed Design

* Add a configuration option to enable case insensitive username handling.
* Make case insensitive username handling the default for new Gerrit sites, but
  keep current case sensitive username handling on existing sites.
* A tool to detect accounts that are only different in capitalization from NoteDB
  data. Already implemented in [change 300308](https://gerrit-review.googlesource.com/c/gerrit/+/300308)
* Add tooling that allows to change the username/external IDs as a way to deal
  with accounts having usernames only different in capitalization.
* Document how such accounts can be dealt with without causing issues due
  to missing data, by using existing REST API endpoints to either delete the
  account's external IDs or by setting a different username.
  This documentation should explain that a complete deletion of accounts is not
  possible, since the data is referenced in other places of the NoteDB.
* Transform external IDs containing the username (`gerrit:JohnDoe`,
  `username:JohnDoe`) to lowercase before computing the SHA1-sum used for
  storage in NoteDB.
* During the upgrade the External ID data in NoteDB has to be migrated to fit the
  new scheme that uses SHA1 sums of all lowercase external IDs. A warning should
  be emitted for existing duplicate accounts. These accounts will not be usable
  after migration.
* If case insensitive username matching is configured, creation of accounts with
  usernames only different in capitalization is prohibited.

### <a id="scalability"> Scalability

During runtime no impact is to be expected, since transforming the external ID to
all lowercase should add negligible computation cost during externalId matching.

The migration of account data including reindexing of accounts took 9:57 min for
298609 accounts on a MacBook. Reindexing of accounts takes the majority of the
time. If additional speedup is required, multithreading might be tested. Online
migration would be preferable and might be added at a later point in time.

## <a id="alternatives-considered"> Alternatives Considered

* A [change](https://gerrit-review.googlesource.com/c/gerrit/+/300314) proposing
  to use the AccountResolver to case insensitively lookup accounts was discussed,
  but dismissed for the following reasons (Thanks to Edwin and Luca for the review):

  * it is searching over a number of account fields, e.g. it would also find
    accounts that contain username as part of their full name
  * it filters out inactive and non-visible accounts
  * it may use the account index, that may contain stale entries

* An additional consideration is to make case insensitive usernames mandatory.
  In this case the general approach will stay the same, in that the SHA-1 sums
  used as note IDs will be computed from the all lowercase external ID. However,
  the migration will be added as a schema migration and thus be mandatory. The
  advantage would be that the code change is a lot smaller, since the creation
  of External IDs is not dependent on any configuration. However, Gerrit
  administrators would still have to manually take care of accounts with usernames
  only different in their capitalization, which might be quite some work. Also
  this approach would require an identity provider that is als ocase insensitive
  in handling usernames. This might not be the case for all Gerrit users.

## <a id="pros-and-cons"> Pros and Cons

* Existing accounts that are only different in capitalization will have to have
  their externalIds deleted or renamed manually, which will disrupt clients using
  these accounts and potentially create quite some work for Gerrit administrators
  to decide which of the accounts to keep.

## <a id="implementation-plan"> Implementation Plan

1) Tooling and documentation of how to remove or rename external IDs of duplicate
    accounts should be provided.
2) Provide migration path to the new case-insensitive way to compute SHA1 hashes
    used for external IDs
3) Change the creation of new external IDs containing usernames to use all
   lowercase IDs for SHA1 computation. This can be done in
   [`ExternalId.Key.sha1()`](https://gerrit.googlesource.com/gerrit/+/refs/heads/master/java/com/google/gerrit/server/account/externalids/ExternalId.java#175).
   This has to submitted together with 2).
4) Rollout with a minor (3.5) release due to requirement of data migration.
5) Provide way to perform migration of external IDs online to allow zero downtime
    upgrades. There is no specific plan of how to implement online migration.
    This feature might be added in the future.


## <a id="time-estimation"> Time Estimation

Release of this feature is planned to happen with the next Gerrit release (3.5).
