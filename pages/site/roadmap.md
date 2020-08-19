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

## Gerrit 3.3
Target: Q4 2020

* Pluggable authentication backend
* Performance improvements
  * Replace H2 persistence with other more performant backends
  * Improve Gerrit performance with mono-repos (tens of GBytes of size)
* Better UX
  * Attention Set (revising assignee and “bolding”)
  * Increased overview in Change Log
  * Porting unresolved comments to the latest patchset
  * Showing comment context (file content or diff) along with comment widget in ChangeLog and
    Comment Threads tab
  * Comment and Patchset Navigation
  * SubmitRules v2
  * Per-label configuration to copy scores onto successfully cherry-picked changes
* Infrastructure
  * TypeScript
  * Content-Security-Policy
  * Rework diff caches
  * Clean up project cache to allow to persist it
  * Persist project cache
  * Switch language level to Java 11
* Plugin Development
  * Bulk interface for PluginDefinedInfos in ChangeAttributeFactory
  * Allow plugins to provide is: operands

## Upcoming plugin improvements related to Gerrit 3.3
* New plugin: Allow group deletion
* Replication plugin
  * Support for external replication queue
  * Message-broker based replication queue
  * Improve unit testing
  * Make persistent events safely recoverable
  * Prevent pending events from significantly delaying server startup
  * Recover events on time basis instead of startup
  * Do not push to the same destination from more than one primary at a time
    (URI locks)
  * Shift the burden of firing pending events onto the specific
    replication threads for each event's remote
  * Distribute tasks to other nodes via a shared filesystem
* High-availability plugin
  * Support for global ref-db
  * Mention HA and setup for multiple primary hosts in Gerrit documentation
* Quota plugin
  * Simplify the plugin.

## Upgrades
* Be able to upgrade a huge site (Qualcomm) from 2.7 to latest stable release
  in less than 24 hours
  * Improve NoteDb offline migration speed (current timing is 24+ hours for Qualcomm)
  * Improve upgrade speed for specifically slow schemas

## Distant future
* Role-based access control
* Evaluate other web frameworks as potential replacements for Polymer
* Rework event infrastructure
* Pushing of server events into the frontend
* Protobuf for REST API entities
* Support for race-free zero-downtime pruning of git packed objects
