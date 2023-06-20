---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-06-01-esc-minutes.html
summary: "Minutes from the ESC meeting held on June 1, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---



## Engineering Steering Committee Meeting, June 1, 2021

### Attendees

Han-Wen Nienhuys, Luca Milanesio, Patrick Hiesel, Saša Živkov

### Place/Date/Duration

Online, June 1, 11:00 - 12:00 CET

### Next meeting

Jul 6, 2021 - 11:00 - 12:00 CET

## Minutes

### Moving to use `main` branch name for the Gerrit repository

`master` is a term that we do not use anymore in the Gerrit project, but we
still use it as the name of the main development branch. A consensus is that we
should start developing against a new `main` branch in Gerrit. The old `master`
branch is going to be removed.

The creation of new projects with an initial commit should be amended to use
`main` instead of `master`.

### Support for Gerrit v2.16

Gerrit v2.16 is still currently supported to allow users to migrate
to any v3.x version: all schemas migrations from any v2.x release, including the
conversion to NoteDb, require to go through that version.

The Community is still spending a considerable effort to keep the change
validation active for the stable-2.16 branch. However, that is not sustainable
in the longer term because of the burden of supporting deprecated and obsolete
machinery.

The ESC consensus is that the special [EOL status of Gerrit v2.16](2020-04-22-gerrit-3.2-release-plan.html#end-of-life-for-gerrit-216x.html)
will end when v3.5 is released. Existing v2.x users can continue to use the published
artifacts and the associated plugins on the [GerritForge's archive](https://archive-ci.gerritforge.com).

The move is going to be largely publicised on the mailing list so that all
Gerrit users can have plenty of advance notification and take action before the
move.

Existing users having issues with the migration to Gerrit v2.16 could request
bug fixes and ad-hoc releases through any vendor that provides
[Enterprise Support](https://www.gerritcodereview.com/support.html#enterprise-support).

### Accidental breakage of the conflicts UI in v3.4

During the release of Gerrit v3.4.0, the functionality of displaying of
[conflicting changes was accidentally broken](https://issues.gerritcodereview.com/issues/40013800).
The problem went unnoticed because there are not specific test validating the
feature, and it is not used anymore in any of Google's `*-review.googlesource.com`
sites.

The breakage happened on Gerrit master and was later cherry-picked onto the
stable-3.4, self-approved, before the RC3, aligned with the
[Gerrit v3.4 release plan policies](https://www.gerritcodereview.com/2021-03-16-gerrit-3.4-release-plan.html).

The consensus is that self-approval of changes should be disabled on Gerrit and
features that are not largely adopted or properly tested should be deprecated
and later removed.

### Review of open designs

The review of the [Gerrit events compatibility](https://gerrit-review.googlesource.com/c/homepage/+/302082)
design document is mostly stalled, with some comments still unanswered and the
focus unclear.

Han-Wen took the action of documenting the Gooogle's Gerrit events system and
publish to the Gerrit Community so that it can be used as __blueprint__ for
future work in the open-source code-base.
