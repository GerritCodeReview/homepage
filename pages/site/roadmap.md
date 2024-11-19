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
[reach out to the
ESC](https://gerrit-documentation.storage.googleapis.com/Documentation/3.4.1/dev-roles.html#steering-committee-member).

Gerrit community half-yearly plans, to align with the release schedule.
The plan uses the OKR (Objective/Key-Result) framework.

> NOTE: To identify the owner of each objective, git-blame the file.

## Gerrit 3.12
Target: H1 2025

### O: JGit performance improvements

#### KR: Speed-up conflicting ref names on push
#### KR: Improve searchForReuse latency for large monorepos by at least one order of magnitude
#### KR: Improve object lookup across multiple packfiles by at least one order of magnitude
#### KR: Parallelize bitmap generation across multiple cores

### O: Gerrit Core experience improvements

#### KR: Support X.509 signed commits

### O: Owners Plugin

#### KR: Explicitly display which actions are required by each owner on a file level basis
#### KR: Give more details on pending reviews by owners
#### KR: Allow to contact the file owner more easily

### O: Make analytics plugin faster and easier to use

#### KR: Natively support repo manifest discovery
#### KR: Faster extraction of metrics for branches


## Gerrit 3.13
Target: H2 2025

### O: JGit performance & concurrency improvements

#### KR: Improve push performance by allowing skipping of connectivity checks
#### KR: Improve push performance by allowing skipping of collision checks
#### KR: Customize lock-interval retries
#### KR: Support read-only multi-pack index

### O: Gerrit Core and UI experience improvements

#### KR: Allow filtering file list in change review screen
#### KR: Package headless Gerrit serving only read/write git protocol

### O: Update Kafka events-broker

#### KR: Support Kafka 3.9.0

### O: Update Zookeeper global-refdb

#### KR: Support Zookeeper 3.9.3

### O: Make Push/Pull Replication Plugins easier to configure

#### KR: Introduce APIs for dynamically creating and updating replication endpoints
#### KR: Surface replication status on UI
#### KR: Improve replication latency on force-push (apply-object with prerequisite)
