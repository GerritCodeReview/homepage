---
title: "Scaling Dimensions"
permalink: scaling.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Scaling Dimensions

As you scale, you will always run into some issues. Depending on your specific
setup those issues may be very different from what other people are running
into. Some of the specific dimensions which people may or may not need to scale
on are:

*   Number of Changes: Several sites have close to 1M changes.
*   Number of Projects: Some Gerrit installs have 20K projects, many have at
    least a few thousand
*   Number of Refs: Several sites have projects with over 100K refs, at least
    one has close to 500K refs
*   Number of Users: Many installs serve 1K users, some serve at least 3K.
*   Number of Groups: Some Gerrit installs use 6K groups (most issues have been
    worked out here)
*   Single Repository Sizes: Some Gerrit projects are 40G aggressively packed,
    these can often cause issues with email templates taking lots of CPU
*   Total Repository Sizes: Gerrit can handle at least 1TB of repository data
    easily
*   Large Files: Gerrit may have difficulty with some very large files (what
    size can it handle easily?)
*   Number of Slaves: Several installations have over 10 slaves per master, at
    least one has 25.
*   Number of Continents with slaves: Slaves for a single master have been
    distributed across at least 3 continents successfully
*   Number of Receive-Packs: Some Gerrit masters are handling 20k receive-packs
    (pushes) per day.

--------------------------------------------------------------------------------

## Servers

### Master

The first step to scaling is to scale your master server. Some easy, but pricey
ways to scale your master are:

*   Adding cores, some of the larger installations use 48 core machines
*   Adding RAM, most of the larger installations have over 100GB, at least one
    has 1TB
*   Ensure fast disk IO, SSDs help prevent serious performance degradation when
    repos are not well repacked (seeks can be crippling here).
*   Network, I suspect that most large installs use 10Gb Ethernet

### Mirrors/Slaves

Once you have a decent master, it is probably worth adding either some git
mirrors (if you do not need ACLs on your repos), or Gerrit slaves to help
offload much of your read only requests. Mirrors/Slaves can also help reduce LAN
and WAN traffic if you place them nearer to your users/build hosts. This can be
particularly useful for remote sites. Some of the larger installations have at
least 25 of these.

#### Shared Storage and Replication Entries For Slaves

A common practice is to use site local shared storage (NFS...) on remote slaves
when there is more than one slave at the remote site. One major advantage of
this is that it reduces the data required to be pushed during replication to
that site. This requires consolidating the replication events to those slaves in
order to avoid having duplicated pushes to the same storage. This consolidation
means that the master replication file will only have one entry for each set of
slaves on the same storage. While a single slave could be setup as the sole
replication receiver, added availability and scaling is being reliably achieved
by using a load balancer on the receiving end to distribute each incoming push
to a different slave (since the back-end storage is the same, they all will
still see every update).

#### DB Slaves

