---
title: "Tentative Roadmap"
permalink: roadmap.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

The Gerrit roadmap is a best-effort collection of features/improvements that the ESC is aware of.
The intention is to give the wider community - contributors as well as administrators and users - a
sense of what they can expect to see in upcoming releases.

This is a living document, so things can change anytime. There is no ordering between
features/improvements.

If you’re a contributor and you intend to work on something which is not mentioned here, please
create a change and select the ESC members as reviewers. Don’t use this channel to submit ideas or
wishes you want someone else of the community to work on!

If someone would like to be involved when a specific topic is tackled, please
[reach out to the ESC](https://gerrit-review.googlesource.com/Documentation/dev-roles.html#steering-committee-member).

Gerrit community half-yearly plans, to align with the release schedule.
The plan uses the OKR (Objective/Key-Result) framework.

## Gerrit 3.12
Target: H1 2025

### O: JGit performance improvements

#### KR: Speed-up conflicting ref names on push
#### KR: Improve searchForReuse latency for large monorepos by at least one order of magnitude
#### KR: Improve object lookup across multiple packfiles by at least one order of magnitude
#### KR: Parallelize bitmap generation across multiple cores

### O: Gerrit dependencies updates

#### KR: Drop Java 17 support and fully adopt Java 21 for source and binaries
#### KR: H2 backend upgrade to v2.3.232
#### KR: Update JGit to master (currently v7.2)

### O: Gerrit Core improvements

#### KR: Support X.509 signed commits [Issue 380211814](https://issues.gerritcodereview.com/issues/380211814)
#### KR: Production support for ref-table in Gerrit cache [Issue 392541994](https://issues.gerritcodereview.com/issues/392541994)
#### KR: New index metrics [Issue 381216361](https://issues.gerritcodereview.com/issues/381216361)
#### KR: New ACL permission for posting reviews to prevent spam on gerrit-review [Issue 391666234](https://issues.gerritcodereview.com/issues/391666234)
#### KR: Prolog rules disabled by default

### O: Gerrit UI experience improvements

#### KR: Improved syntax highlighting when reviewing SVG and toml files
#### KR: Automatic commit message formatting
#### KR: Allow edit suggestions in commit message

### O: Owners Plugin

#### KR: Explicitly display which actions are required by each owner on a file level basis [Issue 380211816](https://issues.gerritcodereview.com/issues/380211816)
#### KR: Give more details on pending reviews by owners [Issue 380113193](https://issues.gerritcodereview.com/issues/380113193)
#### KR: Allow to contact the file owner more easily [Issue 380125109](https://issues.gerritcodereview.com/issues/380125109)

### O: Make analytics plugin faster and easier to use

#### KR: Natively support repo manifest discovery [Issue 380282334](https://issues.gerritcodereview.com/issues/380282334)
#### KR: Faster extraction of metrics for branches [Issue 380282335](https://issues.gerritcodereview.com/issues/380282335)


## Gerrit 3.13
Target: H2 2025

### O: JGit performance & concurrency improvements

#### KR: Improve push performance by allowing skipping of connectivity checks
#### KR: Improve push performance by allowing skipping of collision checks
#### KR: Customize lock-interval retries
#### KR: Support read-only multi-pack index

### O: Gerrit Core and UI experience improvements

#### KR: Allow filtering file list in change review screen [Issue 380234236](https://issues.gerritcodereview.com/issues/380234236)
#### KR: Package headless Gerrit serving only read/write git protocol [Issue 380234237](https://issues.gerritcodereview.com/issues/380234237)

### O: Update Kafka events-broker

#### KR: Support Kafka 3.9.0 [Issue 380282493](https://issues.gerritcodereview.com/issues/380282493)

### O: Update Zookeeper global-refdb

#### KR: Support Zookeeper 3.9.3 [Issue 380234239](https://issues.gerritcodereview.com/issues/380234239)

### O: Make Push/Pull Replication Plugins easier to configure

#### KR: Introduce APIs for dynamically creating and updating replication endpoints [Issue 380234240](https://issues.gerritcodereview.com/issues/380234240)
#### KR: Surface replication status on UI [Issue 380234241](https://issues.gerritcodereview.com/issues/380234241)
#### KR: Improve replication latency on force-push (apply-object with prerequisite) [Issue 380282333](https://issues.gerritcodereview.com/issues/380282333)

## k8s-Gerrit

Roadmap for k8s-Gerrit can be found [here](https://gerrit.googlesource.com/k8s-gerrit/+/refs/heads/master/Documentation/roadmap.md)

## Gerrit 4.0
Target: 2026/2027

### O: Decouple Gerrit review UI review and JGit Server

#### KR: Allow to deploy Gerrit UI and JGit Server as separate and independent services [Issue 381906253](https://issues.gerritcodereview.com/issues/381906253)

#### KR: Enable other review UIs on top of JGit Server (e.g. pull-requests) [Issue 381906254](https://issues.gerritcodereview.com/issues/381906254)
