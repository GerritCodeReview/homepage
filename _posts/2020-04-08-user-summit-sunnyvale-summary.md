---
title: Summary of the Gerrit User Summit & Hackathon 2019 in Sunnyvale
tags: news summit hackathon
keywords: news summit hackathon
permalink: 2020-04-08-user-summit-sunnyvale-summary.html
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

Luca Milanesio (GerritForge), Matthias Sohn (SAP) and Martin Fick (Qualcomm) have
been discussing the issues associated with very large repositories:

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
of the JGit implementation of ref-table, which was initially designed by Shawn Pearce but never applied
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
packed-refs | cold  |     402 ms   | 409,660.1 usec |   412,535.8 usec
packed-refs | hot   |              |   6,844.6 usec |    20,110.1 usec
reftable    | cold  |   112.0 ms   |      33.9 usec |       323.2 usec
reftable    | hot   |              |      20.2 usec |       320.8 usec

### Merge of the two forks of the high-availability plugin

The [high-availability plugin](https://gerrit.googlesource.com/plugins/high-availability)
has been founded in 2016 by Ericsson with the scope of allowing an active failover of their
Gerrit master setup.
Over the years, the plugin has received many contributions by different companies, including
CollabNet, SAP and GerritForge.

Starting from 2018, GerritForge began to fork the plugin because of the need to have
urgent fixes merged that made their way also in the mainstream repository. However, as we all know,
forking is easy but merging is a lot more complicated and painful and the fork continued for over
Two years with duplication of efforts and imparity of fix levels between the two forks.

Marco Miller (Ericsson), David Ostrovsky and Luca Milanesio (GerritForge) worked hard to merge
the two forks and make them aligned in terms of functionality and fixes. After the hackathon and
in the following few weeks, the GerritForge's fork has been successfully merged into the main
repository.

The only active version of the high-availability plugin is now the mainstream repository.
David Ostrovsky and Luca Milanesio have been officially granted the role of maintainers, together with
the current Ericsson and CollabNet members.

### Multi-site plugin decoupled from Kafka and Zookeeper

The [multi-site plugin](https://gerrit.googlesource.com/plugins/multi-site) was originally released
in April 2019 and is fully based on Kafka/Zookeeper infrastructure for the alignment of indexes, caches
and events across sites.

During the hackathon, Marcin Czech (GerritForge) has worked in abstracting the Kafka/Zookeeper layer
out of the multi-site plugin. That allows Gerrit multi-site to be deployed in the future with a different
infrastructure, possibly more cloud-native and integrated with the major cloud provider services.

The Kafka broker interface has been put into the [kafka events plugin](https://gerrit.googlesource.com/plugins/kafka-events),
which was previously used only for stream events and now also for indexing/cache consistency.

With regards to Zookeeper, an initial request to include a generic support for a global-refdb has
[been presented](https://gerrit-review.googlesource.com/c/homepage/+/237980) but then abandoned because of
the unanimous rejection by the Gerrit community.

Waiting for a different solution to be presented, the support for Zookeeper has been then moved to
a GerritForge-owned [repository on GitHub](https://github.com/GerritForge/plugins_zookeeper).

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
version is not an option and *must* be planned and executed systematically.

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

Cesare San Martino (GerritForge) explained how the adoption of Gerrit high-availability
plugin and architecture can help in lowering the risks associated with migrations and
reduce the outage window to a minimum if not even to zero in certain cases.


### Gerrit Q&A with the maintainers

For the very first time the Q&A was a global event, allowing people on-site in Sunnyvale
and remote around the globe in streaming to interact and ask questions directly
to the Gerrit maintainers.

The questions were at 360 degrees covering multiple topics:

- Status of the Gerrit plugins
- Onboarding of new contributors to the Gerrit project
- New organisation of the Gerrit Open-Source community with ESC and CMs
- Gerrit vs. GitHub vs. GitLab: competition or integration
- Pull-request workflow for Gerrit

### What's cooking in JGit

Ivan Frade and Han-Wen Nienhuys (Google) have presented the new innovative
features that are coming in the next forthcoming versions of JGit.
This is the first time since the last [GitTogether in 2011](https://opensource.googleblog.com/2011/12/gittogether-2011.html)
that core Git contributors are participating with a mixed Git/Gerrit audience.

Ivan presented what's new on the JGit server side, which is the backend
that serves the Git protocol for the Chromium and Android Open-Source projects.

The new features introduced in JGit from v5.2/3/4/5 and master are focussed on:

- Exposing server options mechanism, made possible since the introduction of
  Git protocol v2. That allowed to enable precious features like the Git-protocol
  level tracing from a server-side perspective.

- Consistency on demand and update indexes, which allows Git servers on multiple
  sites to pass a consistency version token and detect when commits are replicated
  to remote servers and thus ready to be fetched.

- Reachability checker optimisation, which allows large repositories to reduce
  the execution time and CPU utilisation of the validation of the "WANT SHA1"
  commands received from the Git client.

- Sideband-all, which means that at any point in the communication the client
  and server can pass parallel information via the normal Git protocol client/server
  communication. That allows new use-cases like the packfile off-loading, which
  is a new capability that would communicate to a series of mirrors where the packfiles
  can be fetched concurrently.

- Local reftables, presented by Han-Wen, are an innovative storage format that
  allows repositories to scale to millions of refs without impacting significantly
  the access time on the filesystem and reducing lock contention in case of concurrent updates.


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

David Ostrovsky and Luca Milanesio (GerritForge) presented the work done
to extend the Gerrit DevOps Analytics Open-Source platform (GDA) to cover also
the use-case of the Android Open-Source Project (AOSP).

The GDA platform collects information about Git commits, reviews and logs and correlate
them together to build dashboards of KPIs that are relevant to the people involved
with the project.

Luca described the challenges of applying the platform to AOSP:

- Mirroring of AOSP repositories to GerritHub.io in order to minimise network
  traffic during the Big-Data processing.

- Scale-up the current performance of the analytics extractors and ELT so that
  AOSP branches are resolved quickly and without impact on the JVM utilisation.

- David has presented the challenge of parsing foreign NoteDb change-data using
  the Gerrit internal API.

### What's new in the Bazel tool-chain for Gerrit

David Ostrovsky (GerritForge) presented the advance in the Bazel latest versions
adoption in the Gerrit build tool-chain and its plugins.

The Gerrit build process is complex, and involves Java, JavaScript, 160+ dependencies,
150+ plugins built in two modes (standalone and in-tree). All of that needs to be
orchestrated, automated and executed in a fast, correct and reproducible way.

Gerrit started as a Maven build project (until v2.7) and then later moved to Buck
(v2.8-v2.13) and eventually adopted Bazel (v2.14 onwards). Bazel is the industry standard
for large, distributed and fast builds executed in the build server. It is used
by large companies around the globe, including Spotify, Uber, Stripe, nVidia, Volvo
and many others.

David explained how the overall build process works in Gerrit and highlighted the
versions where the build is actively supported by the community (v2.16 onwards). Bazel builds
are orchestrated by the [Gerrit CI](https://gerrit-ci.gerritforge.com), initially created
by GerritForge and now actively supported by the whole Gerrit community.

Last but not least, David explained some of the tips and tricks on how to perform
integration-tests in Gerrit, using the TestContainers library, which allows to automatically
test and validate more complex scenarios like ElasticSearch indexes and the Gerrit
multi-site plugin.

### Racy JGit

Matthias Sohn (SAP) presented the history of how time is used in JGit and the struggle
to improve the resiliency to the [git racy-reads problem](https://git-scm.com/docs/racy-git/en).

It all started with the [bug #544199](https://bugs.eclipse.org/bugs/show_bug.cgi?id=544199)
reported by Luca Milanesio (GerritForge) which was later fixed by adjusting the way packfiles cache
[consistency is checked](https://git.eclipse.org/r/#/c/138521/)
against the filesystem.

The fix opened up the pandora box of the 2.5s hard-coded resolution in JGit for dealing
with racy-reads. The additional checks to make sure that a packfile has not been changed
after being cached in memory, raised the
[bug #546891](https://bugs.eclipse.org/bugs/show_bug.cgi?id=546891) related to the performance
regression observed.
The reason why JGit historically used a hard-coded resolution of 2.5s was the FAT filesystem
storing timestamps with 2s resolution (the extra .5s is a safety margin), which can still be
found in some Windows systems running Eclipse.

Matthias and the other folks at SAP have been working hard to improve the way the filesystem
resolution is detected and make all of that available in JGit transparently, without having
to configure anything special in Gerrit or JGit.

The problem was not easy to resolve as the complex combination of JVM versions, OSes and filesystems
created a series of conditions that could have made the calculation of the resolution a lot harder
than initially thought.

The challenge was eventually completed after seven months of work by six different authors
(Chris, Han-Wen, Luca, Matthias, Marc, Thomas) and 82 commits across 22 different service releases. JGit
with the racy-reads problem resolved and optimised is now included in all the latest active versions
of Gerrit.

### OSSUM with Gerrit


Miikka Andersson from CollabNet gave a presentation about the company’s latest product
initiative: ossum. Ossum is a developer-focused SaaS solution for software engineering
needs with a strong focus on planning, version control, and Continuous Integration.

Gerrit is one of ossum’s key components on top of which the entire version control service
was built. The decision of choosing Gerrit for the backend wasn’t coincidence: CollabNet
has a long history with Gerrit and ossum is already company’s second product providing
Gerrit-powered Git service.

In his [presentation](https://storage.cloud.google.com/gerrit-talks/summit/2019/ossum-GUS_2019.pdf),
Miikka went through some of the key factors contributing to the decision to choose
Gerrit to be used as Git backend for the new product initiative. In addition to that, some
of the key takeaways and lessons learnt from earlier Gerrit-based product initiatives
were shared with the audience.

### Revert submission

Gal Paikin (paiking@) from Google showed a new feature he was working on.
In this presentation [presentation](https://docs.google.com/presentation/d/e/2PACX-1vTkbE5AIWEFcEyUnQ6ZlfglClgsX9h5fjB6dkSsCvXuL75Jd0DdsZfarvKswYtyCKUN0_QJQDdJ8Qzw/pub?start=false&loop=false&delayms=10000&slide=id.g6c93d79dc5_0_29)
he described RevertSubmission, a new endpoint that allows reverting multiple changes simultaneously.
This endpoint is meant to ease the workflow of many engineers that submit many changes together.

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

For the very first time, the Q&A with the maintainers was done with a vast audience,
including the people from Europe in Gothenburg, the users in Silicon Valley and the
remote attendees remotely using the [GerritForge Live streaming](https://live.gerritforge.com).

The audience was very active and asked many questions related to the Gerrit release
management (can Gerrit have more stable and well-defined release plan?), to the plugins
lifecycle management and to the new processes introduced in the community like the
design-driven contribution.

Also the recurring question about the "competition" between Gerrit, GitLab and GitHub came
back, with different feedback from various users and companies. There is also people still
happily using IBM ClearCase ! That means there isn't a golden standard for using a golden
platform that would resolve all the use-cases.

The main reason people and companies have adopted Gerrit is the need for scalability and
managing a large number of users across different sites across the globe.

Another thing that emerged again is how to smooth the learning curve for the new adopters
of Gerrit Code Review, possibly giving the possibility to contribute using a branch or pull-request
review model, in conjunction with the typical change-based code review.

All the discussions and hints were captured in the
[Gerrit Code Review Issue Tracker](https://bugs.chromium.org/p/gerrit/issues/list?can=2&q=label%3ARetrospective)
associated with the label `retrospective` for easier discovery and tracking.

----

Thank you again to all the attendees of the Gerrit User Summit 2019 in Volvo - Sweden
and GerritForge Inc - California. Looking forward to another exciting year of innovation
and development of the Gerrit Code Review platform and community.

Luca Milanesio (Gerrit Maintainer, Release Manager, ESC member) with contributions and
reviews by David Pursehouse (CollabNet), Fabio Ponciroli (GerritForge), Matthias Sohn (SAP),
David Ostrovsky, Gal Paikin (Google), Douglas Luedtke (Garmin), Nasser Grainawi (Qualcomm).
