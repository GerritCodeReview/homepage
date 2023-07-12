---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2023-07-12-esc-minutes.html
summary: "Minutes from the ESC meeting held on July 12, 2023"
hide_sidebar: true
hide_navtoggle: true
toc: true
--

## Engineering Steering Committee Meeting, Apr 12 - May 3 2023

Christophe Poucet, Patrick Hiesel, Luca Milanesio, Saša Živkov

### Next meeting

September 6, 2023

### Java 11 is EOL, move to Java 21

We can move to Java 21 but the language must remain Java 11 until Java 21 is GA inside Google.
Java 21 is an LTS.

### Next Gerrit user summit

To be held at Volvo Cars (Sweden) + Sunnyvale. There is also a possibility of presenting remotely.
Date: September 30 until October 1st, 2023
An on-site hackathon could be held a week before.

### Introduce a "Gatling Test Required" trigger label

Gatling tests may be required on individual change when it changes  critical backend components.
As an example Luca mentioned the
[change 345634](https://gerrit-review.googlesource.com/c/gerrit/+/345634)
which caused inconsistencies in change query results. Gatling tests couldn't be run for every
change because they are expensive.  The decision to run gatling tests for particular change would be
made by a maintainer reviewing that change. Gatling tests would run on gerrit-ci.

### Proposal to switch index.paginationType default to NONE

A final decision couldn't be reached during this ESC meeting.


### Delete group feature in Gerrit core

ESC agrees with the
[change 376294](https://gerrit-review.googlesource.com/c/gerrit/+/376294).
There should also be a feature switch in gerrit.config to enable/disable this feature. The ability
to delete groups would also be allowed to the group owners.
