---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2025-07-31-esc-minutes.html
summary: "Minutes from the ESC meeting held on July 31, 2025"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

# Engineering Steering Committee Meetings, July 31, 2025

**Participants**: Edwin Kempin [EK], Luca Milanesio [LM], Saša Živkov [SZ]

**Next meeting**: September 24, 2025

## Executive Summary

A critical Gerrit migration to Bazel 8 is needed to fix compatibility issues
with JGit. Gerritforge offered to lead the effort with Google providing
reviews. The immediate next step is to add more details to the associated
[issue 339767728](https://issues.gerritcodereview.com/issues/339767728).

Two key community events were announced: a Git Mini Summit in Amsterdam on
August 28th and a GerritMeet at Google's Munich HQ on November 19th. The Munich
event is notable as Google will unveil a new open-source MCP server, which
generated significant interest.

The future of AI-powered code review was discussed, centered on the experimental
"help me review" feature. Google confirmed ongoing internal development and
welcomed collaboration to prevent duplicated work. A native chat functionality
was also proposed to streamline AI integration in the future.

## Migration to Bazel 8 and bzlmod

[LM] raised the issue of migrating Gerrit to Bazel mode, noting that JGit had
already migrated to Bazel 8 and bzlmod, causing compatibility issues with Gerrit,
which is still on Bazel 7.6.6 and relies on WORKSPACE support. [EK] confirmed
that the migration effort is not yet on Google’s Gerrit Team backlog, as they
rely on Blaze, which still supports WORKSPACE for the foreseeable future.
[LM] suggested that Gerritforge Inc. could allocate the task for the effort
through the compatibility approach (see https://bazel.build/external/migration),
assuming that Google is available for reviews, because any modification to the
dependencies requires an LC+1 from a Google maintainer.
[SZ] suggested that Matthias Sohn would be a suitable person to help with this,
and [EK] agreed that a summary should be added to the
[issue 339767728](https://issues.gerritcodereview.com/issues/339767728) detailing
the work, pluses, minuses, and required involvement from Gerrit maintainers would
be helpful to start the discussion and planning of the activity.

## Git Mini Summit Event in Europe

[LM] announced that Gerritforge, GitLab, GitButler and Google are sponsoring a new
Git event in Europe, scheduled for
[August 28th in Amsterdam](https://events.linuxfoundation.org/open-source-summit-europe/features/co-located-events/#git-mini-summit-2025). [LM] explained that this "Git mini summit" was organized as a community-driven complement of
Git Merge in the US for all of those who have travel restrictions or concerns
to the USA. Their team plans to present their work on JGit optimization and
performance improvement with Gerrit, GitLab, and GitHub Enterprise, thanks to
the R&D work done by Gerritforge in 2024 and 2025 as part of the
[GHS product](https://gerritforge.com/ghs.html). [EK] mentioned that the Gerrit
team is unlikely to participate in this community event; however, other Google
members working on the Git Team will join.

## GerritMeets in Munich

[LM] announced that Florian from Google Cloud and Daniele from Gerritforge had
agreed to organize a GerritMeet event at the Google EU HQ in Munich, with the
date already set to November 19th, 2025. [LM] also mentioned that Google would
be presenting a brand-new MCP server for Gerrit Code Review as a new Open-Source
project on the Gerrit ecosystem. [EK] and [SZ] expressed interest in attending,
especially since it is in Germany and relevant to their activities.

## AI Code Review Feature in Gerrit

[SZ] inquired about the future of Gerrit's experimental "help me review" AI button,
which their users have been exposing internally. [EK] confirmed that there are many
internal discussions about this feature and suggested reaching out to Milutin, who
is driving Google's AI efforts around Gerrit, who has started implementing the
frontend UI based on a fake backend. [EK] welcomed help from [SZ] with this effort,
which would prevent duplicated work. [LM] noted that while the current AI suggestions
are about 20-30% useful, integrating a native chat functionality within Gerrit could
make existing AI code review plugins (chatgpt-code-review and ai-code-review) less
relevant in the future, and they are happy to support Google's AI endeavor once
it's fully open-sourced.
