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

3. There are CI build [scripts] for every plugin.
   * Each script builds that plugin against all the branches it supports.
   * That CI is the public service offering the download of pre-built plugin jar files.

## Compatibility matrix

1. Below, each plugin name has a link to that plugin's documentation files, `master` version.
2. Each branch name links to the corresponding CI jobs view, for the current build status.
   * Plugin tests are currently not executed by the formal Gerrit project CI.
3. Plugins are either
   * compatible with the branch's Gerrit version (YES)
   * or incompatible (NO):

|                 | Branches |              |              |               |
|-----------------|----------|--------------|--------------|---------------|
| Plugin names:   | [master] | [stable-3.1] | [stable-3.0] | [stable-2.16] |
| [account]       | YES      | YES          | YES          | YES           |
| [admin-console] | YES      | YES          | YES          | YES           |
| [batch]         | YES      | NO           | NO           | YES           |
| [emoticons]     | NO       | NO           | NO           | YES           |

[core]: https://gerrit-review.googlesource.com/Documentation/config-plugins.html#core-plugins
[plugins]: https://gerrit-review.googlesource.com/admin/repos/q/filter:plugins%252F
[supported]: https://www.gerritcodereview.com/support.html#supported-versions
[Contributions]: https://gerrit-review.googlesource.com/Documentation/index.html#_about_gerrit
[scripts]: https://gerrit.googlesource.com/gerrit-ci-scripts/+/refs/heads/master/jenkins/

[master]: https://gerrit-ci.gerritforge.com/view/Plugins-master/
[stable-3.1]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-3.1/
[stable-3.0]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-3.0/
[stable-2.16]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-2.16/

[account]: https://gerrit.googlesource.com/plugins/account/+/refs/heads/master/src/main/resources/Documentation
[admin-console]: https://gerrit.googlesource.com/plugins/admin-console/+/refs/heads/master/src/main/resources/Documentation
[batch]: https://gerrit.googlesource.com/plugins/batch/+/refs/heads/master/src/main/resources/Documentation
[emoticons]: https://gerrit.googlesource.com/plugins/emoticons/+/refs/heads/master/src/main/resources/Documentation
