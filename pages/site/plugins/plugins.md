---
title: "Gerrit Code Review - Plugins"
permalink: plugins.html
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

[master]: https://gerrit-ci.gerritforge.com/view/Plugins-master/
[stable-3.1]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-3.1/
[stable-3.0]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-3.0/
[stable-2.16]: https://gerrit-ci.gerritforge.com/view/Plugins-stable-2.16/

|Name|State|Changes|Branch|CI|Branch|CI|Branch|CI|Branch|CI|
|----|-----|-------|------|--|------|--|------|--|------|--|
|    |     |       |[master]||[stable-3.1]||[stable-3.0]||[stable-2.16]||
|[account]|ACTIVE|1|YES|S|YES|S|YES|S|YES|S|
|[admin-console]|ACTIVE|26|YES|S|NO|S|YES|S|YES|S|
|[analytics]|ACTIVE|0|YES|S|YES|S|YES|S|YES|F|
|[analytics-wizard]|ACTIVE|0|YES|S|NO|NONE|NO|S|NO|S|
|[approval-extension]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[approver-annotator]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[audit-sl4j]|ACTIVE|0|YES|S|NO|S|YES|S|YES|F|
|[auth-htpasswd]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[auto-topic]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[automerger]|ACTIVE|2|YES|S|NO|NONE|NO|F|YES|S|
|[autosubmitter]|ACTIVE|0|YES|S|NO|NONE|YES|S|YES|F|
|[avatars-external]|ACTIVE|0|YES|S|NO|NONE|NO|F|NO|F|
|[avatars-gravatar]|ACTIVE|2|YES|S|NO|S|NO|F|YES|S|
|[avatars/external]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[avatars/gravatar]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[batch]|ACTIVE|7|YES|F|NO|NONE|NO|NONE|YES|S|
|[branch-network]|ACTIVE|0|YES|S|NO|NONE|NO|NONE|NO|NONE|
|[cfoauth]|ACTIVE|0|YES|S|NO|S|NO|S|NO|S|
|[change-head]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[change-labels]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[changemessage]|ACTIVE|27|YES|S|NO|NONE|YES|S|YES|S|
|[checks]|ACTIVE|47|YES|S|YES|S|NO|NONE|NO|NONE|
|[cloud-notifications]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[codemirror-editor]|ACTIVE|2|YES|S|NO|NONE|NO|NONE|NO|NONE|
|[commit-message-length-validator]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[commit-validator-sample]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[cookbook-plugin]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[copyright]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[delete-project]|ACTIVE|20|YES|NONE|YES|NONE|YES|NONE|YES|S|
|[donation-button]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[download-commands]|ACTIVE|5|YES|NONE|NO|NONE|NO|NONE|YES|NONE|
|[egit]|ACTIVE|0|YES|S|NO|NONE|NO|S|NO|S|
|[emoticons]|ACTIVE|9|YES|NONE|NO|NONE|NO|NONE|YES|S|
|[events]|ACTIVE|0|YES|S|NO|S|NO|S|NO|S|
|[events-log]|ACTIVE|39|YES|S|YES|S|YES|S|YES|S|
|[evict-cache]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[examples]|ACTIVE|1|YES|S|YES|S|YES|S|YES|S|
|[find-owners]|ACTIVE|4|YES|F|NO|NONE|NO|NONE|YES|S|
|[force-draft]|ACTIVE|1|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[gc-conductor]|ACTIVE|31|YES|S|NO|NONE|YES|S|YES|S|
|[gerrit-support]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[gitblit]|ACTIVE|0|YES|S|NO|NONE|NO|NONE|NO|NONE|
|[gitgroups]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[github]|ACTIVE|0|YES|S|YES|S|YES|S|YES|F|
|[github-groups]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[github-profile]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[github-pullrequest]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[github-replication]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[github-webhooks]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[gitiles]|ACTIVE|16|YES|NONE|YES|NONE|YES|NONE|YES|S|
|[go-import]|ACTIVE|31|YES|S|NO|NONE|YES|S|YES|S|
|[google-apps-group]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[healthcheck]|ACTIVE|5|YES|S|YES|S|YES|S|YES|S|
|[heartbeat]|ACTIVE|38|YES|S|YES|S|YES|S|YES|S|
|[helloworld]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[hide-actions]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[high-availability]|ACTIVE|48|YES|S|YES|S|YES|S|YES|S|
|[hooks]|ACTIVE|0|YES|NONE|YES|NONE|YES|NONE|YES|NONE|
|[hooks-audit]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[hooks-bugzilla]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[hooks-its]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[hooks-jira]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[hooks-rtc]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[imagare]|ACTIVE|1|YES|F|NO|NONE|NO|NONE|YES|S|
|[image-diff]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[importer]|ACTIVE|3|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[its-base]|ACTIVE|2|YES|F|YES|NONE|YES|S|YES|F|
|[its-bugzilla]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|YES|F|
|[its-github]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[its-jira]|ACTIVE|0|YES|S|YES|S|YES|S|YES|S|
|[its-phabricator]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|YES|NONE|
|[its-redmine]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[its-rtc]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[its-storyboard]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[javamelody]|ACTIVE|32|YES|S|NO|S|YES|S|YES|S|
|[kafka-events]|ACTIVE|6|YES|S|YES|S|YES|S|YES|F|
|[labelui]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[lfs]|ACTIVE|31|YES|S|NO|NONE|YES|S|YES|S|
|[lfs-storage-fs]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[lfs-storage-s3]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[log-level]|ACTIVE|26|YES|S|NO|NONE|YES|S|YES|S|
|[login-redirect]|ACTIVE|0|YES|S|NO|S|NO|S|NO|S|
|[maintainer]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[manifest]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[manifest-subscription]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[menuextender]|ACTIVE|0|YES|S|NO|NONE|NO|S|NO|S|
|[messageoftheday]|ACTIVE|27|YES|S|NO|NONE|YES|S|YES|S|
|[metrics-reporter-cloudwatch]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[metrics-reporter-elasticsearch]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[metrics-reporter-graphite]|ACTIVE|0|YES|S|NO|NONE|NO|S|NO|S|
|[metrics-reporter-jmx]|ACTIVE|5|YES|S|NO|NONE|NO|S|NO|S|
|[metrics-reporter-prometheus]|ACTIVE|8|YES|S|NO|S|NO|S|YES|S|
|[motd]|ACTIVE|0|YES|S|NO|NONE|NO|NONE|NO|NONE|
|[multi-master]|ACTIVE|1|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[multi-site]|ACTIVE|98|YES|S|YES|S|YES|S|YES|S|
|[oauth]|ACTIVE|46|YES|S|NO|S|YES|S|YES|S|
|[out-of-the-box]|ACTIVE|0|YES|S|NO|S|NO|S|NO|S|
|[owners]|ACTIVE|8|YES|S|YES|S|YES|S|YES|S|
|[plugin-manager]|ACTIVE|4|YES|NONE|NO|NONE|NO|NONE|YES|F|
|[project-download-commands]|ACTIVE|1|YES|S|NO|NONE|NO|NONE|NO|NONE|
|[project-group-structure]|ACTIVE|30|YES|S|NO|NONE|YES|S|YES|S|
|[prolog-submit-rules]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[pull-replication]|ACTIVE|7|YES|F|NO|S|NO|NONE|NO|NONE|
|[push-pull-replication]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[quickstart]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[quota]|ACTIVE|27|YES|S|NO|NONE|YES|S|YES|S|
|[rabbitmq]|ACTIVE|0|YES|S|YES|S|YES|S|YES|S|
|[rate-limiter]|ACTIVE|42|YES|S|YES|S|YES|S|YES|S|
|[readonly]|ACTIVE|40|YES|F|YES|S|YES|S|YES|S|
|[ref-protection]|ACTIVE|0|YES|S|NO|S|NO|F|YES|S|
|[reject-private-submit]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[rename-project]|ACTIVE|31|YES|S|YES|S|YES|S|YES|S|
|[reparent]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[replication]|ACTIVE|30|YES|NONE|YES|NONE|YES|NONE|YES|NONE|
|[replication-status]|ACTIVE|1|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[repository-usage]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[review-strategy]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[reviewassistant]|ACTIVE|12|YES|F|NO|NONE|NO|NONE|YES|S|
|[reviewers]|ACTIVE|28|YES|S|NO|NONE|YES|S|YES|S|
|[reviewers-by-blame]|ACTIVE|0|YES|S|NO|NONE|YES|S|YES|S|
|[reviewnotes]|ACTIVE|4|YES|NONE|YES|NONE|YES|NONE|YES|NONE|
|[saml]|ACTIVE|0|YES|S|NO|NONE|NO|NONE|YES|S|
|[scripting-rules]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[scripting/groovy-provider]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[scripting/scala-provider]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[scripts]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[secure-config]|ACTIVE|0|YES|S|YES|S|YES|S|YES|S|
|[server-config]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[server-log-viewer]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[serviceuser]|ACTIVE|43|YES|S|YES|S|YES|S|YES|S|
|[shutdown]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[simple-submit-rules]|ACTIVE|1|YES|S|NO|NONE|NO|NONE|YES|S|
|[singleusergroup]|ACTIVE|0|YES|NONE|NO|NONE|YES|NONE|YES|NONE|
|[slack-integration]|ACTIVE|23|YES|S|NO|S|YES|S|YES|S|
|[supermanifest]|ACTIVE|0|YES|S|NO|NONE|NO|NONE|NO|NONE|
|[sync-events]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[sync-index]|READ_ONLY|0|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|[task]|ACTIVE|21|YES|S|NO|NONE|YES|S|YES|S|
|[uploadvalidator]|ACTIVE|26|YES|S|NO|S|YES|S|YES|S|
|[verify-status]|ACTIVE|14|YES|F|NO|NONE|NO|NONE|YES|S|
|[webhooks]|ACTIVE|14|YES|NONE|NO|NONE|YES|NONE|YES|S|
|[websession-broker]|ACTIVE|6|YES|S|YES|S|YES|S|NO|NONE|
|[websession-flatfile]|ACTIVE|1|YES|S|NO|S|NO|S|NO|S|
|[wip]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[wmf-fixshadowuser]|ACTIVE|0|YES|NONE|NO|NONE|NO|NONE|NO|NONE|
|[x-docs]|ACTIVE|1|YES|F|NO|NONE|NO|NONE|NO|NONE|
|[zookeeper-refdb]|ACTIVE|0|NO|NONE|NO|NONE|NO|NONE|NO|NONE|
|[zuul]|ACTIVE|0|YES|F|NO|NONE|NO|NONE|NO|S|
|[zuul-status]|ACTIVE|0|YES|S|NO|NONE|YES|NONE|YES|S|

