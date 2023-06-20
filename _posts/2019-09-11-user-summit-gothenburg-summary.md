---
title: Summary of the Gerrit User Summit 2019 in Gothenburg
tags: news summit hackathon
keywords: news summit hackathon
permalink: 2019-09-11-user-summit-gothenburg-summary.html
summary: "Summary of the Gerrit User Summit 2019 in Gothenburg"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## A year of the Summit innovations

The Gerrit User Summit 2019 can definitely be defined as truly innovative in
its format and audience.

For the first time in the Gerrit history, the Summit is split into two parts.
Volvo Cars have hosted the first in Gothenburg (Sweden) while the second will take
place from the 11th to the 17th of November at GerritForge Inc. HQ in Sunnyvale,
CA (USA).

The Summit has been repeated on both sides of the Atlantic: the
European and US communities come from different background and have different
needs.  The Gerrit Code Review Community is global and is willing to share
experiences and receive feedback from both sides.

We are also innovating on the Hackathon perspective, with three new elements:

1. The Hackathon is now open to everyone, including the people that have never
   contributed to Gerrit before. Experienced maintainers have paired with newbies
   to guide through the very first contributions.

2. The Hackathon at Volvo Cars has been 100% focused in triaging the massive
   backlog of open issues and fixing as many bugs as possible for the latest
   three supported branches: stable-3.0, stable-2.16 and stable-2.15.

3. The OpenStack and Gerrit communities finally have met and started talking and
   interacting more closely.

## The Hackathon and Summit in numbers

- 13 talks by 10 speakers coming from the USA, Germany, UK, Finland and France
- 42 attendees to the Summit
- 19 participants to the Hackathon, 6 of them have never contributed before
  to Gerrit, 3 attending remotely from Germany, 1 from United Kingdom, 1 from USA
  and 1 from Japan
- 226 issues triaged of which:
  * 74 fixed (32%)
  * 56 would not be fixed (25%)
  * 45 could not be reproduced (20%)
  * 27 accepted as issues (10%)
  * 14 flagged as invalid, duplicate or missing information (9%)
  * 10 new issues raised (4%)
- 57 changes opened of which 48 of them have been merged
- 3 Gerrit releases made by 2 release managers

## Hackathon summary

