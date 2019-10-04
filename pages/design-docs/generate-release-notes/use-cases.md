---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use-case

* As an admin I expect release notes that are well-written and
  complete, so that I can safely plan/execute Gerrit upgrades.
* As a release manager I don't want to spend a lot of time and effort
  on manually writing release notes, but the release notes should be
  generated.

## Secondary use-cases

* As a contributor pushing changes should be easy. If a release
  notes entry is required for my change it should be easy to attach.
* As Gerrit community we want to review release notes to ensure high
  quality.
* As reviewer I want to review the release notes entry together with
  the change in Gerrit, so that I have all context in one place.
* As Gerrit community we want to ensure that all relevant changes are
  reflected in the release notes. Hence changes without release notes
  entry should be an exception.
* As Gerrit project we want the creation of new releases be quick and
  easy so that we can do releases any time on short notice. Hence
  generating release notes should be possible any time.
* As admin I expect that release notes are consistenly structured
  across releases (e.g. release notes should always have the same
  sections).

## <a id="acceptance-criteria"> Acceptance Criteria

* When a new release is created, the release notes are either already
  ready or can be generated automatically.
* All relevant changes have a release notes entry attached:
  * The release notes entry is part of the Gerrit change and can be
    reviewed in Gerrit.
  * Changes without release notes entry can be detected and be blocked
    from submit.
  * Trivial changes without release notes entry are possible.
  * Having multiple changes that share one release notes entry are
    possible.
* If a release notes entry for a change is missing it's
  self-explanatory and easy for the contributor to attach it.
* When another branch is merged into a branch, the release notes
  entries of the integrated changes are automatically included into
  the release notes of the target branch.
* When a change is cherry-picked its release notes entry is
  automatically included into the release notes of the target branch.
* Submitting changes with release notes entries should not require
  conflict resolutions in the release notes.
* Amending release notes entries after they have been submitted must be
  possible.
* Amending release notes after a release was created must be possible.
* The (generated) release notes must be well-structured. E.g. it has
  pre-defined sections that are automatically populated with release
  note entries.
* For writing release notes entries it is possible to use basic
  formatting (e.g. lists, subsections, links etc.).

## <a id="background"> Background

Creating Gerrit releases is a pain because release notes must be
written manually which takes a lot of time and effort. Writing the
release notes after the fact has a high risk of missing things that
should have been mentioned. Also the release manager may not know the
details of every change and hence may not be able to summarize each
and every change properly. Reviewing release notes is difficult
because there are no links to the changes that did the implementation.

During the community retrospective it was brought up that the quality
of our releases notes should be improved (e.g. it was criticized that
the release notes sometimes omit important changes).


