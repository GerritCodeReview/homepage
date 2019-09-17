---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-08-20-esc-minutes.html
summary: "Minutes from the ESC meeting held on August 20th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, August 20, 2019

### Attendees

David Pursehouse, Alice Kober-Sotzek, Patrick Hiesel, Luca Milanesio

### Place/Date/Duration

Online, August 20, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on September 3, 12:30 CEST.

## Minutes

* Gerrit News Page

  There were no suggestions for new items. The hackathon in Gothenburg is coming
  up next week and there are likely to be some interesting things to write about,
  however the consensus was that it will be better to make a separate post about
  the hackathon rather than waiting until the next project news at the end of
  next month.

* REST API for retrieving Git trees

  We discussed whether or not the rejected design document should be restructured
  to follow the new structure proposed by Edwin. We don't want to ask the author to
  spend time doing that, and nobody else really has time to do it either.

  For now we will leave it as it is, and for future design documents we will
  ensure that the new structure is used. Alice will look into how we can still
  submit that rejected document.

* Follow up on Dave Borowitz's open changes

  Dave has left the project but there are several of his changes still open. We
  will look over those to see which of them are still needed, and then work on
  getting them submitted.

* Removal of obsolete user preferences

  Patrick discussed this with Edwin and they concluded that it's not necessary
  to implement migrations to remove the obsolete values from users' settings.

  David will rework the changes to remove the migration code.

* Status of the replication plugin

  There have been a lot of complaints about the replication plugin being unstable
  in 2.16. Luca attempted to fix one of the more serious issues, but abandoned it
  due to not being comfortable introducing heavy refactoring on the stable branch.

  GerritHub is currently using a forked version of the plugin that has the fix.

  David pointed out that since the fix in question is fixing a serious bug, it
  should be OK to submit it on the stable branch.

  Luca is concerned that the plugin has very low test coverage and wants to
  ensure that the coverage is increased before making further fixes.

* Gerrit versioning and criteria for accepting fixes

  Following the discussion about the replication plugin fixes, we also discussed
  more generally what the criteria should be for accepting fixes on stable branches
  (both in core and in plugins), and Luca suggested that could adopt a more
  well-defined policy like JGit has.

  David pointed out that JGit's policy is stricter because it is constrained
  by OSGI's restrictions on API changes, and this is not applicable to Gerrit. Luca
  clarified that the idea is only to make the guidelines clearer.

  The Gerrit contribution guidelines do mention what is allowed on stable branches,
  but it's intentionally not very specific so that the maintainers have flexibility.

  Luca will propose some updates to the contribution documentation to make the
  guidelines more concrete. We will review this in a future ESC meeting.

  We also discussed where these guidelines should be published. Currently most of
  the documentation is in the core Gerrit project, with the most recent version
  being on the master branch. This is not very discoverable, so we decided that it
  will be better to move it to the project homepage with a link from core.

* Upcoming hackathon and summit in Gothenburg

  Alice had proposed to focus on bug fixes during this hackathon. This was scheduled
  for Saturday, but Alice won't be joining on that day. Luca suggested to join
  remotely if possible.

  Patrick will propose a talk on recent performance improvement initiatives.

  Luca mentioned that there are many more users registered for this summit than
  the previous European summit in London.

* Design document for reverting multiple changes

  Patrick requested that we have a look at the [design document](https://gerrit-review.googlesource.com/c/homepage/+/233996)
  that has been up for review since last week. Some of us had already looked at it
  briefly.

  Patrick will follow up with ESC members in 3 days.
