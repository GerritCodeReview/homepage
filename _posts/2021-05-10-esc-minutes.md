---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-05-10-esc-minutes.html
summary: "Minutes from the ESC meeting held on May 10, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, May 10, 2021

### Attendees

Ben Rohlfs, Han-Wen Nienhuys, Luca Milanesio, Patrick Hiesel, Saša Živkov, Albert Cui (observer)

### Place/Date/Duration

Online, May 10, 17:00 - 18:00 CET

### Next meeting

Jun 1, 2021 - 11:00 - 12:00 CET

## Minutes

### Switching ESC Seats

Google will switch out Ben for Albert in the ESC. Thanks Ben for all your contributions!

Albert is the product manager for Google's Gerrit team.

### Standalone JS Builds

Gerrit will [remove HTML plugins](https://gerrit-review.googlesource.com/c/gerrit/+/299364) as part of the 3.4 release. In doing so, standalone build support for frontend plugins was removed. This created issues for community members who depended on this behavior.

The ESC discussed that David Ostrovsky provided [a fix](https://gerrit-review.googlesource.com/c/bazlets/+/304117) to bring back standalone build support, however there has never been a clear stance as to whether this functionality is formally supported by the Gerrit project.

The ESC discussed that this functionality is used by very few people; SAP, Gerrit Forge, Google, for example, all do in-tree builds.

The ESC reached consensus that for future releases, standalone build support would be a best effort, community supported feature and not a blocker for releases.

### Commenting / Selection issue in Safari Web Browser

We've seen a growing number of complaints about a commenting / selection issue when using the newest version of Safari, the default in the latest macOS Big Sur release.

Folks from GerritForge are actively looking to address the issue.

### Adding events-broker and global-refdb as submodules in the Gerrit tree

Luca proposed adding GerritForge’s [events-broker](https://gerrit-review.googlesource.com/q/project:modules/events-broker) and [global-refdb](https://github.com/GerritForge/global-refdb) to the Gerrit tree as third party libraries (similar to JGit) to make plugin dependencies easier to manage. Patrick will look into this and provide feedback at the next ESC meeting.

### Open Designs

Marcin has proposed a new design for
[Events Compatibility](https://gerrit-review.googlesource.com/c/homepage/+/302082). Han-Wen has discussed this with Marcin but has not had a chance to look into the updated design.

### Roadmap Update

Skipped

### Monorail Issues assigned to ESC component

We have looked into all open issues and assigned owners to all of them.