During the Hackathon, David Pursehouse and Luca Milanesio have been working on
the release of Gerrit v2.15.16, v2.16.11.1 and v3.0.2, thanks to the precious
help from Gert van Dijk for writing and reviewing the release notes.
In addition to the bug-fixing activity, James Blair and Monty Taylor (both
RedHat, working on the OpenStack project) have presented the project
[Reno](https://github.com/openstack/reno).

The OpenStack project uses it for managing the collection and generation of the
release notes automatically, which can be useful for the Gerrit Code Review
project.
Other interesting discussions have been around the migration process from Gerrit
v2.13 or earlier to v3.0.

## Summit summary

The talks have been mainly centred on the automotive use-case, characterized by:

- The need to build and validate multiple components together
- The scalability of Gerrit Code Review across various sites
- The improvement of Gerrit performance and the introduction of automated tools
  for end-to-end, performance and load testing.

All the talks have been recorded and will be soon published on the
[GerritForgeTV YouTube channel](https://youtube.com/gerritforgetv), together with
the past two years conferences videos.

### Gerrit Community Retrospective

Edwin Kempin (Google) is one of the longest-serving maintainers of the Gerrit Code
Review project. He is one of the Community Managers working hard to strengthen
the collaboration and to improve the way the whole project works.

He has organized an "agile-style" retrospective on what is working well and what
can be improved in the whole project, giving complete freedom to anyone to
participate either on-site and on-line, using a digital ideas board.

The full report has been published on the
[Repo-Discuss Mailing List](https://groups.google.com/forum/#!searchin/repo-discuss/retrospective/repo-discuss/CqFvLzs4Leg/SX5Rq8VkAAAJ).

### Gerrit at Volvo Cars

Nicholas Mucci (Volvo Cars) is both the main organizer of the Summit in
Gothenburg and also a key player in the adoption of Gerrit Code Review for the
development of some of the critical components in modern Volvo Cars.
He stressed the importance of adopting Open Source for Volvo Cars.
Every software component of a car needs to be able to receive updates and security fixes,
which means that Volvo needs to have control over the CI/CD pipeline for improving
and building code constantly.
Cars need to be safe and supported for over 15 years, independently
from vendor lock-in, software licenses or black-box closed source components.
The CI/CD pipeline of Volvo Cars also includes some key Open Source components,
like Zuul, Jenkins and, of course, Gerrit Code Review.

### First-class integration with the Checks plugin

Alice Kober-Sotzek (Google) has presented the current state-of-art of the checks
plugin, developed by Google in 2018/2019. The plugin allows other CI/CD tools,
such as Jenkins, to publish build progress and results directly into Gerrit
Code Review.

There are multiple benefits in having a dedicated API in Gerrit:
Gerrit users can get direct feedback on a Change about its build validation
status, without having to jump into another tool.
Various types of checks (e.g. code-style, unit-test, integration-test, load-tests
...) can be defined and displayed more concisely, without having to configure multiple
labels.
Build actions can be triggered directly from the Gerrit change screen,
simplifying the daily lifecycle of patch-sets validations.
There was high interest for this topic, specifically from the OpenStack
Community. An existing plugin (verify-status) already covers a similar set of
functionality. However, it is mostly incompatible with the recent versions of
Gerrit; it doesn't have a PolyGerrit UI and relies on an external relational database.
The maintainers of the Zuul project have explicitly shown interest in
integrating soon with the checks API and also
[collaborating on its development](https://gerrit-review.googlesource.com/q/topic:subchecks).

### Gerrit goes multi-site

Luca Milanesio and Marcin Czech (GerritForge) have presented the brand-new
multi-site plugin for Gerrit Code Review. Finally, after many years of waiting,
the rest of the OpenSource Community can deploy multiple instances of Gerrit
Masters across the globe.
Previously, only Google was running Gerrit in a multi-master/multi-site fashion.
Also, WANdisco announced years ago a commercial multi-site solution, based on a
custom fork of Gerrit v2.13 and its proprietary replication solution.

The multi-site plugin is available for any version of Gerrit from v2.16 onwards
and requires NoteDb. It has been adopted since May on GerritHub.io. The
reliability of the site has jumped to 100% since then, certified by both
[uptime.gerrithub.io](https://uptime.gerrithub.io) and [pingdom.com](http://stats.pingdom.com/n9a8tbptdn14/994191).

### Labels & Prolog-less submit rules

Edwin Kempin (Google) has showcased how to implement Gerrit submit
rules without the use of Prolog but using a simple Gerrit plugin. The Prolog
language has been a difficult part of the Gerrit submit rules: only one (Luca) in
all audience declared to like it as a programming language.
However, nobody (even Luca) feels confident in reading and writing it easily.
The introduction of the Prolog cookbook has improved the situation in the past.
However, people still misuse the tool by simply "copy&paste" random parts of the
cookbook and at times generating overload on Gerrit and a massive headache for
the Gerrit admins.

Starting from Gerrit v2.16 the submit rules can be implemented via plugins. Edwin
showcased a sample plugin (simple-submit-rule) for implementing some useful
rules, such as blocking a change if some of the comments are not addressed, and a
lot more.

With regards to the future of Gerrit and Prolog, most likely it would be moved
from Gerrit core to a plugin for those who still require it in production.

### End-to-End Git/Gerrit testing with Gatling

Fabio Ponciroli (GerritForge), aka Ponch, showed the work on implementing a
consistent end-to-end test scenario for Gerrit by leveraging the Gatling tool.
Testing Gerrit involves the invocation of REST-API by simulating the PolyGerrit
UI and also the use of Git/HTTP and Git/SSH protocol. Gatling, however, does not
support the Git protocol out-of-the-box. Ponch has introduced the gatling-git
project, that extends Gatling to include the Git protocol.

The definition of end-to-end tests is further simplified by using the Gatling
"feeders". Those are sample data in JSON format, which can also be generated from
existing Gerrit production logs.

Ponch has then showcased, to Luca's surprise, a real use-case of running load
tests against GerritHub.io, and they generated the expected spike of incoming
traffic.

### Using Zuul with Gerrit

Monty Taylor (RedHat) introduced Zuul, an OpenSource project created for
running the validation of OpenStack changes on Gerrit Code Review.

The OpenStack project started their CI/CD pipeline adopting Jenkins CI and
afterwards implementing some higher-level projects like the Jenkins Job Builder
for templating and auto-generating the build jobs.

However, Jenkins wasn't powerful enough to "juggle" the validation of multiple
changes together across components, which is a key requirement of the CI validation
for OpenStack.

None of the OpenSource alternatives to Jenkins was sufficient to satisfy the
OpenStack requirements, and thus they decided back in 2012 to create a brand-new
CI system, named [Zuul](https://zuul-ci.org).

Zuul's job definition does not differ much from the Jenkins-Job-Builder YAML
but relies on [Nodepool](https://zuul-ci.org/docs/nodepool/) and
[Ansible](https://www.ansible.com/) for job scheduling and execution.

Monty and James have already started to implement
[Zuul for upstream Gerrit](https://issues.gerritcodereview.com/issues/40011149),
and we hope to show the progress at the next forthcoming Gerrit User Summit 2019
USA in November in Sunnyvale CA.

### Code review at Tuleap: lessons from the trenches

Thomas Gerbet (Enelean) is part of the Tuleap Team in Grenoble (France).
Gerrit Code Review has been part of their daily development pipeline since the
beginning and they shared their experience on regular reviews.

Gerrit has been the central focal point of the collaboration and helped to improve
the communication and exchange of ideas. In addition to providing a tool for
reviews, it has encouraged people to focus more on communicating effectively,
even face-to-face and with mutual respect and constructive behaviours.

The Tuleap Team had adopted Gerrit from the very first versions when the
distinctive Android-green theme still characterized it. So far, they have been
able to follow all the upgrade cycles, and they are happy to be running on the
latest v3.0 with NoteDb.

### Gertty, the TTY-based Gerrit UI

James E. Blair (RedHat) impressed the audience with its revolutionary TTY-based
UI for Gerrit Code Review. It is quite remarkable how James managed to implement the
full workflow by simply using the Gerrit REST-API and building a fully functional
experience by only using your keyboard.

During the daily work of software development, the keyboard is the central part
of where the activity takes place. Changing the context and opening a web-browser
with a different experience, can be time-consuming and cause the break of the creative
flow. Gertty comes to the rescue and gives to those who feel more productive with
a keyboard the ability to do the whole lifecycle in the fast and most efficient way
possible.

One extra goodie, which is very important for everyone that is travelling for work,
is the ability to fully work off-line and sync back once the connectivity is back.
This was also one of the main goals of the Gerrit project founder, Shawn Pearce: using
the power of Git for allowing a full peer-to-peer cooperation between the members of
the community, including reviews.

Gertty, however, isn't quite there yet, because still relies on a central Gerrit server
and the meta-data is stored in a SQLite database on the local computer. However, James
was open to the idea to remove the local database and place it by the NoteDb
format from Gertty, which would be great as it would implement exactly the way that Shawn
initially designed the Gerrit product.

James also made, during the Hackathon, important fixes to Gertty to make it
fully compatible with the latest version v3.0.x of Gerrit and with
gerrit-review.googlesource.com.

### Towards a lightning-fast Gerrit

Patrick Hiesel (Google) presented remotely from Munich the work that is currently
underway on the master branch of the Gerrit Code Review project.

Google has spent the last year and a half on the stabilization and improvement of the
Gerrit user-experience, using a scientific approach:

1. Define the critical user journeys
2. Measure the user-centric metrics on the page load
3. Improve and iterate

The targets for \*-review.googlesource.com were, for the change display screen, set to
2s and 5s, for the 90th and 95th percentile.

A lot of work has been made on Gerrit for improving the cache effectiveness, switching
from Java serialization to protobuf, which preserves compatibility across Gerrit versions
and upgrades.

With regards to the access to indexes, dashboards have been moved to make parallel queries
so that multiple parts of the page can be loaded concurrently. With regards to the UI
rendering, the components are now lazy-loaded. The number of round-trips from the
browser to the backend has also been reduced to a minimum.

A lot more work is ongoing for the forthcoming v3.1 of Gerrit, including:

- Completion of the JGit/ref-table implementation started from the original design made
  by Shawn.
- Switch to Polymer 2 and then to the lit-elements.
- Split-up of the current monolith gr-app.js into multiple components per page

Last but not least, Patrick gave useful recommendations on how to improve performance
on your current version of Gerrit, making the right choices for caches, CPUs and heap
utilization.

More progress on Gerrit v3.1 and the performance work will be presented at the Gerrit
User Summit in Sunnyvale, in November.

### Dependency visualization for Gerrit Code Review

The Summit has concluded with yet another exciting talk by Michael Watkins (Softagram).

Just nine months ago, Shane McIntosh (McGill University) presented the
[BLIMP Tracer](http://rebels.ece.mcgill.ca/papers/icsme2018_wen.pdf) research work on
the automated structural analysis of code review changes. Now Softagram, a small
startup based in Finland, presented an original commercial version of the same concept,
production-ready and fully integrated with Gerrit Code Review.

Michael went through the three central values provided by the automated structural change
analysis:

1. Graphical visualisation of the impact of the code change
2. Insights on the code changed
3. Automatic checks and scoring of the change

Code Review has become a "huge activity", with over 1 million code reviews created
world-wide every day. Moving a lot of repetitive activity from humans to robots is the
key to make reviews more accurate and enjoyable, leaving a lot of repetitive checks to
robots.

Michael also implemented a fully working plugin for integrating the output produced by
Softagram into the Gerrit change screen. That was a fascinating experiment for
the following reasons:

- Before joining Softagram, Michael had never used Gerrit before. However, he managed
  to learn how to use it quite quickly.
- He managed to develop a brand-new integration for Gerrit without any prior experience
  with the development of plugins

The integration will grow soon and, as Gerrit Community, we are
fully committed to helping Michael and all the other new contributors to get started with
Gerrit development and start contributing for making it better and easier to use.

We are all looking forward to seeing Softagram integration used for the Gerrit Code
Review project, as their solution is free for OpenSource projects.

## Feedback and proposals of improvements for the next Summits

Nicholas Mucci (Volvo Cars) has concluded the event by giving the opportunity
to all participants to the Summit to share their feedback and give new ideas
on how to make the event better next time.

1. We should publish the action items from the Hackathon and Summit and act on them.

   Edwin Kempin gave immediate progress on this, by publishing all the action items
   from the retrospective to the
   [Gerrit Code Review Issue Tracker](https://issues.gerritcodereview.com/issues?q=is:open).

2. We should better advertise the Hackathon and Summit. Outside of the immediate Gerrit
   community, it could be hard for people to learn about these events.

   Luca Milanesio advertising the Summit to the JGit community and Han-Wen (Google)
   invited members of the Google Development Team working on Git/JGit to come and
   present their latest innovations.

3. In expanded advertising, we should include a call for talks.

   The Talks are already open to everyone and go through the Gerrit Code Review process.
   The Summit website is simply a Gitiles view of the `summit/2019` repository.
   However, the process would not have been necessarily clear to everyone, and we will
   commit to making it more accessible and visible for submissions.

4. European summits should be in cheaper countries than Scandinavia; it can be hard to
   get budget for Sweden.  The challenge is then finding a host and site.

   The problem with Gerrit Code Review adoption in Europe is that it is mainly focussed
   on the northern countries, with Sweden and Finland in the first places because of
   the historical use from companies like Nokia and Ericsson.

   It was very nice to see from Enalean that Gerrit is also used in France, which could
   potentially be a cheaper destination for the next Summit in 2020, assuming that a
   company is willing to host the event.

5. We should consider piggy-backing on other related conferences to minimize travel
   costs (e.g. DevOps World, I/O).

   DevOps World was in mid-August in San Francisco. However, the associated costs for the
   location and the time of the year could have been exactly in conflict with the
   previous proposal of making the travelling less expensive. However, other European
   events about OpenSource, like
   [FOSDEM 2020](https://fosdem.org/2020/news/2019-08-11-dates-fosdem-2020/) are in a
   more affordable location and could be an excellent opportunity to get more communities
   together.

----

Thank you again to all the attendees of the Gerrit User Summit 2019 in Volvo - Sweden
and see you in November at Sunnyvale, for the release of Gerrit Code Review v3.1.

Luca Milanesio (Gerrit Maintainer, Release Manager, ESC member)
