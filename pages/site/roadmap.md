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

## Gerrit 3.2
Target: Q2 2020

* Allow group deletion
* Pluggable authentication backend
* Performance improvements
  * Latency improvements for ‘git push’
  * Latency improvements for critical user journeys on the Web UI: View dashboards as well as change
    and diff screens. Write comments and post a review. All of these actions should complete in 2s
    on the 90th percentile and 5s on the 99th percentile.
  * Experimental support for filesystem-based RefTable: Speed improvements for repositories with a
    large number of refs.
  * Replace H2 persistence with other more performant backends
  * Improve Gerrit performance with mono-repos (tens of GBytes of size)
* Better multi-master / multi-site support
  * Support for pluggable global ref-db (JGit or Gerrit)
  * Zookeeper-based global ref-db
* Frontend infrastructure
  * Polymer 3
    * Class based components
    * Migrate from bower to npm and simplify the BUILD process
    * Get rid of html imports, everything plain javascript
  * Content-Security-Policy
  * TypeScript
  * File Upload
* Better UX
  * Attention Set (revising assignee and “bolding”)
  * Increased overview in Change Log
  * Comment and Patchset Navigation
  * Improved theming support: Spacing and Fonts
* Robot comments
  * Support preview/apply fix feature
  * Polish experience especially regarding robot comments posted on every patch set
* Java 11
  * Officially supported for production use
* ssh client
  * migrate from jsch to mina-sshd, this is already supported by jgit since 5.2

## Upcoming plugin improvements related to Gerrit 3.2
* Replication plugin
  * Better multi-master support
  * Support for external replication queue
  * Message-broker based replication queue
* Checks plugin
  * Support for sub-checks
  * Override status
  * Refine UI with regards to many checks
* High-availability plugin
  * Support for global ref-db
  * Mention HA and multi-master setup in Gerrit documentation

## Gerrit 3.3
* Java 11
  * Switch language level to Java 11

## Upcoming plugin improvements related to Gerrit 3.3
* Quota plugin
  * Simplify the plugin.

## Distant future
* Role-based access control
* Evaluate other web frameworks as potential replacements for Polymer
* Rework event infrastructure
* Pushing of server events into the frontend
* Clean up project cache to allow to persist it
* Persist project cache
* Persist account cache
* Rework diff caches
* Protobuf for REST API entities
