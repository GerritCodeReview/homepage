---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2022-01-12-esc-minutes.html
summary: "Minutes from the ESC meeting held on Jan 12, 2022"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Jan 12, 2022

Christophe Poucet, Han-Wen Nienhuys, Luca Milanesio, Matthias Sohn,
Patrick Hiesel, Saša Živkov.

### Next meeting

Feb 2, 2022

## Minutes

## Proposal to drop Log4J completely and use java.util.logging

Google does not use Log4J, and Gerrit does not require it directly because it is
based on Flogger. Can we drop Log4J altogether in Gerrit?

After an initial analysis, it looks like some of the components that Gerrit uses
(e.g., Apache Mina SSHD) still refer to Log4J directly; therefore, removing it
won't be trivial.

Matthias pointed out that the reload4j project (https://reload4j.qos.ch/) has
fixed the vulnerabilities found on Log4J 1.x and made the fork available to the
community with the same Open-Source license.

The removal of Log4J is put on hold, waiting to see if the reload4j project may
work in the meantime.

## Definition of a policy for updating JGit on stable Gerrit branches

Gerrit and JGit have different release schedules: twice a year for Gerrit, four
times a year for JGit. Also, there is reluctance in updating JGit pointer in
Gerrit stable not-EOL branches because of the fear of potential regressions.
The two factors have contributed to the accumulation of lag in the alignment of
the latest JGit version in Gerrit. For example, both Gerrit v3.4 and v3.5 use
JGit v5.12, six months behind the latest.

The consensus is to define a policy for updating JGit pointer on a regular basis
as follows: Gerrit/master updates its submodule to JGit/master regularly. After
two weeks of tests by Google (using the JGit fork) and GerritForge (using the
JGit vanilla), the update is performed on the non-EOL stable branches, assuming
that there are no breaking JGit API changes stable branches that are in EOL
will not have any regular JGit updates

## Delay in Gerrit releases due to the review of release notes

The Gerrit release notes are created and reviewed too late in the process,
causing potential delays and potential mistakes and gaps in the initial Gerrit
versions. Ideally, updating the release notes should be part of the review
process of the changes that are modifying or creating new functionalities,
rather than a one-off task for the release manager.

We had the idea of implementing the mechanism of validating the presence of
release notes in the submit rules; however, that did not take off. Patrick
takes the task of assessing a similar check by using the new submit
requirements available in Gerrit master.

## Proposal to drop Java-8 support for stable-3.3/3.4

Gerrit v3.3.* and v3.4.* are distributed only for Java 11; however, during their
development SAP and Google needed to preserve the source-code compatibility to
Java 8 for being able to upgrade and deploy to their respective Java 8-based
setup. Nowadays, SAP and Google are on Java 11; therefore, there is no need
anymore to keep source-code level compatibility with Java 8.

The consensus is to drop Java 8 source compatibility for stable-3.3/3.4 to
switch the whole Gerrit CI/CD pipeline to Java 11, avoiding complicated
if/then/else in the build scripts.

Luca has created [a small survey](https://www.surveymonkey.co.uk/r/8CQ5BH7)
for asking the community which Java version is used with Gerrit v3.3/v3.4.
Once the results are available, the project can make a final decision on the
matter.

## Proposal to define a trusted group of contributors for running CI builds

Currently, any incoming Gerrit change triggers a CI build, posing security risks
because the execution happens *before* any review or validation by
contributors. Both the Jenkins-based pipeline
(https://gerrit-ci.gerritforge.com) and the Zuul pipeline
(https://ci.gerritcodereview.com) are impacted but with different security
issues.

The use of RBE for the build execution mitigates the problems partially because
some of the build steps have to be executed on the agents anyway
(e.g., PolyGerrit tests).

The possible options are introducing further isolation layers
(e.g., https://gvisor.dev/docs/) or using a service such as Google Cloud Build.
Han-Wen will explore this second option.