## Plugin descriptions

|Name|Description|
|----|-----------|
|[account]|Plugin to expose a self-service API and UX to manage accounts and associated personal information|
|[admin-console]|Provides information via SSH commands to Gerrit Administrators|
|[analytics]|Plugin to aggregate information from Gerrit projects and reviews and expose them through REST and SSH API|
|[analytics-wizard]|Wizard to provision a new GerritAnalytics stack|
|[approval-extension]|Small example plug-in demoing extension points for manipulating approvals|
|[approver-annotator]|NONE|
|[audit-sl4j]|Plugin for logging audit events using a SLF4J appender|
|[auth-htpasswd]|Plugin for Apache htpasswd based authentication|
|[auto-topic]|NONE|
|[automerger]|NONE|
|[autosubmitter]|A plugin that takes care of automatically submitting changes when all approvals and preconditions are satisfied|
|[avatars-external]|Enables to set a custom URL to load avatars from|
|[avatars-gravatar]|Plugin to display user icons from Gravatar|
|[avatars/external]|DEPRECATED|
|[avatars/gravatar]|DEPRECATED|
|[batch]|The batch plugin provides a mechanism for building and|
|[branch-network]|Plug-in to display and navigate Git branches in a HTML5 canvas network|
|[cfoauth]|Plugin to authenticate with a CloudFoundry User Account and Authentication server using OAuth2 protocol|
|[change-head]|[DEPRECATED] Shift what the HEAD symbolic-ref points to|
|[change-labels]|NONE|
|[changemessage]|This plugin allows to display a static info message on the change screen|
|[checks]|This plugin provides a REST API and UI extensions for integrating CI systems with Gerrit|
|[cloud-notifications]|A plugin to obtain push event notifications through Firebase Cloud Messaging (FCM)|
|[codemirror-editor]|CodeMirror plugin for PolyGerrit|
|[commit-message-length-validator]|Plugin to validate that commit messages conform to length limits|
|[commit-validator-sample]|Sample validator to accept, refuse or provide warnings on Git commit changes during push|
|[cookbook-plugin]|Examples of plugin API usage|
|[copyright]|WIP: Copyright scanner to require qualified review when needed|
|[delete-project]|A plugin which allows projects to be deleted from Gerrit via an SSH command|
|[donation-button]|Make a donation button to Shawn Pearce Memorial Fund|
|[download-commands]|Adds the standard download schemes and commands|
|[egit]|This plugin provides extensions for easier usage with EGit|
|[emoticons]|Plugin that allows users to see emoticons in comments as|
|[events]|The events plugin adds a stream events API which parallels|
|[events-log]|This plugin listens to stream events and stores them in a database. The events can be retrieved through REST API|
|[evict-cache]|[DEPRECATED]Allows to synchronize the eviction of caches between two Gerrit instances sharing the same repositories and database|
|[examples]|Collection of example plugins for Gerrit Code Review|
|[find-owners]|Plugin to check for Android and Chromium style OWNERS approval before submit and find owners for a revision|
|[force-draft]|Provides an ssh command to force a change or patch set to draft status|
|[gc-conductor]|This plugin provides an automated way of detecting, managing and cleaning up (garbage collecting) the 'dirty' repositories in a Gerrit instance|
|[gerrit-support]|Plugin to collect information on Gerrit Code Review setup for requesting support|
|[gitblit]|GitBlit code-viewer plug-in with SSO and Security Access Control|
|[gitgroups]|GroupBackend using text files stored in Git|
|[github]|Plugin to integrate with GitHub: replication, pull-request to Change-Sets|
|[github-groups]|Group backend implementation to use GitHub Organisations and Teams as Gerrit Groups|
|[github-profile]|GitHub-Profile integration for migrating and synchronising your GitHub e-mail address and SSH Keys with Gerrit|
|[github-pullrequest]|Import existing GitHub Pull Requests as Gerrit Changes and Patch-Sets with one click|
|[github-replication]|Replication wizard for importing and configuring GitHub repos as Gerrit slaves replicas with a single click|
|[github-webhooks]|Expose Gerrit automation actions (e.g. importing a pull request) as GitHub hooks|
|[gitiles]|Plugin running Gitiles alongside a Gerrit server|
|[go-import]|NONE|
|[google-apps-group]|Sample group backend plugin using Google Groups on a Google Apps domain|
|[healthcheck]|Gerrit plugin for triggering a general configuration and runtime health check|
|[heartbeat]|Plugin that sends heartbeat stream event|
|[helloworld]|Template plugin that adds new SSH commands to a server|
|[hide-actions]|Plugin that allows to hide UI actions by configuration|
|[high-availability]|Synchronize eviction of caches, secondary indexes and stream events between two Gerrit instances sharing the same git repositories and database|
|[hooks]|Server-side hooks executed on Gerrit events|
|[hooks-audit]|Plugin(s) to enable auditing of Gerrit admin and user activity to an external logging system|
|[hooks-bugzilla]|Deprecated. Please use plugins/its-bugzilla instead|
|[hooks-its]|Deprecated. Please use plugins/its-base instead|
|[hooks-jira]|Deprecated. Please use plugins/its-jira instead|
|[hooks-rtc]|Deprecated. Please use plugins/its-rtc instead|
|[imagare]|Plugin allows Gerrit users to upload and share images|
|[image-diff]|An enhanced image diff plugin for PolyGerrit|
|[importer]|Plugin to import projects from one Gerrit server into another Gerrit server|
|[its-base]|Plugin base for issue tracking systems|
|[its-bugzilla]|Plugin to integrate with Bugzilla|
|[its-github]|Plugin to integrate with GitHub Issue Tracker|
|[its-jira]|Plugin to integrate with Atlassian JIRA|
|[its-phabricator]|Plugin to integrate with Phabricator|
|[its-redmine]|Plugin to integrate with Redmine|
|[its-rtc]|Plugin to integrate with IBM Rational Team Concert|
|[its-storyboard]|Plugin to integrate with the Storyboard Issue Tracking System|
|[javamelody]|Plugin to monitor a Gerrit server with JavaMelody|
|[kafka-events]|Gerrit event producer for Apache Kafka|
|[labelui]|The labelui plugin allows users to configure a different control for displaying the labels/approvals on the change screen|
|[lfs]|LFS plugin storing large objects|
|[lfs-storage-fs]|DEPRECATED: Use the plugins/lfs|
|[lfs-storage-s3]|DEPRECATED: Use the plugins/lfs|
|[log-level]|Plugin to allow an administrator to persist configured log levels across restarts|
|[login-redirect]|Plugin to redirect anonymous users to the login form|
|[maintainer]|NONE|
|[manifest]|The manifest plugin provides server side utilities to|
|[manifest-subscription]|This plugin allows users to monitor git-repo manifests in manifest repositories and generate rev-specific manifests (similar to "repo manifest -o") and store them to a separate git repository|
|[menuextender]|Plugin that allows Gerrit administrators to configure additional menu entries from the WebUI|
|[messageoftheday]|NONE|
|[metrics-reporter-cloudwatch]|This plugin reports Gerrit metrics to AWS Cloudwatch Service|
|[metrics-reporter-elasticsearch]|This plugin reports Gerrit metrics to ElasticSearch Indexes|
|[metrics-reporter-graphite]|This plugin reports Gerrit metrics to Graphite|
|[metrics-reporter-jmx]|This plugin exposes Gerrit metrics as JMX resources|
|[metrics-reporter-prometheus]|This plugin exposes Gerrit metrics to Prometheus (https://prometheus.io/)|
|[motd]|Plugin that provides messages to users on fetch/pull/clone|
|[multi-master]|Plugin(s) to enable Gerrrit multi-master operation|
|[multi-site]|Multi-site support for Gerrit Code Review|
|[oauth]|OAuth2 provider plugin. Multiple providers are currently supported:|
|[out-of-the-box]|Plugin to provide an out-of-the-box redirect for a fresh Gerrit install|
|[owners]|Provides a Prolog predicate add_owner_approval/3 that appends label('Owner-Approval', need(_)) to a provided list|
|[plugin-manager]|One plugin to rule them all: install new plugins from Gerrit GUI|
|[project-download-commands]|Plugin that adds support for project specific download commands|
|[project-group-structure]|This plugin enforce a project group structure and restrict project creation within this structure to project group owners only|
|[prolog-submit-rules]|NONE|
|[pull-replication]|Mirror repos from other servers using the Git protocol|
|[push-pull-replication]|Alternative Gerrit replication plugin that uses both push and pull operations as replication logic|
|[quickstart]|Gerrit plugin for providing a Quck-start configuration during the init phase|
|[quota]|This plugin allows to enforce quotas in Gerrit|
|[rabbitmq]|Publishes Gerrit events to RabbitMQ|
|[rate-limiter]|Allows to enforce rate limits in Gerrit|
|[readonly]|A plugin to make Gerrit run in read-only mode|
|[ref-protection]|Creates backups of refs that are deleted or non-fast-forward updated|
|[reject-private-submit]|Reject submission (merging) of private changes|
|[rename-project]|A plugin which allows projects to be renamed from Gerrit via an SSH command|
|[reparent]|Plugin that provides a self-service for reparenting projects|
|[replication]|Copies to other servers using the Git protocol|
|[replication-status]|Record and display the repository's replication status without having to dig into the Gerrit replication_log|
|[repository-usage]|Searches repositories for submodules and manifest files and saves references to a database|
|[review-strategy]|Provide configurations for custom Gerrit review strategies|
|[reviewassistant]|Gives advice to reviewers on how the review should be|
|[reviewers]|A plugin that allows adding default reviewers to a change|
|[reviewers-by-blame]|A plugin that allows to automatically add reviewers to a change from the git blame computation on the changed files. It will add the users as reviewer that authored most of the lines touched by the change, since these users should be familiar with the code and can most likely review the change|
|[reviewnotes]|Annotates merged commits using notes on refs/notes/review|
|[saml]|Plugin for Gerrit authentication with a SAML provider|
|[scripting-rules]|NONE|
|[scripting/groovy-provider]|Allows the load Gerrit plugins implemented as Groovy scripts|
|[scripting/scala-provider]|Allows the load Gerrit plugins implemented as Scala scripts|
|[scripts]|Scripting plugins for providing simple and useful extensions on top of Gerrit|
|[secure-config]|Plugin to encrypt the values of secure.config|
|[server-config]|This plugin enables access (download and upload) to the server config|
|[server-log-viewer]|Displays $site_path/logs through a web browser|
|[serviceuser]|This plugin allows to create service users in Gerrit|
|[shutdown]|Gerrit plugin to provide a graceful shutdown via RESTful API (intended for Windows Service integration)|
|[simple-submit-rules]|NONE|
|[singleusergroup]|GroupBackend enabling users to be directly added to access rules|
|[slack-integration]|Allows for the publishing of certain Gerrit events to a configured Slack Webhook URL|
|[supermanifest]|Update superproject in response to manifest changes|
|[sync-events]|[DEPRECATED]Allows to share stream events between two Gerrit instances|
|[sync-index]|[DEPRECATED]Allows to synchronize secondary indexes between between two Gerrit instances sharing the same git repositories and database|
|[task]|The task plugin provides a mechanism to manage tasks which|
|[uploadvalidator]|This plugin allows to configure upload validations per project|
|[verify-status]|Verification status plugin to visualize different jobs status that contributed to verify vote|
|[webhooks]|This plugin allows to propagate Gerrit events to remote http endpoints|
|[websession-broker]|Plugs into the builtin Gerrit WebSession implementation and broadcast websessions to an external broker|
|[websession-flatfile]|Replaces the builtin Gerrit WebSession implementation with one that uses a flat file based cache|
|[wip]|Plugin that allows to mark changes as Work In Progress|
|[wmf-fixshadowuser]|NONE|
|[x-docs]|This plugin serves Markdown project documentation as HTML pages|
|[zookeeper-refdb]|Zookeeper-backed reference database plugin|
|[zuul]|Gerrit Zuul Plugin|
|[zuul-status]|Displays zuul status on PolyGerrit change|

[account]: https://gerrit.googlesource.com/plugins/account
[admin-console]: https://gerrit.googlesource.com/plugins/admin-console
[analytics]: https://gerrit.googlesource.com/plugins/analytics
[analytics-wizard]: https://gerrit.googlesource.com/plugins/analytics-wizard
[approval-extension]: https://gerrit.googlesource.com/plugins/approval-extension
[approver-annotator]: https://gerrit.googlesource.com/plugins/approver-annotator
[audit-sl4j]: https://gerrit.googlesource.com/plugins/audit-sl4j
[auth-htpasswd]: https://gerrit.googlesource.com/plugins/auth-htpasswd
[auto-topic]: https://gerrit.googlesource.com/plugins/auto-topic
[automerger]: https://gerrit.googlesource.com/plugins/automerger
[autosubmitter]: https://gerrit.googlesource.com/plugins/autosubmitter
[avatars-external]: https://gerrit.googlesource.com/plugins/avatars-external
[avatars-gravatar]: https://gerrit.googlesource.com/plugins/avatars-gravatar
[avatars/external]: https://gerrit.googlesource.com/plugins/avatars/external
[avatars/gravatar]: https://gerrit.googlesource.com/plugins/avatars/gravatar
[batch]: https://gerrit.googlesource.com/plugins/batch
[branch-network]: https://gerrit.googlesource.com/plugins/branch-network
[cfoauth]: https://gerrit.googlesource.com/plugins/cfoauth
[change-head]: https://gerrit.googlesource.com/plugins/change-head
[change-labels]: https://gerrit.googlesource.com/plugins/change-labels
[changemessage]: https://gerrit.googlesource.com/plugins/changemessage
[checks]: https://gerrit.googlesource.com/plugins/checks
[cloud-notifications]: https://gerrit.googlesource.com/plugins/cloud-notifications
[codemirror-editor]: https://gerrit.googlesource.com/plugins/codemirror-editor
[commit-message-length-validator]: https://gerrit.googlesource.com/plugins/commit-message-length-validator
[commit-validator-sample]: https://gerrit.googlesource.com/plugins/commit-validator-sample
[cookbook-plugin]: https://gerrit.googlesource.com/plugins/cookbook-plugin
[copyright]: https://gerrit.googlesource.com/plugins/copyright
[delete-project]: https://gerrit.googlesource.com/plugins/delete-project
[donation-button]: https://gerrit.googlesource.com/plugins/donation-button
[download-commands]: https://gerrit.googlesource.com/plugins/download-commands
[egit]: https://gerrit.googlesource.com/plugins/egit
[emoticons]: https://gerrit.googlesource.com/plugins/emoticons
[events]: https://gerrit.googlesource.com/plugins/events
[events-log]: https://gerrit.googlesource.com/plugins/events-log
[evict-cache]: https://gerrit.googlesource.com/plugins/evict-cache
[examples]: https://gerrit.googlesource.com/plugins/examples
[find-owners]: https://gerrit.googlesource.com/plugins/find-owners
[force-draft]: https://gerrit.googlesource.com/plugins/force-draft
[gc-conductor]: https://gerrit.googlesource.com/plugins/gc-conductor
[gerrit-support]: https://gerrit.googlesource.com/plugins/gerrit-support
[gitblit]: https://gerrit.googlesource.com/plugins/gitblit
[gitgroups]: https://gerrit.googlesource.com/plugins/gitgroups
[github]: https://gerrit.googlesource.com/plugins/github
[github-groups]: https://gerrit.googlesource.com/plugins/github-groups
[github-profile]: https://gerrit.googlesource.com/plugins/github-profile
[github-pullrequest]: https://gerrit.googlesource.com/plugins/github-pullrequest
[github-replication]: https://gerrit.googlesource.com/plugins/github-replication
[github-webhooks]: https://gerrit.googlesource.com/plugins/github-webhooks
[gitiles]: https://gerrit.googlesource.com/plugins/gitiles
[go-import]: https://gerrit.googlesource.com/plugins/go-import
[google-apps-group]: https://gerrit.googlesource.com/plugins/google-apps-group
[healthcheck]: https://gerrit.googlesource.com/plugins/healthcheck
[heartbeat]: https://gerrit.googlesource.com/plugins/heartbeat
[helloworld]: https://gerrit.googlesource.com/plugins/helloworld
[hide-actions]: https://gerrit.googlesource.com/plugins/hide-actions
[high-availability]: https://gerrit.googlesource.com/plugins/high-availability
[hooks]: https://gerrit.googlesource.com/plugins/hooks
[hooks-audit]: https://gerrit.googlesource.com/plugins/hooks-audit
[hooks-bugzilla]: https://gerrit.googlesource.com/plugins/hooks-bugzilla
[hooks-its]: https://gerrit.googlesource.com/plugins/hooks-its
[hooks-jira]: https://gerrit.googlesource.com/plugins/hooks-jira
[hooks-rtc]: https://gerrit.googlesource.com/plugins/hooks-rtc
[imagare]: https://gerrit.googlesource.com/plugins/imagare
[image-diff]: https://gerrit.googlesource.com/plugins/image-diff
[importer]: https://gerrit.googlesource.com/plugins/importer
[its-base]: https://gerrit.googlesource.com/plugins/its-base
[its-bugzilla]: https://gerrit.googlesource.com/plugins/its-bugzilla
[its-github]: https://gerrit.googlesource.com/plugins/its-github
[its-jira]: https://gerrit.googlesource.com/plugins/its-jira
[its-phabricator]: https://gerrit.googlesource.com/plugins/its-phabricator
[its-redmine]: https://gerrit.googlesource.com/plugins/its-redmine
[its-rtc]: https://gerrit.googlesource.com/plugins/its-rtc
[its-storyboard]: https://gerrit.googlesource.com/plugins/its-storyboard
[javamelody]: https://gerrit.googlesource.com/plugins/javamelody
[kafka-events]: https://gerrit.googlesource.com/plugins/kafka-events
[labelui]: https://gerrit.googlesource.com/plugins/labelui
[lfs]: https://gerrit.googlesource.com/plugins/lfs
[lfs-storage-fs]: https://gerrit.googlesource.com/plugins/lfs-storage-fs
[lfs-storage-s3]: https://gerrit.googlesource.com/plugins/lfs-storage-s3
[log-level]: https://gerrit.googlesource.com/plugins/log-level
[login-redirect]: https://gerrit.googlesource.com/plugins/login-redirect
[maintainer]: https://gerrit.googlesource.com/plugins/maintainer
[manifest]: https://gerrit.googlesource.com/plugins/manifest
[manifest-subscription]: https://gerrit.googlesource.com/plugins/manifest-subscription
[menuextender]: https://gerrit.googlesource.com/plugins/menuextender
[messageoftheday]: https://gerrit.googlesource.com/plugins/messageoftheday
[metrics-reporter-cloudwatch]: https://gerrit.googlesource.com/plugins/metrics-reporter-cloudwatch
[metrics-reporter-elasticsearch]: https://gerrit.googlesource.com/plugins/metrics-reporter-elasticsearch
[metrics-reporter-graphite]: https://gerrit.googlesource.com/plugins/metrics-reporter-graphite
[metrics-reporter-jmx]: https://gerrit.googlesource.com/plugins/metrics-reporter-jmx
[metrics-reporter-prometheus]: https://gerrit.googlesource.com/plugins/metrics-reporter-prometheus
[motd]: https://gerrit.googlesource.com/plugins/motd
[multi-master]: https://gerrit.googlesource.com/plugins/multi-master
[multi-site]: https://gerrit.googlesource.com/plugins/multi-site
[oauth]: https://gerrit.googlesource.com/plugins/oauth
[out-of-the-box]: https://gerrit.googlesource.com/plugins/out-of-the-box
[owners]: https://gerrit.googlesource.com/plugins/owners
[plugin-manager]: https://gerrit.googlesource.com/plugins/plugin-manager
[project-download-commands]: https://gerrit.googlesource.com/plugins/project-download-commands
[project-group-structure]: https://gerrit.googlesource.com/plugins/project-group-structure
[prolog-submit-rules]: https://gerrit.googlesource.com/plugins/prolog-submit-rules
[pull-replication]: https://gerrit.googlesource.com/plugins/pull-replication
[push-pull-replication]: https://gerrit.googlesource.com/plugins/push-pull-replication
[quickstart]: https://gerrit.googlesource.com/plugins/quickstart
[quota]: https://gerrit.googlesource.com/plugins/quota
[rabbitmq]: https://gerrit.googlesource.com/plugins/rabbitmq
[rate-limiter]: https://gerrit.googlesource.com/plugins/rate-limiter
[readonly]: https://gerrit.googlesource.com/plugins/readonly
[ref-protection]: https://gerrit.googlesource.com/plugins/ref-protection
[reject-private-submit]: https://gerrit.googlesource.com/plugins/reject-private-submit
[rename-project]: https://gerrit.googlesource.com/plugins/rename-project
[reparent]: https://gerrit.googlesource.com/plugins/reparent
[replication]: https://gerrit.googlesource.com/plugins/replication
[replication-status]: https://gerrit.googlesource.com/plugins/replication-status
[repository-usage]: https://gerrit.googlesource.com/plugins/repository-usage
[review-strategy]: https://gerrit.googlesource.com/plugins/review-strategy
[reviewassistant]: https://gerrit.googlesource.com/plugins/reviewassistant
[reviewers]: https://gerrit.googlesource.com/plugins/reviewers
[reviewers-by-blame]: https://gerrit.googlesource.com/plugins/reviewers-by-blame
[reviewnotes]: https://gerrit.googlesource.com/plugins/reviewnotes
[saml]: https://gerrit.googlesource.com/plugins/saml
[scripting-rules]: https://gerrit.googlesource.com/plugins/scripting-rules
[scripting/groovy-provider]: https://gerrit.googlesource.com/plugins/scripting/groovy-provider
[scripting/scala-provider]: https://gerrit.googlesource.com/plugins/scripting/scala-provider
[scripts]: https://gerrit.googlesource.com/plugins/scripts
[secure-config]: https://gerrit.googlesource.com/plugins/secure-config
[server-config]: https://gerrit.googlesource.com/plugins/server-config
[server-log-viewer]: https://gerrit.googlesource.com/plugins/server-log-viewer
[serviceuser]: https://gerrit.googlesource.com/plugins/serviceuser
[shutdown]: https://gerrit.googlesource.com/plugins/shutdown
[simple-submit-rules]: https://gerrit.googlesource.com/plugins/simple-submit-rules
[singleusergroup]: https://gerrit.googlesource.com/plugins/singleusergroup
[slack-integration]: https://gerrit.googlesource.com/plugins/slack-integration
[supermanifest]: https://gerrit.googlesource.com/plugins/supermanifest
[sync-events]: https://gerrit.googlesource.com/plugins/sync-events
[sync-index]: https://gerrit.googlesource.com/plugins/sync-index
[task]: https://gerrit.googlesource.com/plugins/task
[uploadvalidator]: https://gerrit.googlesource.com/plugins/uploadvalidator
[verify-status]: https://gerrit.googlesource.com/plugins/verify-status
[webhooks]: https://gerrit.googlesource.com/plugins/webhooks
[websession-broker]: https://gerrit.googlesource.com/plugins/websession-broker
[websession-flatfile]: https://gerrit.googlesource.com/plugins/websession-flatfile
[wip]: https://gerrit.googlesource.com/plugins/wip
[wmf-fixshadowuser]: https://gerrit.googlesource.com/plugins/wmf-fixshadowuser
[x-docs]: https://gerrit.googlesource.com/plugins/x-docs
[zookeeper-refdb]: https://gerrit.googlesource.com/plugins/zookeeper-refdb
[zuul]: https://gerrit.googlesource.com/plugins/zuul
[zuul-status]: https://gerrit.googlesource.com/plugins/zuul-status
