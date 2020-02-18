---
title: "Gerrit Code Review - Plugins"
permalink: template.html
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## About this page

1. This page lists all the (non [core]) [plugins] known to the Gerrit project.
   * -With their compatibility status across the [supported] version branches.
   * Some plugins might be missing from this page.
     * [Contributions] to add them are welcome, if needed.

2. These plugins are made by different parties and maintained to varying degrees.
   * Therefore, the Gerrit project does not guarantee their reliability.
   * However many are reliable and valuable integrations across Gerrit deployments.
   * There is a [parent] component for plugin-specific components/issues in Monorail.

3. There are CI build [scripts] for every plugin.
   * Each script builds that plugin against all the branches it supports.
   * Some plugins don't have branches but still support them, through their `master` branch.
   * That CI is the public service offering the download of pre-built plugin jar files.

## Compatibility matrix

1. Below, each plugin name has a link to that plugin's README page.
   * A corresponding plugin description summary table follows (first sentence, or NONE -if none).
     * [Contributions] to provide descriptions or update existing ones are welcome.
   * The last known plugin activity state and number of recent changes is also shown.

2. Each branch name links to the corresponding CI jobs view, for the current build status.
   * The latter last captured result shows in the CI column, next to that branch.
   * For formatting purposes, results are abbreviated to (e.g.) `S`UCCESS or `F`AILURE.
   * NONE shows if CI doesn't build a specific plugin branch or version yet.
     * [Contributions] to propose building those are also welcome if needed.
   * Plugin tests are currently not executed by the formal Gerrit project CI.

3. Plugins either
   * have a formal branch matching that Gerrit version (YES),
   * or don't have that branch (NO); again, versions may still build using `master`.
   * N/A shows across for inactive plugins.

4. Plugins compatibility with each Gerrit version depends on their current CI build results.
   * Those build results likely change over time; this matrix is their last snapshot.
   * Every once in a while, this page then has to be updated, [manually] for now.

[Contributions]: https://gerrit-review.googlesource.com/Documentation/index.html#_about_gerrit
[core]: https://gerrit-review.googlesource.com/Documentation/config-plugins.html#core-plugins
[manually]: https://www.gerritcodereview.com/publishing.html#updating-the-plugins-page
[parent]: https://bugs.chromium.org/p/gerrit/issues/list?q=component%3Aplugins
[plugins]: https://gerrit-review.googlesource.com/admin/repos/q/filter:plugins%252F
[scripts]: https://gerrit.googlesource.com/gerrit-ci-scripts/+/refs/heads/master/jenkins/
[supported]: https://www.gerritcodereview.com/support.html#supported-versions
