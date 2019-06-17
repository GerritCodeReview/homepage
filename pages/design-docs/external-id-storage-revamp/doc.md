---
title: "Revamp External ID Storage"
sidebar: gerritdoc_sidebar
permalink: design-docs-revamp-external-id-storage-doc.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/revamp-external-id-storage
---

*Author: hiesel@ - Last updated: 2019-06-17*

## Objective
Eliminate latency added to requests at random after an external ID was updated on the host. Reduce latency caused by
authentication. Provide fast lookups for email => account and external ID => account in primary storage.

## Background
Gerrit distinguishes between accounts and external IDs. There is a 1:n (account:external ID) relationship between these
entities. The account entity stores information about the user including the full name and the username. An external ID
is a link of an account to an external authentication system (such as Google Accounts or an LDAP provider).

Gerrit users frequently complain about the latency of their requests. Prior work on caches has identified the current
external ID system in Gerrit as one component that can add significant latency of up to 1 minute to a random, unrelated
request after any external ID was updated on the same host.

A full-stack analysis has shown that we have to pay a penalty for authenticating a user on every request that has its
root cause in the external ID system.
The current system uses an ExternalId cache that is serialized and written to disk. The cache holds an entire generation
of all external IDs. Hence, it is invalidated when a single external ID is updated. This forces the task to reload all
external IDs from the Git repository. While we make an effort to paper over this effect by replacing the cache value
in-memory in the task that served the update request, other tasks (slaves) still suffer from the aforementioned
phenomenon.

## Scale
Google-internal metrics suggest that requests spend tens of hours waiting for the external ID cache fleet-wide per day.

Numbers from larger, non-Google installations suggest that we update refs/meta/external-ids up to 500 times per day.

## Objectives
Fast lookup using only primary storage for:
- ExternalID => Account (used for login)
- Primary email address => Account (used for different internal operations)
- `Account.Id` => Account (used for different internal operations)
- Guarantee/guaranteeable uniqueness for primary email addresses
- Guarantee/guaranteeable uniqueness for external IDs
- Little or no impact to latency of other requests when a user updates any of their data (account data, external IDs,
  email addresses). Upper bound guarantee for impact on other requests.

## Detailed Design
In the special All-Users repository, we already have account refs that contain account metadata, such as the user’s full
name and status:
`refs/users/uu/vvvvvuu`
The ref contains a Git config file (account.config) with the account data:

```
[account]
        fullName = Patrick Hiesel
        preferredEmail = hiesel@google.com
```

We add external IDs associated with the account to external-ids.config on the same ref:
```
[externalId "<external-id-key-1>"]
        accountId = 123123
[externalId "<external-id-key-2>"]
        accountId = 123123
```
We remove the monolithic `refs/meta/external-ids`.

We add two new refs with NotesMaps that allow fast lookups of accounts by primary email and by external ID:

```
refs/index/account-by-external-id/<shard>
refs/index/account-by-email/<shard>
```

The respective notes map stores a mapping of a SHA1(email)/SHA1(external-id) to a single file. The file is in git-config
format and contains:

```
[account]
        id = 123
```

### Sharding
The previously outlined ref name specification, contains a <shard> part. This part is computed from the key entity (for
account-by-external-id, that is external-id). The goal is to shard the index onto multiple refs to avoid lock failures
when updating it. Open-source instances see up to 500 updates of external IDs per day, many of which suffer from a lock
failure. Sharding will help ease that.

The shard is computed from `SUBSTRING(SHA1(entity), x)`. For now `x = 1` which means 6 (A-F hex) + 10 (digits) = 16
shards. The parameter is not configurable dynamically, but can be adapted in the future requiring a data migration.

### Caching

#### Accounts
The account cache is currently mutable and invalidated using direct eviction for a single master. For multi-master or
master-slave setups, it is evicted using events. This is problematic because messages can be lost.
In addition, it currently means that when a Gerrit instance starts up, the cache is empty.

With this migration, we will add the externalIDs to the account data stored in the account cache and make the cache
immutable. The cache will also be serialized to disk by default.

Entities are implemented with the following structure:

```
message AccountCacheKey {
        int32 account_id;
        bytes object_id;  // SHA1 of refs/users/xx/uuuuxx
}
```

```
message AccountCacheValue {
        String status;
        // ...
        repeated AccountCacheExternalIdValue external_id;
}
```

```
message AccountCacheExternalIdValue {
        string external_id;
        // ...
}
```

As mentioned, the AccountCache will be written to disk. On SSD, read latency is low. For better performance, we keep a
reasonable sized (2x max-number-of-accounts) in-memory version as well.

The required memory footprint is low even on a host with 200k accounts:

```
200k accounts x [ key(4 bytes account ID + 20 bytes SHA1) + value(400 bytes metadata + 200 bytes external ID)] ~ 128 MiB.
```

The current implementation of the AccountCache has logic to parallelize loading accounts. This is obsolete by the new
cache design and will be removed.

Overall, this approach cuts out a lot of existing complexity (parallelization logic, mutable caches).

If required, we can add the following two caches in the future:
#### AccountByExternalId [optional]

```
message AccountByExternalIdKey {
        string external_id;
}
```

```
message AccountByExternalIdValue {
        int64 account_id;
        string account_ref_sha1; // Used for checking the freshness of the record
}
```

#### AccountByEmail [optional]

```
message AccountByEmailKey {
        string email;
}
```

```
message AccountByEmailValue {
        repeated int64 account_id;
        repeated string account_ref_sha1; // Used for checking the freshness of the
        // record
}
```

The lookup for an account by email or by external ID is then:

Retrieve `Account.Id` from a lookup in `AccountBy{Email/ExternalId}`. Retrieve the Account from the AccountCache. If this
yields an entity, we are done. If not, the record in AccountBy{Email/ExternalId} was out of date. Use the primary
storage to resolve Email/External ID to Account.Id. Use the account cache to get the account.

### Migration

Migration will be done with a schema upgrade.

### Debuggability
Admins frequently debug access issues for users that sometimes relate to problems with external IDs. The most frequent
operation is looking up an account by ID and checking the history as well as correlating that with external ID updates.

The new schema supports this and in fact makes it easier as the account ref is then the single source of truth.
We expect admins to manually check either one of the lookup indices infrequently.

### Alternatives Considered

#### Keep the current system
On Google's infrastructure (this applies also to open-source installations), users are spending tens of hours / day on aggregate waiting for Gerrit to return a request while Gerrit is reading external IDs. This is not acceptable.


#### Use symrefs as index
We create a symref for every e-mail/external ID that points to the account ref.
```
refs/emails/SHA(email) => refs/users/xx/uuuuxx
refs/external-ids/scheme/SHA(external-id-parts) => refs/users/xx/uuuuxx
```

This ensures uniqueness for both external IDs and primary emails. It comes at the cost of increasing the number of refs in All-Users by roughly 4x:


Assuming a single installation has 200.000 accounts and users have 2 external IDs.
```
400k external ID refs + 200k account refs + 200k email refs = 800k refs
```

Core git currently does not have a RefTable implementation, so it is not feasible for open-source installations to
switch to RefTable as they would loose the ability to use core-Git for administrative purposes.

In addition, a large number of refs is always a concern in that this in untested terrain. We also might want to add
similar indices in the future hereby further adding to the number of refs.
