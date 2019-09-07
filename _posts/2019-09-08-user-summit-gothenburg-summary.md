--
title: "Gerrit User Summit 2019 at Gothenburg - Summary"
tags: news
keywords: news
permalink: 2019-09-08-user-summit-gothenburg-summary.html
summary: "Summary of the Gerrit User Summit 2019 at Gothenburg"
hide_sidebar: true
hide_navtoggle: true
toc: true
--

## A year of the Summit innovations

The Gerrit User Summit 2019 can definitely be defined as truly innovative in
its format and audience.

For the first time in the Gerrit history, the Summit is split into two parts.
Volvo Cars have hosted the first in Gothenborg (Sweden) while the second will take
place from the 11th to the 17th of November at GerritForge Inc. HQ in Sunnyvale,
CA (USA).

The Summit has been repeated twice in a year on both sides of the Atlantic. The
European and US communities come from different background and have different
needs.  The Gerrit Code Review Community is global and is willing to share
experiences and receive feedback from both sides.

We are also innovating on the Hackathon perspective, with three new elements:

1. The Hackathon is now open to everyone, including the people that have never
   contributed to Gerrit before. Experienced maintainers have paired with newbies
   to guide through the very first contributions.

2. The Hackathon at Volvo Cars has been 100% focussed in triaging the massive
   backlog of open issues and fixing as many bugs as possible for the latest
   three supported branches: stable-3.0, stable-2.16 and stable-2.15.

3. The OpenStack and Gerrit communities finally have met and started talking and
   interacting more closely.

## The Hackathon in numbers

- N issues triaged
- M bugs closed
- O changes opened of which P merged
- Q participants to the Hackathon of which R that have never contributed before
  to Gerrit and T attending remotely from Germany, United Kingdom and the United
  States 
- S attendees to the Summit

## Hackathon summary

During the Hackathon, David Pursehouse and Luca Milanesio have been working at
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
- The improvement of Gerrit performances and the introduction of automated tools
  for end-to-end, performance and load testing.

All the talks have been recorded and will be soon published on the
[GerritForgeTV YouTube channel](https://youtube.com/gerritforgetv), together with
the past two years conferences videos.

### Gerrit at Volvo Cars

Nicholas Mucci (Volvo Cars) is both the main organizer of the Summit in
Gothenburg and also the key player of the adoption of Gerrit Code Review for the
development of some of the critical components of the modern Volvo Cars.
He has stressed how important it is for Volvo Cars the adoption of OpenSource.
The security of a car lies in the ability to have complete control and the
ability to make software fixes. Cars need to be safe and supported for over 15
years, independently from vendor lock-ins, software licenses or black-box closed
source components.
The CI/CD pipeline of Volvo Cars also includes some key components, like Zuul CI
and Jenkins, both truly OpenSource projects.

### First-class integration with the Checks plugin

Alice Kober-Sotzek (Google) has presented the current state-of-art of the checks
plugin, developed by Google in 2018/2019. The plugin allows other CI/CD tools,
such as Jenkins, to publish its progress and build results directly into Gerrit
Code Review.

There are multiple benefits in having a dedicated API in Gerrit:
Gerrit users can get direct feedback on the Change about the build validation
status, without having to jump into another tool.
Various types of checks (e.g. code-style, unit-test, integration-test, load-tests
...) can be defined and displayed more concisely, without having to set multiple
labels.
Build actions can be triggered directly from the Gerrit change screen,
simplifying the daily lifecycle of the patch-sets validations.
The topic has been of extreme interest, specifically from the OpenStack
Community. An existing plugin (verify-status) already covers a similar set of
functionalities. However, it is mostly incompatible with the recent versions of
Gerrit; it doesn't have a PolyGerrit UI and relies on an external relational DBMS.
The maintainers of the Zuul CI project has explicitly shown interest in
integrating soon with the checks API.

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
uptime.gerrithub.io and pingdom.com.

### Labels & Prolog-less submit rules

Edwin Kempin (Google) has showcased the ability to start expressing Gerrit submit
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

With regards to the future of Gerrit and Prolog, most likely it would be removed
from core and just included as a plugin for those who still require it in production.

### End-to-End Git/Gerrit testing with Gatling

Fabio Ponciroli (GerritForge), aka Ponch, showed the work on implementing a
consistent end-to-end scenario for Gerrit by leveraging the Gatlin tool.
Testing Gerrit involves the invocation of REST-API by simulating the PolyGerrit
UI and also the use of Git/HTTP and Git/SSH protocol. Gatlin, however, does not
support the Git protocol out-of-the-box. Ponch has introduced the gatling-git
project, that provides the ability to extend Gatlin to include the Git protocol.

The definition of the end-to-end tests is further simplified by using the Gatling
"feeders". Those are sample data in JSON format, which can also be generated from
existing Gerrit production logs.

Ponch has then showcased, with Luca's surprise, a real use-case of running load
tests against GerritHub.io, and they generated the expected spike of incoming
traffic.

### Using Zuul CI with Gerrit

Monty Taylor (RedHat) has introduced Zuul CI, an OpenSource project created for
running the validation of OpenStack changes on Gerrit Code Review.
The OpenStack project started their CI/CD pipeline adopting Jenkins CI and
afterwards implementing some higher-level projects like the Jenkins Job Builder
for templating and auto-generating the build jobs.

However, Jenkins did not turn out to be powerful enough for its inability to
"juggle" the validation of multiple changes together across components, which is
a key requirement of the CI validation for OpenStack.

None of the OpenSource alternatives to Jenkins was enough to satisfy the
OpenStack requirements, and thus they decided to create a brand-new CI system,
named Zuul CI.

Zuul CI jobs definition does not differ much from the Jenkins-Job-Builder YAML
but relies on Notepool and Ansible for job scheduling and execution.

### TBC: Day 2

