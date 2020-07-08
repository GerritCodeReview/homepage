---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-07-07-esc-minutes.html
summary: "Minutes from the ESC meeting held on July 7th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, July 7, 2020

### Attendees

David Pursehouse, Patrick Hiesel, Luca Milanesio

### Place/Date/Duration

Online, June 7, 12:30 - 13:00 CEST

### Next meeting

The next meeting will be held on August 4, 12:30 CEST.

## Minutes

### Project News

The next news post is due to be published at the end of July. We will
collect news items ad-hoc as this date approaches.

### Secure Pipeline

Luca has set up a secure CI pipeline and will publish Kubernetes artifacts
so that we can spin up this pipeline to test fixes against older releases
on-demand.

### Problematic terminology

The community managers have started an initiative to remove or replace
problematic terminology from Gerrit (For example: "master"). The ESC supports
this initiative.

### Stability fixes for 3.2

There are stability issues with the 3.2 release with respect to the replication
plugin. A fix is being vetted at the moment and will release shorty.

### Maintainership

There is a candidate for a new maintainership that will be discussed with the
maintainers in an offical nomination shortly.

### Review of open design documents

No progress.

### Java 11

We will move to Java 11 being the default JDK before cutting stable branches for 3.3.
This will raise the langage level of the project to 11. We will continue to run
builds for Java 8+ for some time to ensure customers with custom JDKs can still run
Gerrit.

### Review of issues on the ESC component

Patrick went over the list after the meeting and removed issues that aren't in
the ESC's domain.
