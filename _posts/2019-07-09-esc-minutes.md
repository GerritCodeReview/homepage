---
title: "Gerrit ESC Meeting Minutes"
tags: news
keywords: news
permalink: 2019-07-09-esc-minutes.html
summary: "Minutes from the ESC meeting held on July 9th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, July 9 2019

### Attendees

Luca Milanesio, David Pursehouse, Alice Kober-Sotzek, Ben Rohlfs, Patrick Hiesel

### Place/Date/Duration

Online, July 9, 12:30 - 13:15 CEST

### Next meeting

The next meeting will be held on July 23, 12:30 CEST.

## Minutes

* Gerrit News Page

  The next edition of the project news was postponed until the end of July,
  and will contain news about what has happened in June and July.

  Instead of brainstorming ideas for the news during the meeting, it was
  decided to consider it offline and upload suggestions to the existing draft
  post on the homepage project.

* Upcoming Gerrit User Summits in Gothenburg and Sunnyvale

  The "Prolog-less submit rules" talk was already given during the last
  summit in the USA. It can be dropped from the schedule for Sunnyvale
  and only be presented in Gothenburg for the benefit of European attendees.

* REST API for retrieving Git trees

  A design document for
  "[Add a new REST API to retrieve trees](https://gerrit-review.googlesource.com/c/gerrit/+/228127)"
  is still pending, so a full discussion is postponed until the next
  meeting.

* Soy migration documentation

  The soy project includes Google-specific links that are not publicly
  accessible. See [issue 177](https://github.com/google/closure-templates/issues/177).

  Patrick will follow up internally at Google to discuss how this can be
  improved.

* Redesign of external IDs

  Patrick's [proposed redesign of external IDs](https://gerrit-review.googlesource.com/c/homepage/+/228398)
  has received mostly positive feedback, with some valid points raised by
  Martin about atomic ref updates.

  Luca proposed to hold a lightning talk at the Gotherburg summit to
  present the new design. Patrick agreed to do that; although he is not
  attending the summit he will join remotely.

  The design doc will cook for a few more days to see how points can be
  addressed and to add more details where needed.

* Owner/maintainer of the replication plugin

  Luca raised the question of who is the main stakeholder/owner/maintainer
  of the replication plugin, since there are several open changes that are
  pending review.

  David proposed that the main stakeholders are SAP (Saša), Ericsson (Marco),
  CollabNet (David) and GerritForge (Luca), while Google isn't using it.

* Joint meeting with community managers

  Edwin suggested that we have a joint meeting between ESC and the community
  managers.

  We agreed that this is a good idea, but it may be difficult to find a time
  slot that works for everyone due to the different time zones. On the other
  hand, it is perhaps not necessary for all members to attend.

* Polymer 2 and themes

  Luca asked about how theming with Polymer 2 will work. Ben explained that
  arbitrary css styling as currently possible will not be possible any more
  with Shadow DOM. However it should be noted that the current 'support' was
  never official; the recommended and documented approach is still to override
  css properties from plugins that use `registerStyleModule()`. We are open
  to adding more css properties and will have to see how much of an issue this
  becomes.

* Quota backend changes

  The changes started by Jacek during the last hackathon are still pending.
  Patrick had previously reviewed them and left some comments, which have
  since been addressed, but the new patch sets were uploaded during Patrick's
  vacation. Patrick will review them again soon.

* New Gitiles releases

  Per the discussion in the previous meeting, a stable branch has been
  created on gitiles and new releases have been made which include the
  fix for the recent regression. The version numbering scheme was not
  changed; this can be done later if really needed.
