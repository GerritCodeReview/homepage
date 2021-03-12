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
[reach out to the ESC](https://gerrit-documentation.storage.googleapis.com/Documentation/3.1.0/dev-roles.html#steering-committee-member).

## Gerrit 3.4
Target: Q2 2021

* UX
  * CI Results Tab / Frontend plugin
  * Per-label configuration to copy scores onto successfully cherry-picked changes
* Support for race-free zero-downtime pruning of git packed objects

## Upcoming plugin improvements related to Gerrit 3.4
* New plugin: Allow group deletion
* Replication plugin
  * Support for external replication queue
  * Message-broker based replication queue
  * Improve unit testing
  * Make persistent events safely recoverable
  * Prevent pending events from significantly delaying server startup
  * Distribute tasks to other nodes via a shared filesystem
* High-availability plugin
  * Mention HA and setup for multiple primary hosts in Gerrit documentation

## Gerrit 3.5
Target: Q4 2021

* UX
  * Composable SubmitRules
* Switch language level to Java 11

## Upcoming plugin improvements related to Gerrit 3.5
* Replication plugin
  * Recover events on time basis instead of startup
  * Do not push to the same destination from more than one primary at a time
    (URI locks)
  * Shift the burden of firing pending events onto the specific
    replication threads for each event's remote


## Upgrades from 2.7 to latest stable release
* Be able to upgrade a huge site (Qualcomm) from 2.7 to latest stable release
  in less than 24 hours
  * 2.16.x: Improve NoteDb offline migration speed (current timing is 24+ hours for Qualcomm)
  * Improve upgrade speed for specifically slow schemas

## Distant future
* Role-based access control
* Evaluate other web frameworks as potential replacements for Polymer
* Rework event infrastructure
* Pushing of server events into the frontend
* Protobuf for REST API entities
* Pluggable authentication backend
* Quota plugin
  * Simplify the plugin.
