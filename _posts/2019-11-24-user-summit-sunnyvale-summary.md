---
title: Summary of the Gerrit User Summit 2019 in Sunnyvale
tags: news summit hackathon
keywords: news summit hackathon
permalink: 2019-11-24-user-summit-sunnyvale-summary.html
summary: "Summary of the Gerrit User Summit 2019 in Sunnyvale"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## High-performance Summit in numbers

The Gerrit User Summit 2019 has ended, with highest score of achievements
in the history of the 11 years of the entire Gerrit open-source project:

1. Two dates and locations in a 12-months period: Gothenburg (Sweden) and
   Sunnyvale (California).

2. Four Gerrit releases delivered: v2.15.16, v2.16.11, v3.0.2, v3.1.0

3. 127 people registered across the two locations,
   87 people attended on-site (70% turnout) and 38 people followed at
   different times the event remotely using the live streaming coverage
   provided by [GerritForge](https://gerritforge.com).

4. 373 changes merged (204 in Gothenburg, 169 in Sunnyvale).

5. 32 developers attended the Hackathons, 8 of them have never contributed or
   attended an event before.

6. The highest performing version of Gerrit v3.1.0 released, with over 2x
   git and REST-API performance compared to v3.0.x

7. 22 talks presented across Gothenburg and Sunnyvale, with 6 new speakers
   that have never presented before at the Summit.

The performance of the Summit is yet again another evidence of the continuous
growth of the community and the increased synergies with the JGit, OpenStack/Zuul
and the Tuleap open-source projects.

## Sunnyvale Hackathon summary

### Gerrit v3.1.0 preparation, load testing and release

During the Hackathon, David Pursehouse has been working on the release of
Gerrit v3.1.0, with the help and support of all the other developers at the
hackathon.

Following the experiences of the previous releases, this year the major focus
has been the stability, end-to-end and load testing of the release. Matthias Sohn (SAP),
Fabio Ponciroli (GerritForge) and Antonio Barone (GerritForge) worked in improving
the Gerrit E2E test suite to perform A/B testing of Gerrit v3.0 vs. v3.1.

GerritForge has upgraded early on the GerritHub.io multi-site setup, keeping one
data-centre (Canada) on v3.0 and upgrading the second data-centre (Germany) to v3.1.
GerritHub.io has thus been the target of the Gerrit v3.1 validation tests which has
been successfully completed and shown a 2x performance improvement ratio between the
two releases.

> NOTE: The E2E tests for Gerrit are based on [Gatling open-source framework](https://gatling.io/)
> with the [Git protocol support](https://github.com/gerritforge/gatling-git) implemented
> by GerritForge.

### Support for large repositories in Gerrit

TOOD

### Review and merge of the ref-table support in JGit and Gerrit

## Summit summary

The talks have been mainly centred on the new features introduced in Gerrit v3.1:

- The porting to PolyGerrit 2 and the new development team in Germany
- Performance improvements in v3.1
- Support for Git protocol v2

Some of the talks presented in Gothenburg have been replayed in Sunnyvale as well,
with the addition of brand-new talks about the new features and developments completed
in the past three months.

TODO

### What's new in Gerrit v3.1

TODO

### Road-map and migration path to Gerrit v3

TODO

### Gerrit Q&A with the maintainers

TODO

### What's cooking in JGit

TODO

### New developments and team structure in the PolyGerrit Team

TODO

### Status of the Gerrit Code-Review Analytics for the Android open-source project

TODO

### What's new in the Bazel tool-chain for Gerrit

TODO

### Racy JGit

TODO

### OSSUM with Gerrit

TODO

### Revert submission

TODO

### Gerrit metrics and dashboards

TODO

## Feedback and proposals of improvements for the next Summits

TODO

----

Thank you again to all the attendees of the Gerrit User Summit 2019 in Volvo - Sweden
and GerritForge Inc - California. Looking forward to another exciting year of innovation
and development of the Gerrit Code Review platform and community.

Luca Milanesio (Gerrit Maintainer, Release Manager, ESC member)
