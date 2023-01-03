---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2022-12-14-esc-minutes.html
summary: "Minutes from the ESC meeting held on Dec 14, 2022"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Dec 14, 2022

Christophe Pouchet, Luca Milanesio, Saša Živkov, Patrick Hiesel

### Next meeting

Dec 14, 2022

### Import of projects

Luca gave an overview of the [draft design document](https://gerrit-review.googlesource.com/c/homepage/+/354234)
published regarding the process of moving from change-number to project/change-number
as unique global identifier of a change.

Patrick gave an initial positive feedback on the overall approach, with some
points to be clarified and addressed:

- Need for a solid migration path that allows gradual rollouts, so that
  it would be possible to first migrate to Gerrit v3.8 and then enable a smooth
  migration of projects to the new numbering scheme.

- The `refs/sequences/changes` on `All-Projects` will continue to exist as
  a fallback for projects that do not adopt the new numbering.

Luca pointed out that the APIs would still need to receive the project
as part of the change identifier; it may the be discarded if the new
scheme is not enabled and it will fallback to the current behaviour.

Saša highlighted that a useful implication of this move would be making
the move of projects across Gerrit primaries a lot easier, because of
the ability of having project-specific numbering.

### Overview of the Gerrit User Summit 2022 survey

Luca presented an initial overview of the survery results about the
Gerrit User Summit 2022 in November: 100% of the people responding
to the questions agreed that their objective was achieved.

More detailed results will be published on January 2023.
