---
title: "Tentative Roadmap"
permalink: roadmap.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

The Gerrit roadmap is a best-effort collection of features/improvements that the ESC is aware of.
The intention is to give the wider community - contributors as well as administrators and users - a
sense of what they can expect to see in upcoming releases.

This is a living document, so things can change anytime. There is no ordering between
features/improvements.

If you’re a contributor and you intend to work on something which is not mentioned here, please
create a change and select the ESC members as reviewers. Don’t use this channel to submit ideas or
wishes you want someone else of the community to work on!

If someone would like to be involved when a specific topic is tackled, please
[reach out to the ESC](https://gerrit-documentation.storage.googleapis.com/Documentation/3.4.1/dev-roles.html#steering-committee-member).

## Gerrit 3.6
Target: Q2 2022

See [Google 2021 Q4 OKRs](google-okrs.html).

## Gerrit 3.5
Target: Q4 2021

See [Google 2021 Q3 OKRs](google-okrs.html).

* UX
  * Composable SubmitRules
* Switch language level to Java 11

## Upcoming plugin improvements related to Gerrit 3.5
* New plugin: Allow group deletion
* Replication plugin
  * Recover events on time basis instead of startup
  * Do not push to the same destination from more than one primary at a time
    (URI locks)
  * Shift the burden of firing pending events onto the specific
    replication threads for each event's remote
  * Support for external replication queue
  * Message-broker based replication queue
* High-availability plugin
  * Mention HA and setup for multiple primary hosts in Gerrit documentation

## Upgrades from 2.7 to latest stable release
* Be able to upgrade a huge site
  ([Qualcomm](https://groups.google.com/g/repo-discuss/c/WVwvngCkRMs/)) from 2.7
  to latest stable release in less than 4 hours
  * [Improve](https://gerrit-review.googlesource.com/q/hashtag:notedb-migration-optimizations)
    NoteDb offline migration speed (Nov 2021 timing is ~2.5 hours for Qualcomm)
  * [Improve](https://gerrit-review.googlesource.com/q/hashtag:schema-optimizations)
    schema upgrade speed (Nov 2021 timing is ~3 hours for Qualcomm)
  * [Improve](https://gerrit-review.googlesource.com/q/hashtag:reindex-optimizations)
    offline reindex speed (Nov 2021 timing is ~2 hours for Qualcomm)
  * Additional improvements planned through Q1 2022
