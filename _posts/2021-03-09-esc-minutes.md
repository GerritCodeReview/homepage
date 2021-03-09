---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-03-09-esc-minutes.html
summary: "Minutes from the ESC meeting held on Mar 9, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Mar 9, 2021

### Attendees

Ben Rohlfs, Han-Wen Nienhuys, Luca Milanesio, Patrick Hiesel, Saša Živkov

### Place/Date/Duration

Online, Mar 9, 11:00 - 12:00 CET

### Next meeting

Apr 06, 2021 - 11:00 - 12:00 CET

## Minutes

### Follow-up actions

* ElasticSearch in Gerrit core

  Background on the issue: ElasticSearch moved releases to SSPL starting 7.11.
  Google is opposed to SSPL software on principle. SAP also forbids it.

  Han-Wen contacted Ericsson and Digital.ai: both confirmed that ElasticSearch
  is not used yet in production and there are no dates defined yet.
  Luca will propose on the mailing list to remove ES from Gerrit core and,
  if needed, can be later supported as a non-core libModule.

* Gerrit events rewrite and GCloud pub/sub notifications

  Han-Wen has proposed [Change-Id: Ia54acb37](https://gerrit-review.googlesource.com/c/gerrit/+/296326)
  which represents the beginning of the initiative of having Gerrit
  notes exported as events. The
  [previous design in review posted by Alice](https://gerrit-review.googlesource.com/c/homepage/+/280925)
  has been abandoned because largely outdated compared to the current
  status on Gerrit master.

### Patch-set comment experiment in Gerrit v3.3

The [patch-set level comment](https://www.gerritcodereview.com/3.3.html#new-features)
introduced in Gerrit v3.3 as an experiment could become an official
features in v3.4.

Luca proposted [Change-Id: I57569fb](https://gerrit-review.googlesource.com/c/gerrit/+/291225)
for exposing the additional messages to stream events, so that CI systems can
leverage it. Once the change is merged, both Zuul and Jenkins integrations
would need to consume the new information.

### ElasticSearch moved to SSPL

ElasticSearch moved releases to SSPL starting 7.11. Google is opposed
to SSPL software on principle. SAP also forbids it.

Context: index support started with Lucene and Solr. Solr was clunky,
so collabnet and ericsson worked to move to Elastic, but neither
deployed. Alibaba seems to be using it.

Long term technical solution: use ES as a module (ie. a non-swappable
part of Gerrit, compiled separately). ES also slowed down our
development, so getting rid of it may be a net positive.

Resolution: we will freeze the version for now. Han-Wen will reach out
to Jacek and Marco to see if they have interest in maintaining it.

### Design docs vs code guideline/process

Qualcomm requested to have more clarity on when a design document is
required vs. just submitting the proposal a working code in a Gerrit
change for review.

In the past the community was a lot smaller and Shawn was overseeing
the whole code-base and could have given a lot of guidance without
the need of a lot of input from other contributors.

There is a general consensus though that a short-track of posting
a change with a meaningful commit message could still be good enough
when:

- the change is small and has a limited impact on Gerrit functionality
- introduces a clear and limited functionality
- enables a trivial use-case without edge cases
- allows only one simple solution, without alternatives

For all other cases, a design document is still the most valid
approach to trigger the exchange of ideas around the new feature.

### Status of the Gerrit CI pipeline changes

The adoption of [Zuul](https://zuul-ci.org/) continues and the next
step will be the validation of Gerrit changes. Once that is completed,
Zuul can then move into the next steps of:
- Supporting builds on RBE
- Supporting Docker-container based tests

The current [Jenkins-based CI pipeline](https://gerrit-ci.gerritforge.com) will
still be needed though for all the other builds not related to incoming
changes:
- plugins stable builds
- E2E tests
- Other libraries

### Spring cleaning of Gerrit REST-API

The front-end team is tracking which Gerrit API are unused and is
planning to remove them on master, which will become Gerrit v3.4:

- Drop of Polymer2 cruft
- Removal of *some* of 50 different API methods

The initiative is guided by data observed on `*.googlesource.com`
and a list of proposed dropped API will be also posted to repo-discuss.

### Decommission of JSch on Gerrit master

David has driven the initiative of [moving away from JSch](https://gerrit-review.googlesource.com/c/gerrit/+/269976)
and adopting instead Mina SSH client.

Han-Wen has already reviewed and provided the green light, Patrick is now
reviewing the change and finalising the merge.

### Release plan for Gerrit v3.4

David has proposed the [Gerrit v3.4 release plan](https://gerrit-review.googlesource.com/c/homepage/+/298876)
targeting a release date of May 17. The plan looks good and has been approved.

There is a general agreement that we should continue to target Java 11 as a runtime,
keeping the ability to be able to build the code from source on Java 8 as well.

Saša expressed the concern that in Gerrit v3.3 some plugins (e.g. high-availability)
may not be able to compile on Java 8 because of Java 11-only dependencies.
Luca has fixed the issue with the high-availability plugin (global refdb with
java8 classifier) but raised the concern that we cannot force all plugins' developers
to respect that norm.

There is a consensus that core plugins will continue to be compatible with Java 8
at source level, with the recommendation (but not requirement) to do the same for
the other plugins.

### Gerrit v3.3 and double-release on Java 8

Luca presented the data about the adoption of Java 11 on the latest versions of
Gerrit:

- Gerrit v3.3 JVM statistics: 3399 setups (up to 3rd Feb 2021)
  * Java 11 (96.3%)
  * other (3.6%)
  * Java 8 (0.1%)
- Gerrit v3.2 JVM statistics: 5915 setups (up to 3rd Feb 2021)
  * Java 11 (57.2%)
  * Java 8 (41.6%)
  * other (1.2%)

Saša mentioned the need for SAP to keep on having the source code to compile
on Java 8, but not necessarily the requirement to have Java 8 distribution or
binaries.

The consensus is to keep the current policy of releasing only on Java 11 to keep
the current adoption rate.

### New features on EOL branches

Following the [Change-Id: Ifebae17f](https://gerrit-review.googlesource.com/c/gerrit/+/298880)
proposed by Luca, Han-Wen proposed to make the policy even more restrictive and
ban the introduction of new features in any stable branch.

That should also include 3rd party dependencies (either Google or non-Google ones) unless
they are required to address critical and security bugs.

There is a general consensus that brand-new features should be introduced only on master and,
if needed cherry-picked on a un-maintained private fork should anyone needed on an earlier
stable branch.

### Roadmap updates

- Protobuf in Gerrit events: Patrick won't be able to finalize this in time for v3.4
- Luca added to v3.4 the introduction of additional cloud-native events-brokers:
  GCloud PubSub and/or AWS Kinesis.
- Saša mentioned that it would be nice to have a redesign/rewirte of the replication plugin
  code somewhere in the future, even though SAP is planning to switch to pull-replication
  which would leverage Git protocol v2.
