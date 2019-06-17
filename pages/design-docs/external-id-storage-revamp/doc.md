---
title: "Revamp External ID Storage"
sidebar: gerritdoc_sidebar
permalink: design-docs-revamp-external-id-storage-doc.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/revamp-external-id-storage
---

*Author: hiesel@ - Last updated: 2019-07-10*

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

### Current Performance Problems

The problems with the current design can be classified as follows:

#### External ID Cache

The current system uses an ExternalId cache that is serialized and written to disk. The cache holds an entire generation
of all external IDs, keyed by the SHA1 of `refs/meta/external-ids`. This is roughly, `Cache<ObjectId, List<ExternalID>>`.

That implies that it has to be re-read from primary storage whenever a single External ID changes.

There is code to swap out the cache value in memory for the Gerrit job that performed the update. However,
in any replicated system (master/master, master/slave), remote replicas will have to reload all External IDs from Git.
The same is true for any Gerrit task during startup if the cache value is not available in the disk cache.

The time it takes to reload all External IDs is dependent on a variety of factors:
- Storage: DFS vs. Filesystem
- Hardware (mostly SSD vs HDD)
- Number of external IDs

On googlesource.com, we see load times of up to 1 minute.

The External ID cache is used when looking up an account by email or an external ID by account ID. The most
prominent use case is `AccountResolver#search` which is used in various parts in Gerrit. This makes it so that
a large variety of requests can suffer from this bottleneck.

#### Contention on Writes

In the current design, `refs/meta/external-ids` is a bottleneck that all External IDs have to go through. This puts a limit
on how many updates the system can process. That limit solely depends on Gerrits peformance when updating refs.
Again, ref update performance can vary based on system-specifics, but it's usually in the low,
single-digit seconds.

Gerrit Forge sees update rates of up to 83/min (1.38/sec) where an average update takes 3s. This shows that
the current design has write contention.

#### Authentication

In the current system, authentication is done in primary storage by looking up the user's external ID directly in Git.
We retrieve the account number from the NoteMap behind `refs/meta/external-ids` and look up the account.

On googlesource.com, the External ID cache is also used during authentication to fixup accounts, increasing the
number of requests that can suffer from the bottleneck mentioned in 'External ID Cache'.

#### Loading Accounts

The account cache is currently implemented as a mutable cache. This is mandated by the fact that the value (`AccountState`)
contains the account's external IDs, so it is dependent on value changes in `refs/meta/external-ids`.

In Gerrit, we favor caches where either the key or value tell us if the cached entity is outdated. This is because
that makes cache handing in replicated setups (master/master, master/slave) easier in that one does not have
to propagate cache invalidations. A lot of cache keys contain the SHA1(s) of the refs that are used to generate the data.
In case the key contains all SHA1(s), the cache is usually marked immutable.

The fact that `refs/meta/external-ids` changes so frequently and is a single-ref only currently prevents us from
making the account cache immutable.

This adds the following problems:
- The cache can't be serialized
- Instances start up with an empty cache adding to cold start performance issues
- Extra propagation needed for replicated Gerrit tasks upon cache invalidation

## Scale
Google-internal metrics suggest that requests spend tens of hours waiting for the external ID cache fleet-wide per day.

Numbers from larger, non-Google installations suggest that we update refs/meta/external-ids up to 600 times per workday (8h).

## Objectives

- Remove the need to reload all external IDs when a single one changes
- Resolve bottleneck for external ID updates
- Make AccountCache immutable
- (optional) Allow for authentication to happen using only in-memory data
- Provide fast lookups using only primary storage for:
  - ExternalID => Account (used for authentication)
  - Primary email address => Account (used for different internal operations, mostly around Git PersonIdents)
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

Besides enabling reverse lookups, the new `refs/index/` refs guarantee uniqueness. This is especially important for
external IDs, which should only ever be associated with a single account.

When updating an external ID, the respective refs are updated atomically in a BatchRefUpdate. This covers both the account
ref and the newly created index refs.

Unfortunately, JGit's implementation of BatchRefUpdate on a file repository rewrites the whole packed-refs file on each update.
For smaller systems or systems that don't rely on JGit's implementation, this isn't an issue. Hence they can use BatchRefUpdate
to get atomicity.

For system with more load that are based on JGit's file repository, we will implement an alternative update mechanism that uses
individual ref updates. That uses loose-refs (single files) to avoid aforementioned contention.
The flow is:
1) Update the Note in `refs/index/account-by-external-id/<shard>`
2) Update `refs/users/...`

(2) has a way lower chance of failing. If it fails though, we can recover from the failure:
- If we were just re-assigning the external ID from one account to the other, we know the account
that should have the ID and

Atomicity will be configurable, with the default being `atomicUpdate=true`. We hope that future versions of JGit will offer
a file-based RefTable as alternative to packed/loose refs so that we can just remove the non-atomic path.

### Sharding
The previously outlined ref name specification, contains a <shard> part. This part is computed from the key entity (for
account-by-external-id, that is external-id). The goal is to shard the index onto multiple refs to avoid lock failures
when updating it.

The shard is computed from `SUBSTRING(SHA1(entity), x)`. For now `x = 1` which means 6 (A-F hex) + 10 (digits) = 16
shards. The parameter is not configurable dynamically, but can be adapted in the future requiring a data migration.

### Caching

#### Accounts
After the primary storage migration, all data in `AccountState` is derived from contents of the account ref. This enables us
to make the account cache be immutable and serialized to disk.

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

### Data Integrity

`refs/index/...` and `refs/users/...` have a potential to get out of sync. We will provide a Gerrit program
that can be run manually or automated to check the integrity of the data and fix up inconsistencies.

We expect no inconsistencies if atomic updates are used.

Administrators can update refs manually by performing a `git push`. Gerrit will check consistency of these
modifications using an enforcer in ReceiveCommits.

Manual updates to the files or branches using core git on the source-of-truth directly are discouraged, but still possible.

Aforementioned programs can be used to check and regain consistency.

### Migration

Migration will be done with a schema upgrade.

### Debuggability
Admins frequently debug access issues for users that sometimes relate to problems with external IDs. The most frequent
operation is looking up an account by ID and checking the history as well as correlating that with external ID updates.

The new schema supports this and in fact makes it easier as the account ref is then the single source of truth.
We expect admins to manually check either one of the lookup indices infrequently.

### Alternatives Considered

#### Keep the current system
On googlesource.com (this applies also to open-source installations), users are spending tens of hours / day on aggregate waiting for Gerrit to return a request while Gerrit is reading external IDs. This is not acceptable.

#### Fix just the read bottleneck

We could leave the system as-is and just try to address the largest pain point: Read gaps in the ExternalIdCache.

This is hard, but could be done using by incorporating the NoteMap keys (SHA1s) in the key. We are OK having the ref's
tip SHA1 in a cache key requiring us to have the ref available each time we access a cached value and performance-wise,
this is battle-proof. However, we don't want to take this one step further and use NoteMap keys as that would require
reading repo contents.

Besides that, all other outlined problems would remain.

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

#### Use the secondary index instead of refs/index/...

We relied on the secondary index for authentication in the past and it was a disaster. There were issues where users
were sent to infinite redirect loops because of data inconsistencies and other issues that made it clear that
during authentication we only ever want to rely on primary data.