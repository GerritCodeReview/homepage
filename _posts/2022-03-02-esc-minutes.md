---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2022-03-02-esc-minutes.html
summary: "Minutes from the ESC meeting held on Mar 2, 2022"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Mar 2, 2022

Christophe Poucet, Han-Wen Nienhuys, Luca Milanesio, Patrick Hiesel, Saša Živkov.

### Next meeting

April 6, 2022

## Review of the current Gerrit roadmap

As Gerrit v3.6 release plan has been announced, the roadmap can be
adjusted to reflect what is likely to be included:

- Prolog-less submit requirements
- Push notifications (tentative)
- Bulk actions (tentative)
- Cleanup of Change-Ids inconsistencies
- Performance improvements for large changes

The following features are WIP but unlikely to be completed by v3.6:

- Streaming Java API for retrieving query results
- Workflow for reviewing/approving non-fast-forward pushes

## [Issue 15707](https://bugs.chromium.org/p/gerrit/issues/detail?id=15707): Adopt Supply Chain Security best practices from SLSA

More clarification on the issue would be required from Nasser. At high-level
it does not seem like a Gerrit project issue. Gerrit can also be compiled
from source directly if the trust on Maven artifacts is an issue.

It remains also an open question to identify Which SLSA level do we want
the Gerrit Code Review project to be.

## Further ESC issues

Follow-up discussion about potential DoS problem; cannot currently be disclosed.
