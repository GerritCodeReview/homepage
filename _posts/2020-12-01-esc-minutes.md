---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-12-01-esc-minutes.html
summary: "Minutes from the ESC meeting held on December 1st"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, December 1, 2020

### Attendees

Ben Rohlfs, Han-Wen Nienhuys, Patrick Hiesel, Luca Milanesio, Saša Zivkov

### Place/Date/Duration

Online, December 1, 11:00 - 12:30 CET

### Next meeting

The next meeting will be held on January 5, 11:00 CEST.

## Minutes

### New community maintainer nomination

Luca nominated a new community maintainer and the ESC discussed and supports
the nomination. Luca will send an email to the maintainer mailing list following
the official process for nomination.

### Reworking the events system

Han-Wen brought up that Google is doing some internal work in Q1 around
dispatching events (specifically using Cloud PubSub for googlesource.com hosts).

Some of this work might be applicable to open-source as well and built in core.
Mostly, this includes the idea to build a compoenent that can generate events
based off of ChangeNotes and two SHA1s by diffing the state between the two
SHA1s and emitting events for all actions that happened in between.

Luca expressed interest to collaborate on a larger rewrite of the upstream events
system and the aforementioned component.

Saša asked if this work would also enable open-source instances to be hooked up
with Google Cloud PubSub. Han-Wen and Patrick stated that this is possible, but
would require a bit of glue code in a Gerrit plugin to call Cloud PubSub APIs.

### Triaging issues (follow up to Issue 11170, contributor summit)

The ESC discussed if and under what SLA bugs in the project's public issue tracker
are triaged. The Gerrit Frontend team at Google tries to look at frontend bugs as
part of their triage, the backend team only looks at issues labeled with googlesource.com
indicating that the issue can be reproduced on googlesource.com.

The ESCs consensus on this topic is that triage and fixing of issues is done
best-effort. If contributors (both individuals and companies) require a better
SLA, they can either dedicate resources (i.e. contributors to triage and fix issues)
or sign a support contract with a company offering consulting (such as GerritForge).

### Retrospective: 3.3. Release

Luca led a short retrospective to hear how the release went and what can be improved.
Overall, everyone was very happy with how it went and appreciative of the work that
the release managers (Luca and Marco) did.

Ben said that the frontend could have been more proactive with merging Typescript changes
faster and getting in attention set earlier.

Saša thought that there were quite some discussions going on which looked like more churn
than usually. Han-Wen and Patrick said that it looks like this was caused by JGit issues.

There could overall be better tests, especially for longer running JGit operations.

### API Object migration (POJO -> Proto)

Patrick discussed moving from Plain Old Java Objects (POJO) in the API definitions to
using Protocol Buffers (Protos). We already use Protos in different parts in Gerrit
(e.g. caches).

This has the benefit that objects are immutable (especially interesting to the events
system) and can be reused client side to implement REST API clients in any language
without duplicating definitions.

Ben said that the frontend would welcome this move.

The consensus was that we move forward with that migration. Since it's under the hood,
no design doc is required.

### Open Designs

James Blair has a design open for the checks plugin. Ben has a tentative plan to hook
up the checks plugin with the new CI plugin interface. James is welcome to continue
working on the checks plugin, but this work doesn't require a design doc.

Luca hopes that the work on the pluggable auth backlend gets picked up soon.

### Roadmap

The ESC went over the internal roadmap doc once more and will update the public roadmap
soon.

### Open issues

Han-Wen will write a post on the homepage explaining how Google does triage of upstream
issues and Luca will do the same for GerritForge.



