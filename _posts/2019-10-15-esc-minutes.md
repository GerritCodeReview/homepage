---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-10-15-esc-minutes.html
summary: "Minutes from the ESC meeting held on October 15th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, October 15, 2019

### Attendees

David Pursehouse, Luca Milanesio, Patrick Hiesel

### Place/Date/Duration

Online, October 15, 12:30 - 13:00 CEST

### Next meeting

The next meeting will be held on October 30, 12:30 CEST.

## Minutes

### Gerrit News Page

The next issue of the project news is due to be published on November 29.

So far it only contains one item by Edwin about the new plugin steering
group.

There were no new items proposed during this meeting. Patrick will
follow up with the frontend team at Google to see if they have anything
to add related to their recent work.

Members of the community may propose items by adding a change on the
[draft post](https://gerrit-review.googlesource.com/c/homepage/+/239186).

### Security issue with LDAP and Java 11

[Issue 11567](https://bugs.chromium.org/p/gerrit/issues/detail?id=11567)
reports that LDAP startTLS doesn't work as expected on Java 11 and is
marked as a security issue.

There has been a lot of discussion around the issue, and the conclusion
is that it's an issue with Java 11 rather than with Gerrit. Since Java 11
is not yet an officially supported runtime anyway, this issue doesn't
need restricted visibility.

### Status and metrics for gerrit-review.googlesource.com

Luca pointed out that recently the performance of gerrit-review has been
slow, and requested that some kind of status page be provided so that users
can see if there are any known issues.  Patrick will look into this.

### Scaling Gerrit

Patrick mentioned that some Gerrit features don't perform well at scale,
for example the mergeability indexing. This is discussed in more detail
in [these design documents](https://gerrit-review.googlesource.com/q/topic:indexing-mergeable).

In general, we agreed that it's better to first attempt to find a way to
improve scaling performance, but if that doesn't work then we should
prefer to allow the feature to be optionally enabled/disabled rather than
completely removing it.

### Renaming of 'reviewdb' package to 'entities'

In the previous meeting it was agreed that we will go ahead with the
package rename for Gerrit 3.1.  David Ostrovsky has rebased the change
and associated plugin changes, and it is now ready to be approved and
submitted. Alice was working on this, but is away at the moment, so
Patrick will take over.

### Building JGit from source

The change that adds support to build Jgit from source is now working
as expected and only lacks the Library-Compliance vote. Patrick agreed
to apply that vote so that the change can be submitted.

### Migration of Lucene indices to use dimensional types

The [series of changes](https://gerrit-review.googlesource.com/q/topic:lucene-dimensional-numeric-types)
to migrate the Lucene based secondary indices to use dimensional types
is still pending, and is marked as blocking the 3.1 release. Although
the changes are related to Lucene they also required some changes in the
Elasticsearch implementation, so David asked Patrick to have a look at
them to check if they will also have impact on Google's index backend.

### Follow up on blocking issues for 3.1

Per the release plan for 3.1 we expect to cut the stable-3.1 branch and
make the first release candidate at the end of this week.

We had a look at the list of issues that are labelled `Blocking-3.1` and
the open changes that have the hashtag `blocking-3.1`. Aside from the changes
already discussed in this meeting, there are still a few PolyGerrit related
items.

### Topics for the upcoming hackathon

Luca suggested that we make a list of topics for the upcoming hackathon. He
also suggested that, like the hackathon in Sweden, regular contributors
should donate some of their time to help new contributors get up to speed.

David pointed out that some of the maintainers' time will be decidated to
stabilizing and finalizing the 3.1 release during the week.

### Remove the internal gitweb servlet

Following on from the last meeting's discussion of repository browsing,
David suggested that we remove the internal gitweb servlet and focus on
improving the integration with the gitiles plugin which is now a core
plugin. Everyone agreed that this is a good idea, but we should postpone
it until after the 3.1 release.

### Roadmap

There was no further discussion about the Gerrit roadmap. Alice has set
a separate meeting for 22nd October.

### Review of issues on the ESC component

We briefly went over the issues that have been added to the
[ESC component](https://issues.gerritcodereview.com/issues?q=status:open%20componentid:1371029)
on the issue tracker and did not find any that need urgent attention.
