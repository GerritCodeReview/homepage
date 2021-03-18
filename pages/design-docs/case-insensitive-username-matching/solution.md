---
title: "Design Doc - Case Insensitive Username Matching - Solution"
permalink: design-docs/case-insensitive-username-matching-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Case Insensitive Username Matching

## <a id="overview"> Overview

* If a user authenticates, the username is case insensitively matched with the
  username/external ID stored in NoteDB, e.g. `johndoe`, `JohnDoe` and `JOHNDOE`
  can all be used to authenticate against the same account.
* Accounts with usernames only different in capitalization will be prohibited by
  checking for existing usernames case insensitively.
* Usernames will be stored case preserving.

## <a id="detailed-design"> Detailed Design

* A bash script to detect duplicate accounts from NoteDB data. (Already implemented
  in [change 300308](https://gerrit-review.googlesource.com/c/gerrit/+/300308))
* An SSH command to delete accounts by removing the external IDs associated to
  the account from NoteDB.
* Transform external IDs containing the username (`gerrit:JohnDoe` and
  `username:JohnDoe`) to lowercase before computing the SHA1-sum used for storage
  in NoteDB
* During the upgrade the External ID data in NoteDB has to be migrated to fit the
  new scheme that uses SHA1 sums of all lowercase external IDs. A warning should
  be emitted for existing duplicate accounts. These accounts will not be usable
  after migration.

### <a id="scalability"> Scalability

During runtime no impact is to be expected, since transforming the external ID to
all lowercase should add negligible computation cost during username matching.

The migration of account data should be able to use multiple threads to be able
to deal with large numbers of accounts in a reasonable time frame, especially if
a downtime is required for migration.

## <a id="alternatives-considered"> Alternatives Considered

A [change](https://gerrit-review.googlesource.com/c/gerrit/+/300314) proposing
to use the AccountResolver to case insensitively lookup accounts was discussed,
but dismissed for the following reasons (Thanks to Edwin and Luca for the review):

* it is searching over a number of account fields, e.g. it would also find
  accounts that contain username as part of their full name
* it filters out inactive and non-visible accounts
* it may use the account index, that may contain stale entries

## <a id="pros-and-cons"> Pros and Cons

* The data migration will require time during the update and might not be possible
  to do online.
* Existing duplicate accounts will have to be deleted manually, which will disrupt
  clients using these accounts and potentially create quite some work for Gerrit
  administrators to decide which of the accounts to keeps.

## <a id="implementation-plan"> Implementation Plan

1) Further creation of duplicate accounts should be prohibited to limit the
   work required to get rid of the duplication.
2) Tooling to remove duplicate accounts should be provided. This can happen in
   parallel to 1).
3) Provide migration path to the new SHA1 format used for external IDs
4) Change the creation of new external IDs containing usernames to use all
   lowercase IDs for SHA1 computation. This has to submitted together with 3).
5) Rollout with a minor (3.x) release due to requirement of data migration.


## <a id="time-estimation"> Time Estimation

TBD
