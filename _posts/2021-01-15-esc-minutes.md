---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-01-15-esc-minutes.html
summary: "Minutes from the ESC meeting held on January 12th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, January 12, 2021

### Attendees

Ben Rohlfs, Han-Wen Nienhuys, Patrick Hiesel, Luca Milanesio, Saša Zivkov

### Place/Date/Duration

Online, January 12, 11:00 - 11:45 CET

### Next meeting

The next meeting will be held on February 2, 11:00 CEST.

## Minutes

### Gerrit long-term stable releases (LTS)

Should the Gerrit project start keeping long-term support branches for one or
more releases of Gerrit? The current [EOL policy](https://www.gerritcodereview.com/support.html#supported-versions)
defines an 18 months (3 releases) lifetime. Gerrit v2.16, released back in
November 2018, represents an exception and will be kept for longer to allow
existing pre-2.16 installations to migrate to Gerrit v3.x and beyond.

The proposal to an extended support cycle for some elected LTS releases has been
unanimously rejected for the following reasons:

- The LTS branch would need strong governance on what can and cannot be added. The code-base
  could diverge from the mainstream development and eventually become a _de-facto_ fork of Gerrit.

- Web-browsers may not have an LTS support policy aligned with Gerrit, causing compatibility
  issues and additional hurdles to support browser upgrades. E.g. Firefox Enterprise Edition support
  is limited to 1 year.

- The Gerrit Community focuses on helping to migrate to more recent and modern releases, such as v3.3
  with attention-set. Having an LTS release for 5-10 years would give further incentive
  for companies to shelf current upgrade plans.

 - Older versions of Gerrit have more issues with rough edges on the user experience, which people see
   and use to judge the product. Having more obsolete LTS versions of
   Gerrit around would bring even more bad PR to the product itself.

### Zuul for gerrit itself

The Gerrit Code Review project has started adopting [Zuul](https://zuul-ci.org/) from 2019/2020 and
it is now used for the build of a large number of plugins on the [Gerrit Zuul CI instance](https://ci.gerritforge.com).

Han-Wen proposed to extend the adoption of Zuul to the CI of Gerrit itself.
There is consensus to proceed, assuming that Zuul has bridged the gap for supporting Docker-based
build agents, instead of GCloud VMs. Luca will follow up with James (Zuul maintainer) to check
the status and plan the next steps.

### Status of dropping Java 8 support for Gerrit

Google is planning to move to Java 11 in H2/2021, allowing to drop the support for Java 8 build
validation on Gerrit master. The target release for dropping Java 8 is therefore Gerrit v3.5, while
Gerrit v3.4 will continue to support Java 8 compilation.

### What's cooking in GerritForge for 2021

Luca shared the [GerritForge’s shopping list for 2021](https://gitenterprise.me/2021/01/04/2021-whats-cooking-in-gerritforge/)
which contains:

- The support for cloud-native events-brokers: Google's GCloud Pub/Sub and AWS Kinesis streams
- Proto-buffers for representing events for Gerrit v3.4
- Further improvements in the pull-replication plugin
- Integration of Jenkins with the new CI reboot in Gerrit v3.4

### Policies for PolyGerrit dependencies up-to-date

Gerrit Code Review code-base is mirrored on the [GerritCodeReview project in GitHub](https://github.com/gerritcodereview)
which automates the [Dependabots's security checks and warnings](https://dependabot.com/).

Ben will be also added to the list of GitHub project's owners so that the PolyGerrit Team can
receive and assess all the feedback provided by Dependabot.

### Top #3 PolyGerrit-related show-stoppers vs. GWT UI

GerritForge has performed a survey with its clients to identify the top #3 problems
that companies have indicated as show-stoppers for migrating to PolyGerrit in Gerrit v2.16
and beyond.

1. [Issue 40012178](https://issues.gerritcodereview.com/issues/40012178): Horizontal spacing usage

2. [Issue 40013256](https://issues.gerritcodereview.com/issues/40013256): Lack of CSS customisation

3. [Issue 40011499](https://issues.gerritcodereview.com/issues/40011499): Gap in browsers support

There is positive attitude for discussing those issues with Ben and the PolyGerrit Team and
find possible solutions. GerritForge has offered its development Team to cooperate with the
development and fix of the above issues, with the agreement of the rest of the community.

### Eclipse moving away from Gerrit

The Eclipse system administrator has announced the intention to move away from Gerrit.
Matthias described the current situation for at least JGit/EGit projects and the intention
to keep Gerrit as code-review system for the projects.

The discussion inside the Eclipse foundation continues, there are no actions for the ESC
at this point in time.