DB slaves are being used on remote sites so that remote slaves do not have to
traverse the WAN to talk to the master DB. Both PostGreSQL and MYSQL are being
used successfully for this. This can be particularly helpful to help reduce some
WAN traffic related to high ref counts when doing repo syncs (the [change cache]
(https://gerrit-review.googlesource.com/#/c/35220) was also designed to help
with this.)

### Multi - Master

The Gerrit MultiMaster plug-in describes how to setup a single site multi-master
with a shared storage back-end for git repository data. However, there are
currently no known sites using the open source MM technology yet. The google
hosted gerrit-review site currently runs in multi-site multi-master mode, but it
relies on proprietary technology to do so.

--------------------------------------------------------------------------------

## Jetty

The default built in web container which Gerrit uses is Jetty. Some
installations have had serious "Failed to dispatch" errors which lead to 100%CPU
and filled up logs, requiring a server reboot to recover. This can triggered by
long running RPCs building causing the http queue to be used. One way to
workaround this issue is to set httpd.maxQueued = 0. Alternatively, you can use
[Tomcat]
(https://gerrit-review.googlesource.com/#/c/35010/6/Documentation/install-tomcat.txt)
instead to replace Jetty.

--------------------------------------------------------------------------------

## Repo Syncs

With beefier servers, many people have [seen]
(http://groups.google.com/group/repo-discuss/browse_thread/thread/c8f003f2247d7157/ad6915f5558df8f5?lnk=gst&q=repo+sync+error#ad6915f5558df8f5)
channel master issues with ssh. Setting GIT\_SSH will cause repo to avoid using
channel master, and thus avoid triggering these errors:

```
export GIT\_SSH=$(which ssh)
```

Is this related to resetting the key after a certain amount of data?

--------------------------------------------------------------------------------

## Java HEAP and GC

Operations on git repositories can consume lots of memory. If you consume more
memory than your java heap, your server may either run out of memory and fail,
or simply thrash forever while java gciing. Large fetches such as clones tend to
be the largest RAM consumers on a Gerrit system. Since the total potential
memory load is generally proportional to the total amount of SSH threads and
replication threads combined, it is a good idea to configure your heap size and
thread counts together to form a safe combination. One way to do that is to
first determine your maximum memory usage per thread. Once you have determined
the per thread usage, you can tune your server so that you total thread count
multiplied by your maximum memory usage per thread, does not exceed your heap
size.

One way to figure out your maximum memory usage per thread, is to find your
maximum git clone tipping point. Your tipping point is the maximum number of
clones that you can perform in parallel without causing your server to run out
of memory. To do this, you must first tune your server so that your ssh threads
are set to a higher than safe value. You must set it to a value at least as high
as the number of parallel clones you are going to attempt. When ready, increase
your testing with higher and higher clone counts until the server tips, then
deduce the point right before it tips. It helps to use your "worst" repository
for this. Once you have found the tipping point, you can calculate the
approximate per thread memory usage by dividing your heap size by your clone
count. If you find that you still have large java gc, you may further want to
reduce your thread counts.

Your luck may vary with tweaking your jvm gc parameters. You may find that
increasing the size of the young generation may help drastically reduce the
amount of gc thrashing your server performs.

--------------------------------------------------------------------------------

## Replication

There are many scalability issues which can plague replication, most are related
to high ref counts, those are not specifically mentioned here, so you will
likely need to first be familiar with the "High Ref Counts" section to make
replication run smoothly.

### JSch

Jsch has threading issues which seem to serialize replication even across worker
groups. This has lead some teams to perform replication without using ssh (Jsch
is the ssh implementation used inside jgit). To do this, you may setup a "write
only" git deamon on your slaves with a port only open to your Gerrit master and
replicate via git daemon without authentication or encryption. This is
particularly useful if you have sites which replicate to at very different
speeds.

### Failed To Lock

With older versions of the replication plug-in, your replication can start
running into contention and failing with "Failed to Lock" errors in your logs.
This can happen when 2 separate threads attempt to replicate the same
project/branch combination (the plug-in no longer allows this). This problem can
resurface even with the newer plug-ing if you run a MultiMaster setup since
nothing currently prevents two different masters running the replciation plug-in
for the same instance from pushing the same ref at the same time.

There are other scenarios besides replication contention that can cause "Failed
to Lock" errors. Fortunately, the current version of the replication plug-in can
be configured to retry these failed pushes.

--------------------------------------------------------------------------------

## High Ref Counts

High ref counts can have impacts in many places in the git/jgit/Gerrit stacks.
There are many ongoing fixes and tweaks to alleviated many of these problems,
but some of them still remain. Some can be "unofficially" worked around.

### git daemon mirrors

Current versions (prior to git 1.7.11) will use an [excessive amount of CPU]
(http://marc.info/?l=git&m=133310001303068&w=2) when receiving pushes on sites
with high ref counts. Upgrading git there can help drastically reduce your
replication time in these cases.

### git

Suggest to your users that they use the latest git possible, many of the older
versions (which are still the defaults on many distros) have severe problems
with high ref counts. Particularly [bad]
(http://marc.info/?l=git&m=131552810309538&w=2) versions are between 1.7.4.1 and
1.7.7. Git 1.8.1 seems to have some speed-ups in fetches of high ref counts
compared to even 1.7.8.

### jgit

jGit still has a [performance problem]
(http://groups.google.com/group/repo-discuss/browse_thread/thread/d0914922dc565516)
with high refs. Two diffenert patches, the [bucket queue]
(https://git.eclipse.org/r/#/c/24295/) patch and the [integer priority queue]
(https://git.eclipse.org/r/5491) patch, have been proposed and will drastically
reduce upload and replication times in Gerrit if applied for repos with many (>
60K?) patch sets.

There are some very high performance patches which make jgit extremely fast.

### Tags

If you have android repositories, you likely use around 400-600 of them. Cross
project tagging can be [problematic]
(http://marc.info/?l=git&m=133772533609422&w=2). There are no good solutions yet
to this problem.

--------------------------------------------------------------------------------

### ACLS

On servers with little or no anonymous access, and large change counts, it can
be disastrous when non-logged-in users access a change-list page. A change-list
page scans all the changes and skips the changes a user cannot see until it has
found enough changes to display which the user can see. When there is no
anonymous access, this may mean traversing all of the changes in your instance
only to return a blank list. When the change count starts approaching 1M
changes, this large change traversal can cripple even a very high scale DB and
Gerrit combination. This is most prevalent on Monday mornings after your users
return to the office and have not logged into Gerrit yet (but are still
accessing it). One hacky way to deal with this is to potentially make a change
to Gerrit to never run the ChangeList page for non-logged in users. However,
this is not a viable solution for public sites. Of course, public sites likely
do not have 1M changes which are not visible to non-logged in users. It may make
sense to make this a configuration option in Gerrit at some point if this cannot
be sped up?

--------------------------------------------------------------------------------

## Disk Space / File Cleanup

Installations which do not have enough spare disk space for their repos can run
into problems easily. Be aware that git repos contain highly compressed data and
that at times this data may need to be uncompressed. It is easy to underestimate
the temporary needs of repositories because git is so good at compressing this
data. However, minor changes can cause repositories to "explode" so it is good
to plan for this and leave a lot of free space for this to never be an issue.
This is particularly important for those using SSDs where they might be more
likely to skimp on space.

### Git GC Repo Explosions

Under certain conditions git gc can cause a repo explosion (jgit gc does not
suffer from this problem because it puts unreachable objects in a packfile),
primarily when unreferenced objects are removed from pack files and are placed
as loose refs in the file-system. Eventually git gc should prune these, but
until that happens serious problems can occur.

Some of the situations which can cause many unreferenced objects:

*   A user uploads a change to the wrong repository and it gets rejected by
    Gerrit
*   Tags are [deleted](http://marc.info/?l=git&m=131829057610072&w=2) from the
    linux repo

### Git GC

Running GC regularly is important, particularly on sites with heavy uploads.
Older versions of jgit do not have built in gc and require using git gc. Setting
up a crontab is probably a good idea in these case. If you do run gc too often,
however excessive pack file churn can also be a problem. A potential [solution]
(https://gerrit-review.googlesource.com/#/c/35215/) for packfile churn:

> nice -n 19 ionice -c 3 gitexproll.sh -r 5 ...

Pack file churn can lead to several issues, RAM utilization, Disk utilization
and excessive WAN utilization for file-system mirroring scripts (such as rysnc).

### Keep and Noz files

Currently, Gerrit may leave behind some temporary files in your git repos when
it shuts down (particularly if ungraceful). There are some temporary files which
begin with "noz", this can consume disk space if left uncleaned. There are also
some .keep files in the objects/pack directories which can be left behind, these
don't in themselves don't take space, but they will prevent git gc from
repacking the packfile they are associated with which can lead to poor disk
space utilization and performance issues.

### ~/.gerritcodereview

The temporary unjared war files in here can build up. (This has been move to
review\_site/tmp in Gerrit 2.5+)

--------------------------------------------------------------------------------

## hooks

Servers with lots of RAM are susceptible to slow forks which can delay each hook
invocation quite a bit. When java uses over 10G of memory, it may add at least a
second to each hook invocation. Using java 7 seems to avoid this problem and
makes hooks blazingly fast again.
