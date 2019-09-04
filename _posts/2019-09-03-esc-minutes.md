---
title: "Gerrit ESC Meeting Minutes"
tags: news
keywords: news
permalink: 2019-09-03-esc-minutes.html
summary: "Minutes from the ESC meeting held on September 3rd"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, September 3, 2019

### Attendees

David Pursehouse, Patrick Hiesel, Luca Milanesio, Ben Rohlfs

### Place/Date/Duration

Online, September 3, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on September 17, 12:30 CEST.

## Minutes

* Gerrit News Page

  There were no suggestions for news items. The draft for the next issue already
  exists, and is scheduled for publishing on September 27th. Anyone can send
  suggested news items for review before then.

* Hackathon and User Summit in Gothenburg

  The recent hackathon and summit were a great success. During the hackathon
  many bugs were fixed, and 3 new releases have since been made.

  The talks at the summit were all recorded and will be published once they
  have been vetted by Volvo's legal team.

  Patrick's remote presentation about Gerrit performance was well received,
  and he will present it in-person at the next summit in November.

  Luca will prepare a more detailed article to be published on the project
  news page soon.

* REST API for retrieving Git trees

  The authors of the rejected design are planning to attend the upcoming user
  summit in Sunnyvale so there may be some opportunity to revisit the proposal
  and come to a compromise.

* Gerrit versioning and criteria for accepting fixes

  Luca's [updates to the versioning rules](https://gerrit-review.googlesource.com/c/gerrit/+/234560)
  were reviewed, accepted, and submitted.

* Design document for reverting multiple changes

  The design for [reverting multiple changes](https://gerrit-review.googlesource.com/c/homepage/+/233996)
  was reviewed and approved.

* Plans for 3.1 release and EOL of 2.15

  David suggested that we should start thinking about the release schedule
  for Gerrit 3.1 and therefore also bringing 2.15 to EOL.

  Everyone agreed that the upcoming hackathon in November would be a good
  time to release 3.1. This date also aligns with the planned schedule for
  completing the migration to Polymer2.

  We will cut the stable-3.1 branch some weeks before (mid October; exact date
  TBC) so that we have time to make release candidates and stabilise it.

  We need to make sure the release notes get updated in a more timely manner than
  3.0 so that we don't have to do them at the last minute again.

  The planned EOL for 2.15 should be announced early so that nobody is caught
  by surprise. We will make a separate news announcement, and update the
  homepage with more explicit details of support levels for recent releases.

* Proposal for making more frequent patch releases

  Luca proposed to make more frequent patch releases (for example every two
  weeks) to avoid that we have to make large release note updates and that
  the releases include too many fixes (i.e. from 3.0.1 to 3.0.2).

  David and Patrick disagreed. Making releases is time consuming and it
  doesn't always make sense to release on a fixed schedule, for example if
  there are only a couple of changes. It's better to wait and make a release
  only when there are a reasonable number of fixes. Release note updates
  are not really a problem; 3.0.2 was a rather large release but most of the
  release notes could be copied from 2.15.x and 2.16.x.

  End-to-end testing can be automated to reduce the time spent in making a
  release (see the next section). Also, Edwin is working on a way to
  automate creation of the release notes.

* Improved end-to-end testing

  Most of the release process is now automated, but there is no end-to-end
  testing. Work on this is in progress at GerritForge - see the
  [example change posted for review](https://gerrit-review.googlesource.com/c/gerrit/+/225212).

  We will follow up on this in the next meeting.

* Polymer 2 and customization/themes

  Ben talked about the current status of Polymer 2 migration in terms of
  what level of support should be expected for customization.

  In Polymer 2 the shadow DOM makes it more difficult than before for
  plugins to override styles and behaviors, so we need to decide which
  parts we want to allow to be customizable, for example the header.

  The frontent team would prefer to limit the amount of customization, but
  are aware that there are users that might want more. For example Wikimedia
  has some very specific styling, and GerritForge has customizations on the
  search box.

  In some cases the frontend team might be willing to make global changes
  based on customer customizations (for example the GerritForge search box)
  but would need to run them by the UX team.

  Consensus among ESC members is that we should apply good judgement on what
  should be customizable but don't necessarily need to support every use
  case.

* Migration of CI to Zuul

  Monty Taylor (Redhat) has offered to help with the adoption of [Zuul](https://zuul-ci.org/)
  for Gerrit's CI. They are also keen to help with support for the checks
  plugin in Zuul.

  Everyone agrees that this would be a good move.

  Migration of our existing CI jobs should not be too difficult since we
  already define them in a yaml format similar to the one that Zuul expects.

  There is no timeline yet. Luca will follow up.

* JGit updates

  We had planned to include JGit upgrades in 2.16.11 and 3.0.2 but at the
  last minute a regression was found and the updates were reverted.

  The root cause of the regression was [found and fixed by Han-Wen Nienhuys](https://git.eclipse.org/r/#/c/148706/)
  earlier this week. Matthias Sohn is making new JGit releases, and we will
  include the upgrades for the next 2.16 and 3.0 patch releases.

  Patrick reminded that we were planning to change Gerrit to build JGit
  from source, and asked what the status is. This is still planned, but
  has stalled during the ongoing work to stablize JGit.
