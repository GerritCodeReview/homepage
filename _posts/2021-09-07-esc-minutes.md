---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-09-07-esc-minutes.html
summary: "Minutes from the ESC meeting held on Sep 7, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---



## Engineering Steering Committee Meeting, Sep 7, 2021

### Attendees

Han-Wen Nienhuys, Luca Milanesio, Saša Živkov

### Place/Date/Duration

Online, Sep 9, 11:15 - 12:00 CET

### Next meeting

TBD

## Minutes

### Action items

Google has published [quarterly objectives](google-okrs.html) for Q3.

### Virtual summit Dec 2-3

Recent events were contributor/developer summits, so there were no
user summits for 2 years. GerritForge would like to organize a
user-event. As the pandemic isn't under control yet, a face-to-face
event is unlikely.

A user-event attracts more participants, so will need infrastructure
beyond Google meet. GerritForge can hire an external company.

GerritForge considered a f2f hackathon in London in December, but it
looks impossible. (Both Google and SAP have WFH policies. We cannot
and don't want to send people to a f2f event.)

This means we should do the release of Gerrit 3.5 in November.

### Case sensitive usernames

Our survey is closing tomorrow, but we have 5 responses from companies
who have users just distinguished by case. So we cannot remove the
support completely, and must go ahead with the current solution (make
it configurable). This will be submitted to `master` shortly. The new
default is case-insensitive.

### Java 11

Google has moved to Java 11 as of Aug 31. Gerrit can move to Java 11
for current `master`. Stable releases remain on Java 8. We merge
forward from stable, so the difference in language level should cause
no problems.

### Moving drafts out of the change index

Han-Wen: Google is [moving has:draft out of the change
index](https://gerrit-review.googlesource.com/c/gerrit/+/317099). The
new solution does a prefix ref scan. Google would love to see
real-life data if this prohibitively expensive for upstream deployments;
we could change the draft storage in response (`refs/users/USERID/drafts/CHANGEID` iso.
`refs/drafts/CHANGEID/USERID`).

Luca: we support reducing the amount of indexing. `All-Users` gets a
lot of traffic and Jacek Centkowski is looking into it; he can provide
timings.

If it is expensive, could we change the storage in a dual-read mode
(read old+new storage format, write new format) to provide a seamless
upgrade path for 3.4 to 3.5.

### Classical replication and bitmaps

Saša: SAP will post findings for the classical replication plugin. We
have a scenario where disabling bitmaps decreases replication times
(for push replication).

Han-Wen: that's odd. Try JGit bitmaps iso. CGit bitmaps maybe? We
tweaked bitmap generation for our deployment. Will forward to the JGit
team at Google.

