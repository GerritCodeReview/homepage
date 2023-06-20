---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-04-07-esc-minutes.html
summary: "Minutes from the ESC meeting held on Apr 6, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Apr 6, 2021

### Attendees

Ben Rohlfs, Han-Wen Nienhuys, Luca Milanesio

### Place/Date/Duration

Online, Apr 6, 11:00 - 12:00 CET

### Next meeting

May 4, 2021 - 11:00 - 12:00 CET

## Minutes

### CSS Overrides

Wikimedia [raised the problem of CSS overrides](https://groups.google.com/g/repo-discuss/c/bokM7QOGULs)
in the Gerrit Frontend from Gerrit v3.1 onwards. We know that other Gerrit hosts have similar
problems.

Ben as the Frontend lead is aware of the problem and proposed the following:

- Gerrit's webcomponents are using the Shadow DOM and there is no way to change that. It is possible
  to reach into the Shadow DOM of components with JavaScript, but this is only an option for one-off
  workaround, not a general solution to the problem.
- We will look into [css ::part()](https://developer.mozilla.org/en-US/docs/Web/CSS/::part) for
  release 3.5 and beyond. That spec can potentially address the use case well.
- The Frontend team is fine with adding more css variables and plugin endpoints, if that helps
  hosts to enable the desired customizations. This can even be done for stable branches, if needed.
  But we are asking for a detailed explanation for what should be styled and why. At the moment we
  think that most of the requests will be addressed by features planned for 3.4 (Checks UI) and 3.5
  (Submit Requirements).
- The Frontend team is also committed to responding quickly to such issues on the repo-discuss@
  mailing list, especially when they are blocking upgrades from previous versions.

### Gerrit v3.4 release status

GerritForge will continue to improve the automatic E2E Gatling tests run daily on stable-3.4.
A temporary 8x slowdown was discussed, but that was a one-off and performance is back to normal.
Han-Wen has filed [issue 40013643](https://issues.gerritcodereview.com/issues/40013643) for
looking into Soy slowdown.

Luca proposed to issue a “weekly release bulletin” with list of commits included, builds
summary and Gatling tests highlights. The ESC appreciates such weekly updates.

### ElasticSearch support

It was decided to keep ElasticSearch support in 3.4, but remove it in 3.5.

### Click Tracking

The [issue 40013625](https://issues.gerritcodereview.com/issues/40013625) was briefly discussed.
Han-Wen and Ben explained how the 'clearcut' plugin works on Google hosted Gerrit instances. It
collects usage statistics and performance data in accordance with the Google Privacy Policy.

### Open Designs

Marcin has proposed a new design for
[Events Compatibility](https://gerrit-review.googlesource.com/c/homepage/+/302082). Han-Wen will
find someone at Google to review the change and moderate the design process.

Luca will reach out to Jacek about potentially closing the
[stale designs](https://gerrit-review.googlesource.com/c/homepage/+/246449) for an "Auth Extension
Point".

### Roadmap Update

Skipped

### Monorail Issues assigned to ESC component

We have looked into all open issues and closed some. The remaining 4 issues are
valid and will keep being monitored by the ESC.

