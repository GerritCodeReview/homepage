---
title: "Gerrit Community Manager Meeting Minutes"
tags: gcm
keywords: gcm minutes
permalink: 2025-03-13-community-managers-minutes.html
summary: "Minutes from the community managers meeting held on March 14th, 2025"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

# Gerrit Community Managers Meeting, March 14th, 2025

**Participants**: Daniele Sassoli [DS], Nasser Grainawi [NG], Mathias Sohn [MS]

## Bi-Weekly Catch-up Meetings

These catch-ups have been happening regularly every 2 weeks for many years, however, despite the
agenda being public, they've not really been advertised.
DS suggested writing up minutes every time some worth sharing is discussed, as it happens for the
ESC, and so, here we are.

## Gerrit User Summit 2025 Planning

Organization of the User Summit for 2025 has started with the aim to hold it again around October
time. We currently have interest by a few companies but no firm commitments. If you or your company
is interested in hosting the User Summit feel free to reach out to DS, Luca or any community
manager.

## Reducing spam on both issue tracker and gerrit.googlesource

The community managers, together with the ESC, have agreed that membership to repo-discuss should be
required in order to post comments on [changes](https://gerrit-review.googlesource.com/) or
raise issues on [issuer.gerrit](https://issues.gerritcodereview.com/).
This will allow us to ban users who are found to post spam content.

In order to do this a new permission will be required in Gerrit core, as it's not currently possible
to prevent someone to post comments on issues while still allowing read access. DS has already started working on this as part of
[454501](https://gerrit-review.googlesource.com/c/gerrit/+/454501). This will require careful
consideration from Google as they're running on master, Edwin has advised that they'll be able to
plan this for the second half of the year.

We're sure this will be a welcome change as everyone can agree spammers have caused quite a lot of
noise over time on our platform.

## GerritMeets

GerritMeets is progressing nicely with a talk planned in March on caching backend for Gerrit.
April's talk is already lined up too and will see a case-study from Google and Accenture on using
Gerrit as part of a wider framework for developing with the Android platform with a focus on the
automotive space.

