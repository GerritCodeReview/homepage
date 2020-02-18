---
title: "Gerrit Code Review - Plugins"
permalink: plugins.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## About this page

1. This page lists all the (non [core]) [plugins] known to the Gerrit project.
   * -With their compatibility status across the [supported] version branches.
   * Some plugins might be missing from this page.
     * [Contributions] to add them are welcome.

2. These plugins are made by different parties and maintained to varying degrees.
   * Therefore, the Gerrit project does not guarantee their reliability.
   * However many are reliable and valuable integrations across Gerrit deployments.
   * There is a [parent] component for plugin-specific components/issues in Monorail.

3. There are CI build [scripts] for every plugin.
   * Each script builds that plugin against all the branches it supports.
     * Some plugins don't have branches but still support them, through their `master` branch.
   * That CI is the public service offering the download of pre-built plugin jar files.

## Compatibility matrix

1. Below, each plugin name has a link to that plugin's documentation files, `master` version.
   * If the plugin has no source documentation files, then that link points to its README page.
   * A brief yet revealing summary of the plugin About markdown file shows.
     * The active form or present tense (third person) is used for summaries.
     * Summaries are shorter than plugin's About information, so this is usable and maintainable.
2. Each branch name links to the corresponding CI jobs view, for the current build status.
   * Plugin tests are currently not executed by the formal Gerrit project CI.
3. Plugins are either
   * compatible with the branch's Gerrit version (YES)
   * or incompatible (NO) -or yet to be proven as compatible.
   * Proving version compatibility requires the corresponding CI [scripts]:

| Plugins            | Branches |              |              |               | About
|--------------------|----------|--------------|--------------|---------------|------
|                    | [master] | [stable-3.1] | [stable-3.0] | [stable-2.16] |
| [account]          | YES      | YES          | YES          | YES           | Provides the ability to manage accounts
| [admin-console]    | YES      | YES          | YES          | YES           | Provides user-level and access control information
| [analytics]        | YES      | YES          | YES          | YES           | Exposes aggregated Gerrit data metrics over REST and ssh APIs
| [analytics-wizard] | YES      | NO           | YES          | YES           | Provisions a new GerritAnalytics stack
| [audit-sl4j]       | YES      | YES          | YES          | YES           | Pushes audit Gerrit events to the LoggerAudit SLF4J appender
| [automerger]       | YES      | NO           | YES          | YES           | Allows automatic merging of changes from one branch to another
| [autosubmitter]    | YES      | NO           | YES          | YES           | Submits changes when all approvals/preconditions are satisfied
| [avatars-external] | YES      | NO           | YES          | YES           | Allows to use an external url to load the avatar images from
| [avatars-gravatar] | YES      | YES          | YES          | YES           | Provides avatars from gravatar.com or others serving that API
| [batch]            | YES      | NO           | NO           | YES           | Previews proposed Gerrit changes to multiple projects/refs
| TODO               | TODO     | TODO         | TODO         | TODO          | TODO
| [emoticons]        | NO       | NO           | NO           | YES           | Allows users to see emoticons in expanded comments as images
| TODO               | TODO     | TODO         | TODO         | TODO          | TODO

[core]: https://gerrit-review.googlesource.com/Documentation/config-plugins.html#core-plugins
[plugins]: https://gerrit-review.googlesource.com/admin/repos/q/filter:plugins%252F
[supported]: https://www.gerritcodereview.com/support.html#supported-versions
[Contributions]: https://gerrit-review.googlesource.com/Documentation/index.html#_about_gerrit
[parent]: https://bugs.chromium.org/p/gerrit/issues/list?q=component%3Aplugins
[scripts]: https://gerrit.googlesource.com/gerrit-ci-scripts/+/refs/heads/master/jenkins/

[master]: https://gerrit-ci.gerritforge.com/view/Plugins-master/
[stable-3.1]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-3.1/
[stable-3.0]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-3.0/
[stable-2.16]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-2.16/

[account]: https://gerrit.googlesource.com/plugins/account/+/refs/heads/master/src/main/resources/Documentation
[admin-console]: https://gerrit.googlesource.com/plugins/admin-console/+/refs/heads/master/src/main/resources/Documentation
[analytics]: https://gerrit.googlesource.com/plugins/analytics/+/refs/heads/master/src/main/resources/Documentation
[analytics-wizard]: https://gerrit.googlesource.com/plugins/analytics-wizard
[audit-sl4j]: https://gerrit.googlesource.com/plugins/audit-sl4j/+/refs/heads/master/src/main/resources/Documentation
[automerger]: https://gerrit.googlesource.com/plugins/automerger/+/refs/heads/master/src/main/resources/Documentation
[autosubmitter]: https://gerrit.googlesource.com/plugins/autosubmitter
[avatars-external]: https://gerrit.googlesource.com/plugins/avatars-external/+/refs/heads/master/src/main/resources/Documentation
[avatars-gravatar]: https://gerrit.googlesource.com/plugins/avatars-gravatar/+/refs/heads/master/src/main/resources/Documentation
[batch]: https://gerrit.googlesource.com/plugins/batch/+/refs/heads/master/src/main/resources/Documentation
[TODO]: TODO
[emoticons]: https://gerrit.googlesource.com/plugins/emoticons/+/refs/heads/master/src/main/resources/Documentation
[TODO]: TODO
