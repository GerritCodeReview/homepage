---
title: "Gerrit Code Review - Plugins"
permalink: plugins.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## About this page

This page lists all the (non [core]) [plugins] known to the Gerrit project,
with their compatibility status across the [supported] version branches.
Some plugins might be missing from this page. [Contributions] to add them are welcome.

These plugins are made by different parties and maintained to varying degrees.
Therefore, the Gerrit project does not guarantee their reliability.
However many are reliable and valuable integrations across Gerrit deployments.

There are CI build [scripts] for every plugin.
Each script builds that plugin against all the branches it supports.
That CI is the public service offering the download of pre-built plugin jar files.

## Compatibility matrix

Below, each plugin name has a link to that plugin's documentation files, master version.
Each branch name links to the corresponding CI jobs view, for the current build status.

|                 | Branches |              |              |               |
|-----------------|----------|--------------|--------------|---------------|
| Plugins         | [master] | [stable-3.1] | [stable-3.0] | [stable-2.16] |
| [admin-console] | TODO     | TODO         | TODO         | TODO          |
| TODO            | TODO     | TODO         | TODO         | TODO          |

[core]: https://gerrit-review.googlesource.com/Documentation/config-plugins.html#core-plugins
[plugins]: https://gerrit-review.googlesource.com/admin/repos/q/filter:plugins%252F
[supported]: https://www.gerritcodereview.com/support.html#supported-versions
[Contributions]: https://gerrit-review.googlesource.com/Documentation/index.html#_about_gerrit
[scripts]: https://gerrit.googlesource.com/gerrit-ci-scripts/+/refs/heads/master/jenkins/

[master]: https://gerrit-ci.gerritforge.com/view/Plugins-master/
[stable-3.1]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-3.1/
[stable-3.0]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-3.0/
[stable-2.16]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-2.16/

[admin-console]: https://gerrit.googlesource.com/plugins/admin-console/+/refs/heads/master/src/main/resources/Documentation
