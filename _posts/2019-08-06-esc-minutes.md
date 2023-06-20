---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-08-06-esc-minutes.html
summary: "Minutes from the ESC meeting held on August 6th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, August 6, 2019

### Attendees

David Pursehouse, Alice Kober-Sotzek, Patrick Hiesel, Ben Rohlfs

### Place/Date/Duration

Online, August 6, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on August 20, 12:30 CEST.

## Minutes

### Gerrit News Page

  The project news for June and July was
  [published](https://www.gerritcodereview.com/2019-07-26-gerrit-news-jun-jul-2019.html).

  Although there was not a lot of content, we decided that it's worth continuing to
  publish such news on a bi-monthly schedule. Therefore the next edition is scheduled
  for the end of September and will cover things that have happened in August and September.

  We had a brief discussion about what kind of things should be included, i.e. whether
  it should only be news about core development. The conclusion was that anything related
  to the project can be included, if it is of interest.

  We also discussed whether it would be interesting to include sections about new
  developers who have joined the project, for example Google recently onboarded a few new
  [frontend developers](https://groups.google.com/d/msg/repo-discuss/CnWrhhdttFk/SDcuaRBQCwAJ)
  and maybe it would be nice to include that kind of information. We will look into doing
  this if it's possible to do it in a way that's not too Google-centric.

### Mentoring for the pluggable Auth Backend feature

  Google has tentatively confirmed that they will provide one developer to act as
  'mentor' for this feature for one quarter, probably Q4 of this year. We will follow
  up on this in the next meeting.

### REST API for retrieving Git trees

  We had a rather long discussion about the
  [design](https://gerrit-review.googlesource.com/c/homepage/+/231894) and decided to
  reject it. Alice will post a detailed response on that change.

### Redesign of external IDs

  Patrick's [alternative solution](https://gerrit-review.googlesource.com/c/gerrit/+/231934)
  was submitted. We will come back to this in the next meeting after data has been
  gathered.

### Recommendation on where to store global configurations

  ESC was requested to provide guidance about whether global configurations should
  go in `gerrit.config` or `All-Projects`.

  This is now being tracked in
  [issue 40011036](https://issues.gerritcodereview.com/issues/40011036).

### Development workflow for frontend fixes

  The typical workflow for bug fixes on the backend is to submit the change to the
  earliest appropriate stable branch and then merge up through other stable branches
  to master. Frontend fixes, however, are generally submitted to master and then
  cherry-picked back to the stable branch.

  We discussed whether or not we should change this to align the workflow for backend
  and frontend fixes. There were several points raised:

  - It's not always obvious for a developer whether or not a fix needs to go to a
    stable branch. It's often easier to just send it to master. This is the case for
    both backend and frontend changes.

  - If a fix gets submitted on a stable branch first, it takes some time before it
    reaches master through merges. This particularly affects Google because they
    run Gerrit at master.

  - Release managers usually watch out for fixes that are sent to master, and
    either change the destination branch before they are submitted, or cherry-pick
    them after, and then take care of the merges up through to master.

  - Release managers sometimes have difficulty cherry-picking or resolving merge
    conflicts for frontend changes because they are not as familiar with frontend
    code as they are with backend.

  We concluded that we will not enforce any change in workflow, keeping the current
  status quo. The maintainers who are more familiar with frontend code agreed to
  provide support in cherry-picking and merging frontend fixes.

### Removal of obsolete user preferences

  When GWT was replaced with PolyGerrit there were some features that got dropped,
  and the related settings are no longer presented in the UI. However, support for
  those settings still exists in the backend.

  Changes were proposed to remove them (see topic
  '[remove-gwt-prefs](https://gerrit-review.googlesource.com/q/topic:remove-gwt-prefs)'
  and change [230365](https://gerrit-review.googlesource.com/c/gerrit/+/230365)) but
  the reviews have stalled after migrations were implemented to remove the unused
  settings from user preferences.

  Patrick will follow up on those reviews and look into whether we really need to
  remove the user preferences, or if it's OK to just remove the code.
