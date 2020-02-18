---
title: "Gerrit Code Review - Plugins"
permalink: template.html
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

[core]: https://gerrit-review.googlesource.com/Documentation/config-plugins.html#core-plugins
[plugins]: https://gerrit-review.googlesource.com/admin/repos/q/filter:plugins%252F
[supported]: https://www.gerritcodereview.com/support.html#supported-versions
[Contributions]: https://gerrit-review.googlesource.com/Documentation/index.html#_about_gerrit
[parent]: https://bugs.chromium.org/p/gerrit/issues/list?q=component%3Aplugins
[scripts]: https://gerrit.googlesource.com/gerrit-ci-scripts/+/refs/heads/master/jenkins/
