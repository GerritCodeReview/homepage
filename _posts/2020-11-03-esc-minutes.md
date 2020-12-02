---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-11-03-esc-minutes.html
summary: "Minutes from the ESC meeting held on November 3rd"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, November 3, 2020

### Attendees

Ben Rohlfs, Patrick Hiesel, Luca Milanesio, Saša Zivkov, Edwin Kempin (CM, guest)

### Place/Date/Duration

Online, November 3, 11:00 - 12:30 CET

### Next meeting

The next meeting will be held on December 1, 11:00 CEST.

### Organizational

The meeting minutes for this meeting were under embargo until
the security issue that was discussed was fixed. The were made
public in December 2020.

## Minutes

### Security

Patrick discussed the plan to fix the security issue that makes
NoteDb content and tags accessible both in the Gerrit branch API
and in code browsers like Gitiles.

Edwin talked about the analysis of affected version that he
performed and suggested to fix 2.15-3.3.

Luca stated that many users are still on 2.14.

The consensus is to also try and fix 2.14.

The ESC discussed how the work can be split up. Google volunteered
to do the backports and Luca and Marco to do the releases.

The ESC had consensus that it will inform contributors and admins of
known larger installations shortly before the public announcement to
give them a chance to act before the issue becomes public.

With the public announcement, the ESC will also publish patched
binaries.

There is consesus that these meeting notes will be kept under an
embargo until we have published a fix for the issue.

### Testing at scale

Patrick started a discussion around testing at scale. Ben wanted to
know if Luca offers hosted solutions to clients. Luca said that most
clients require on-prem installations. Upgrading is a challenge.

Load testing at scale is something we desire but there was no concrete
AI for anyone to take here.
