---
title: Summary of the Gerrit User Summit & Hackathon 2019 in Sunnyvale
tags: news summit hackathon
keywords: news summit hackathon
permalink: 2019-11-24-user-summit-sunnyvale-summary.html
summary: "Summary of the Gerrit User Summit & Hackathon 2019 in Sunnyvale"
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
   87 people attended on-site (70% turnout) and 38 people followed the event
   remotely at different times using the live streaming coverage
   provided by [GerritForge](https://gerritforge.com).

4. 373 changes merged (204 in Gothenburg, 169 in Sunnyvale).

5. 32 developers attended the Hackathons, 8 of them have never contributed or
   attended an event before.

6. The highest performing version of Gerrit v3.1.0 released, with over
   [2x git and REST-API performance compared to v3.0.x](https://gitenterprise.me/2019/12/20/stress-your-gerrit-with-gatling/).

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

Luca Milanesio (GerritForge), Matthias Sohn (SAP) and Martin Fick have been discussing
the issues associated with very large repositories:

1. JVM heap utilisation and associated GC cycles

   Luca contributed the information about the problems and investigations associated with
   large *stop-the-world* (STW) GC pauses observed when running Git operations on large
   repositories. The JVM heap would need to create a large in-memory packfile and thus
   would require the JVM to allocate a very large continuous area of memory. That operation
   could, in some cases, trigger a STW GC cycle that could make the Gerrit server unavailable
   for a few seconds.

2. Git in-memory cache of Packfiles and BLOBs

   Matthias has contributed its experience at SAP in dealing with large repositories. The JVM
   heap allocated is huge, up to 500 GBytes. A big part of the heap is dedicated to the in-memory
   packfile caching which would avoid the continuous allocation/release of large areas of memory.
   However, it looks like that even though the cache is still needed, the JVM at times releases
   part of it and may cause the continuous memory allocation/release that may cause STW GC cycles.

3. Quotas support for expensive operations

   Martin has proposed a change to the Gerrit quotas to block or delay incoming operations
   in the execution queue. It could allow to identify operations that could be potentially
   trigger a STW GC and reschedule them at a later time. Whilst this would not completely solve
   the problem it would allow the Gerrit instance to have a "breathing space" and recover
   heap before serving the exensive operations.

### Review and merge of the ref-table support in JGit and Gerrit

Han-Wen Nienhuys (Google) and Matthias Sohn (SAP) have worked in the final review and submission
of the JGit implementation of ref-table, which was initially designed by Shawn Perce but never applied
to the OpenSource code-base. Han-Wen has redesigned the feature for making it compatible with the
filesystem-based implementation of JGit.

The ["implement FileReftableDatabase"](https://git.eclipse.org/r/#/c/146568/) change has been merged
into JGit and later [included in Gerrit v3.1.2](https://gerrit-review.googlesource.com/c/gerrit/+/247498).

The [Git reftable](https://github.com/eclipse/jgit/blob/master/Documentation/technical/reftable.md) is
an alternative storage for keeping the list of Git refs on the filesystem. The ones currently implemented
in Git are the loose refs and packed refs, which are both not scalable for repositories with a large number
of refs (e.g. 500k or more).

With regards to the reftable performance, the following table speaks more than a thousand words:

format      | cache | scan         | by name        | by SHA-1
------------|-------|--------------|----------------|------------------
packed-refs	| cold  |     402 ms   | 409,660.1 usec |	412,535.8 usec
packed-refs | hot   |              |   6,844.6 usec |    20,110.1 usec
reftable	| cold  |   112.0 ms   |      33.9 usec |       323.2 usec
reftable	| hot   |              |      20.2 usec |       320.8 usec

## Summit summary

The talks have been mainly centred on the new features introduced in Gerrit v3.1:

- The porting to PolyGerrit 2 and the new development team in Germany
- Performance improvements in v3.1
- Support for Git protocol v2

Some of the talks presented in Gothenburg have been replayed in Sunnyvale as well,
with the addition of brand-new talks about the new features and developments completed
in the past three months.

This year the Summit was hosted in the new home of GerritForge in the USA, downtown
Sunnyvale, at The Satellite in the historic Del Monte building.

### What's new in Gerrit v3.0/v3.1

David Ostrovsky, Luca Mianesio (GerritForge) and Patrick Hiesel (Google) have presented
the new features and improvements introduced in Gerrit v3.0/v3.1, two closely
related versions.

Gerrit v3.0/v3.1 include respectively 1,589 and 1,443 commits, which together makes over
3k of changes compared to the latest v2.16.x releases. Gerrit major release number has been
incremented because of breaking changes introduced:

- Removal of the GWT UI
- Removal of ReviewDb (deprecated from v2.16)
- Removal of pushes to refs/drafts/* and refs/changes/*

New and noteworthy feature include:

- Re-introduction of Git protocol v2
- Significant speed-up of the Gerrit frontend and backend, showing up to 2x performance
  improvement (Gatling automated tests)

Any upgrade to Gerrit v3.0/v3.1 require to have a stop at v2.16 and convert the changes from
ReviewDb to NoteDb.

### Road-map and migration path to Gerrit v3

Luca Milanesio (GerritForge) presented a deep-dive into the high-level process of
migrating Gerrit from old releases to the latest v3.1.

Migrating is always difficult, and Gerrit migrations before the advent of NoteDb were
alwyas cursed by the schema upgrades needed by ReviewDb. However, migrating to the latest
version is not an option and *must* be planned and executed sistematically.

Luca classified Gerrit migrations in four quadrants, based on their version distance
and installation size.

1. Trivial

   Small upgrade step (e.g. v2.15 to v2.16) for a small-sized Gerrit setup.
   It is typically resolved by a war upgrade and Gerrit restart.

2. Complex

   Small upgrade step for a large-scale Gerrit setup.
   It typically requires more coordination and communication with the teams about
   the planning and execution of the cutover plan. The outage window needs to be
   tested and reduced to a minimum.

3. Risky

   Big upgrade step (e.g. v2.11 to v3.1) for a small-sized Gerrit setup.
   The big gap of releases introduce functional differences and gaps on
   the different features (e.g. draft changes migrated to WIP/Private).

4. Ultrahazardous

   Big upgrade step (e.g. v2.11 to v3.1) for a large-scale Gerrit setup.
   THe big functional gap combined with a large setup involving potentially
   hundreds or thousands of people may lead to a very delicate and hazardous
   upgrade.

Luca went through the overview of how to plan and execute the migrations of type
1., 2. and 3. while advised to avoid type 4. migrations as they may lead to
expensive and un-necessary risks.

Any upgrade of type 4. can be translated as a series of upgrades of type 2. which
would lower the risk and increase the confidence and understanding of the new
Gerrit features.

Gareth Bowles (Apple) presented his experience on managing Gerrit and automating
each phase of its lifecycle using Ansible. Apple's installation has 1k projects with
over 670k patch-sets and used by over 800+ worldwide.

Cesare San Martino (GerritForge) explained how the adoption of Gerrit High-Availability
plugin and architecture can help in lowering the risks associated with migrations and
reduce the outage window to a minimum if not even to zero in certain cases.


### Gerrit Q&A with the maintainers

TODO

### What's cooking in JGit

TODO

### New developments and team structure in the PolyGerrit Team

Google's Gerrit frontend team has been successfully re-staffed with four new
hires over the summer. Today it consists of Ben, Dhruv, Dmitrii, Milutin, Ole,
Tao - all working from the Munich office alongside Google's backend team.

For the 3.1 release the frontend infrastructure has been changed to use Polymer
2 instead of 1, which among other things means that all UI components are
encapsulated using the Shadow DOM. The team's focus are further infrastructure
projects (Polymer 3, stronger typing, npm, content-security-policy, ...),
performance, checks and a new feature for tracking whose turn it is for all your
code reviews.

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

We all know metrics are important to monitor the status of our systems and avoid
our users to tell us Gerrit is not working before we realise it.

Gerrit logs are an under-evaluated gold mine of metrics.
In this [presentation](https://docs.google.com/presentation/d/1EeJdCngQaVBxJPQaGC2DYtTS9gzM9II-uoi7DtPQkw0/edit?usp=sharing)
Fabio Ponciroli (aka Ponch, GerritForge) showed its five favourites metrics which
help in the daily job of a Gerrit admin.

### Stress your Gerrit with Gatling

Fabio Ponciroli (GerritForge), aka Ponch, showed the work on implementing a consistent
end-to-end test scenario for Gerrit by leveraging the Gatling tool.

Testing Gerrit involves the invocation of REST-API by simulating the PolyGerrit UI and
also the use of Git/HTTP and Git/SSH protocol. Gatling, however, does not support
the Git protocol out-of-the-box. Ponch has introduced the gatling-git project,
that extends Gatling to include the Git protocol.

The definition of end-to-end tests is further simplified by using the Gatling “feeders”.
Those are sample data in JSON format, which can also be generated from existing
Gerrit production logs.

Ponch has then showcased, to Luca’s surprise, a real use-case of running load tests
against GerritHub.io, and they generated the expected spike of incoming traffic.

This is a [post](https://gitenterprise.me/2019/12/20/stress-your-gerrit-with-gatling/),
with the video of the presentation, about the topic published on the GerritForge blog.

## Feedback and proposals of improvements for the next Summits

TODO

----

Thank you again to all the attendees of the Gerrit User Summit 2019 in Volvo - Sweden
and GerritForge Inc - California. Looking forward to another exciting year of innovation
and development of the Gerrit Code Review platform and community.

Luca Milanesio (Gerrit Maintainer, Release Manager, ESC member)
