---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2022-05-11-esc-minutes.html
summary: "Minutes from the ESC meeting held on May 11, 2022"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, May 11, 2022

Christophe Poucet, Han-Wen Nienhuys, Luca Milanesio, Patrick Hiesel, Saša Živkov

### Next meeting

June 1, 2022

## Status of Gerrit v3.6.0 release plan

RC4 is out and is working as expected; GerritHub.io has already rolled out 50% of
its sites to v3.6.0 and raised the [Issue 15909](https://bugs.chromium.org/p/gerrit/issues/detail?id=15909)
caused by a NoteDb format change unnoticed because not advertised by a schema
version upgrade.

In the old days of ReviewDb, schema version was indicating broken compatibility
between releases. In NoteDb the schema version is associated with the schema
of the JSON data. The P1 was not spotted because was not highlighted in the
Release-Notes footer and threfore not included in the release notes.

We could do further tests in the future to make sure of not breaking it again
by having Gatling tests with two nodes with two different releases
(e.g. v3.5 and v3.6).

The issue is now fixed in v3.5 with the [Change 336833](https://gerrit-review.googlesource.com/c/gerrit/+/336883)
which makes Gerrit v3.5 tolerant with the new label format in v3.6.

Status of [Change 326953](https://gerrit-review.googlesource.com/c/gerrit/+/326953)
needed for releasing v3.6:
- Not finalised yet, because Gal left Google months ago and nobody took over yet.
- Patrick volunteer to take ownership of the problem and propose an alternative solution.

> *UPDATE*: The v3.6.0 release has been postponed by 1 week to allow enough time to
> review and test [Change 326953](https://gerrit-review.googlesource.com/c/gerrit/+/326953)
> properly. David and Luca are willing to help developing and testing the solution E2E.

## Roadmap updates

### Gerrit v3.5/v3.6 and user data

Han-Wen highlighted that user data (e-mail and name) is no longer persisted in
NoteDb change metadata and a new tool has been developed for
[redacting historical data](https://gerrit.googlesource.com/gerrit/+/08b89f6666f4a0fe1c026629e12a5430b6950932/java/com/google/gerrit/server/notedb/CommitRewriter.java#112)
but not wired in any schema migration.

### Streaming API for Gerrit searches

Luca mentioned that there was no space to push this through v3.6: the feature is
delayed to v3.7, with possibly other maintainers willing to help.

Patrick mentioned that the feature is worthwhile, but not simple to implement:
streams can only be consumed once, so need to ensure that they are.
