---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2022-02-08-esc-minutes.html
summary: "Minutes from the ESC meeting held on Feb 9, 2022"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Feb 9, 2022

Christophe Poucet, Han-Wen Nienhuys, Luca Milanesio, Patrick Hiesel, Saša Živkov.

### Next meeting

March 2, 2022

## Action items

As discussed, adding a Submit Requirement for the `Release-Notes:` footer.

## Dropping Java 8 for v3.3/v3.4?

Java 8 is only for custom builds; we won't add Java 11 language
features to the stable branch.

Decision: Java 11 is the official version. Java 8 should work, but
requires custom build.

## Draft release plan for Gerrit 3.6 / Spring hackathon

SubmitRequirements will be finished by the time 3.6 is out; Google
rolling it out this week.

SAP/Google can't commit to travel plans due to covid policies, and
will participate virtually. Paladox will help with backporting FE
fixes from `master` to `stable-3.6`.

## Delays for Library-Compliance

An escalation route was documented by Edwin.

## Making OAuth a core plugin.

OpenID is deprecated, we should support OAuth out of the box to
provide a good experience for standalone usage. The current maintainer
(David O) is also Gerrit Maintainer, and is used by GerritForge for
Gerrithub.

Corporate deployments tend to use SAML rather than OAuth.

Consensus: this is OK.

## GCP credits for Gerrit CI

The Gerrit CI workers cause toil for the Google team, as the VMs are
in scope for compliance and security scanning. Han-Wen will
investigate offering GCP credits to Gerritforge; cost of CI VMs is not
a primary issue for Gerritforge.

## Ignoring self-approvals for gerrit-review.googlesource.com

This was brought up, but the change was
[documented](https://www.gerritcodereview.com/2021-06-01-esc-minutes.html#accidental-breakage-of-the-conflicts-ui-in-v34).
ESC is open to change process and suggestions how to disseminate info
better. Perhaps CC the community managers?

## repo-discusss subscribed to Stackoverflow?

This was suggested in the community meeting. Only questions with the
gerrit tag are mirrored.

## Open designs

No news

## Roadmap

Han-Wen to publish Google quarterly goals for Q1.

## ESC issues

Discussion about potential DoS problem; cannot currently be disclosed.
