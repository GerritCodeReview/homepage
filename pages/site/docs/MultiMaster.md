---
title: "MultiMaster"
permalink: multimaster.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---


We spent some time at the May 2012 Hackathon outlining an incremental approach
to making open source Gerrit clusterable (the version running for android-review
and gerrit-review is already clustered but uses much of Google's proprietary
technologies such as GFS and BigTable). Several incremental steps were outlined
on how to move Gerrit in that direction.

## Shared Git Repo - Shared DB

This is the simplest case for Gerrit multi master, so it is likely the first
step which is needed by most other ideas is to support a very simple
master/master installation of Gerrit where both (or all if more than 2) masters
share a common filesystem backend (likely a high end NFS server) and a common
db.

Four issues have been identified here which need to be resolved before this is
possible:

1.  Cache coherency and
1.  Submit conflict resolution
1.  Mirror/Slave Replication
1.  User sessions

A naive approach to #1 is to simply use really short cache times, but this sort
of defeats the purpose of caching. To solve this properly, some sort of eviction
protocol will need to be developed for masters to inform their peers of a needed
eviction (a plugin is up for [review]
(https://gerrit-review.googlesource.com/#/c/37460/1) which does this using UDP).

## 2 could be easily solved by manually determining a submit master and later

Upgrading to some sort of voting mechanism among peer masters to choose a submit
master, these would be incremental approaches. The issue is that each server
runs a plugin queue and can therefor can attempt to merge changes to the same
branches at the same time resulting in "failed to lock" errors which will leave
failed to merge messages on changes. If the same change makes it into multiple
queues, might it also cause issues by attempting to being merged twice? If a
peer goes down, might its queue be the only holder of certain changes which then
will be missed until a restart of some server?

## 3 can be solved similarly to #2

Select a replication master. The replication master is responsible to rerun full
replication on startup and anytime a master goes down (since it may have currently
been replicating something). Otherwise, masters can replicate as they would normally
(as a single master) as they cause ref updates. Since there is a bug where replication
"failed to lock" attempts are not retried currently, this should also be fixed since
they will likely be even more prevalent with multi master setups.

A simple ssh connection between peers was deemed sufficient in most cases to
accomplish both #1 and #2. Although a single form of communication is not very
good since it prevents the cluster from distinguishing between a downed node and
a network split. Without being able to distinguish this, the cluster cannot
dynamically adapt when communication is down with a peer. Likely a cluster
should have a backdoor com channel to help indicate inter node network failures,
since the DB and the Repos are shared in this scenario, either could easily be
used for the back door channel (CAF is using the repos:
All-Projects:refs/meta/masters/node).

Spearce has a solution to #4

A [thread]
(https://groups.google.com/d/msg/repo-discuss/ZIIuBaCz9Jc/ZTQGpuy_Y1MJ) about
some what is required for this setup to work well.

## Multi Site Masters with Separate Backends

The main additional problem with separate backends is: resolving ref updates in
a globally safe way. In Google’s implementation, this is solved by placing the
refs in BigTable. ZooKeeper seemed like a good free/open source alternative
since it is Java based and under the Apache license. The other piece to solve is
moving object data across sites, it was suggested that ZooKeeper would likely be
involved in helping to coordinate this, but details were not really discussed.

A plugin for ZooKeeper ref-db is up for [review]
(https://gerrit-review.googlesource.com/#/c/37460/1).

## Distributed FS

Finally, it was felt that once multi sites were conquered, that a distributed
filesystem may eventually be needed to scale the git repos effectively, Hadoop
DFS was proposed for this.
