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

|Name|State|Changes|Description|        |            |            |             |
|----|-----|-------|-----------|--------|------------|------------|-------------|
|    |     |       |           |[master]|[stable-3.1]|[stable-3.0]|[stable-2.16]|
|[account]|ACTIVE|1|Plugin to expose a self-service API and UX to manage accounts and associated personal information.|YES|YES|YES|YES|
|[admin-console]|ACTIVE|26|Provides information via SSH commands to Gerrit Administrators.|YES|NO|YES|YES|
|[analytics]|ACTIVE|0|Plugin to aggregate information from Gerrit projects and reviews and expose them through REST and SSH API.|YES|YES|YES|YES|
|[analytics-wizard]|ACTIVE|0|Wizard to provision a new GerritAnalytics stack|YES|NO|NO|NO|
|[approval-extension]|ACTIVE|0|Small example plug-in demoing extension points for manipulating approvals.|NO|NO|NO|NO|
|[approver-annotator]|ACTIVE|0|NONE|NO|NO|NO|NO|
|[audit-sl4j]|ACTIVE|0|Plugin for logging audit events using a SLF4J appender|YES|NO|YES|YES|
|[auth-htpasswd]|ACTIVE|0|Plugin for Apache htpasswd based authentication.|NO|NO|NO|NO|
|[auto-topic]|ACTIVE|0|NONE|NO|NO|NO|NO|
|[automerger]|ACTIVE|2|NONE|YES|NO|NO|YES|
|[autosubmitter]|ACTIVE|0|A plugin that takes care of automatically submitting changes when all approvals and preconditions are satisfied.|YES|NO|YES|YES|
|[avatars-external]|ACTIVE|0|Enables to set a custom URL to load avatars from.|YES|NO|NO|NO|
|[avatars-gravatar]|ACTIVE|2|Plugin to display user icons from Gravatar.|YES|NO|NO|YES|
|[avatars/external]|READ_ONLY|0|DEPRECATED|N/A|N/A|N/A|N/A|
|[avatars/gravatar]|READ_ONLY|0|DEPRECATED|N/A|N/A|N/A|N/A|
|[batch]|ACTIVE|7|The batch plugin provides a mechanism for building and|YES|NO|NO|YES|
|[branch-network]|ACTIVE|0|Plug-in to display and navigate Git branches in a HTML5 canvas network|YES|NO|NO|NO|
|[cfoauth]|ACTIVE|0|Plugin to authenticate with a CloudFoundry User Account and Authentication server using OAuth2 protocol.|YES|NO|NO|NO|
|[change-head]|READ_ONLY|0|[DEPRECATED] Shift what the HEAD symbolic-ref points to.|N/A|N/A|N/A|N/A|
|[change-labels]|ACTIVE|0|NONE|NO|NO|NO|NO|
|[changemessage]|ACTIVE|27|This plugin allows to display a static info message on the change screen.|YES|NO|YES|YES|
|[checks]|ACTIVE|46|This plugin provides a REST API and UI extensions for integrating CI systems with Gerrit.|YES|YES|NO|NO|
|[cloud-notifications]|ACTIVE|0|A plugin to obtain push event notifications through Firebase Cloud Messaging (FCM).|YES|NO|NO|NO|
|[codemirror-editor]|ACTIVE|2|CodeMirror plugin for PolyGerrit|YES|NO|NO|NO|
|[commit-message-length-validator]|ACTIVE|0|Plugin to validate that commit messages conform to length limits.|YES|NO|NO|NO|
|[commit-validator-sample]|ACTIVE|0|Sample validator to accept, refuse or provide warnings on Git commit changes during push.|YES|NO|NO|NO|
|[cookbook-plugin]|ACTIVE|0|Examples of plugin API usage.|YES|NO|NO|NO|
|[copyright]|ACTIVE|0|WIP: Copyright scanner to require qualified review when needed|YES|NO|NO|NO|
|[delete-project]|ACTIVE|20|A plugin which allows projects to be deleted from Gerrit via an SSH command|YES|YES|YES|YES|
|[donation-button]|ACTIVE|0|Make a donation button to Shawn Pearce Memorial Fund|YES|NO|NO|NO|
|[download-commands]|ACTIVE|5|Adds the standard download schemes and commands.|YES|NO|NO|YES|
|[egit]|ACTIVE|0|This plugin provides extensions for easier usage with EGit.|YES|NO|NO|NO|
|[emoticons]|ACTIVE|9|Plugin that allows users to see emoticons in comments as|YES|NO|NO|YES|
|[events]|ACTIVE|0|The events plugin adds a stream events API which parallels|YES|NO|NO|NO|
|[events-log]|ACTIVE|39|This plugin listens to stream events and stores them in a database. The events can be retrieved through REST API.|YES|YES|YES|YES|
|[evict-cache]|ACTIVE|0|[DEPRECATED]Allows to synchronize the eviction of caches between two Gerrit instances sharing the same repositories and database|YES|NO|NO|NO|
|[examples]|ACTIVE|1|Collection of example plugins for Gerrit Code Review.|YES|YES|YES|YES|
|[find-owners]|ACTIVE|4|Plugin to check for Android and Chromium style OWNERS approval before submit and find owners for a revision.|YES|NO|NO|YES|
|[force-draft]|ACTIVE|1|Provides an ssh command to force a change or patch set to draft status|YES|NO|NO|NO|
|[gc-conductor]|ACTIVE|31|This plugin provides an automated way of detecting, managing and cleaning up (garbage collecting) the 'dirty' repositories in a Gerrit instance.|YES|NO|YES|YES|
|[gerrit-support]|ACTIVE|0|Plugin to collect information on Gerrit Code Review setup for requesting support.|YES|NO|NO|NO|
|[gitblit]|ACTIVE|0|GitBlit code-viewer plug-in with SSO and Security Access Control|YES|NO|NO|NO|
|[gitgroups]|ACTIVE|0|GroupBackend using text files stored in Git|NO|NO|NO|NO|
|[github]|ACTIVE|0|Plugin to integrate with GitHub: replication, pull-request to Change-Sets|YES|YES|YES|YES|
|[github-groups]|ACTIVE|0|Group backend implementation to use GitHub Organisations and Teams as Gerrit Groups|YES|NO|NO|NO|
|[github-profile]|ACTIVE|0|GitHub-Profile integration for migrating and synchronising your GitHub e-mail address and SSH Keys with Gerrit|YES|NO|NO|NO|
|[github-pullrequest]|ACTIVE|0|Import existing GitHub Pull Requests as Gerrit Changes and Patch-Sets with one click.|YES|NO|NO|NO|
|[github-replication]|ACTIVE|0|Replication wizard for importing and configuring GitHub repos as Gerrit slaves replicas with a single click|YES|NO|NO|NO|
|[github-webhooks]|ACTIVE|0|Expose Gerrit automation actions (e.g. importing a pull request) as GitHub hooks.|YES|NO|NO|NO|
|[gitiles]|ACTIVE|16|Plugin running Gitiles alongside a Gerrit server|YES|YES|YES|YES|
|[go-import]|ACTIVE|31|NONE|YES|NO|YES|YES|
|[google-apps-group]|ACTIVE|0|Sample group backend plugin using Google Groups on a Google Apps domain.|NO|NO|NO|NO|
|[healthcheck]|ACTIVE|5|Gerrit plugin for triggering a general configuration and runtime health check|YES|YES|YES|YES|
|[heartbeat]|ACTIVE|38|Plugin that sends heartbeat stream event.|YES|YES|YES|YES|
|[helloworld]|READ_ONLY|0|Template plugin that adds new SSH commands to a server.|N/A|N/A|N/A|N/A|
|[hide-actions]|ACTIVE|0|Plugin that allows to hide UI actions by configuration.|YES|NO|NO|NO|
|[high-availability]|ACTIVE|48|Synchronize eviction of caches, secondary indexes and stream events between two Gerrit instances sharing the same git repositories and database.|YES|YES|YES|YES|
|[hooks]|ACTIVE|0|Server-side hooks executed on Gerrit events.|YES|YES|YES|YES|
|[hooks-audit]|ACTIVE|0|Plugin(s) to enable auditing of Gerrit admin and user activity to an external logging system|YES|NO|NO|NO|
|[hooks-bugzilla]|READ_ONLY|0|Deprecated. Please use plugins/its-bugzilla instead.|N/A|N/A|N/A|N/A|
|[hooks-its]|READ_ONLY|0|Deprecated. Please use plugins/its-base instead.|N/A|N/A|N/A|N/A|
|[hooks-jira]|READ_ONLY|0|Deprecated. Please use plugins/its-jira instead.|N/A|N/A|N/A|N/A|
|[hooks-rtc]|READ_ONLY|0|Deprecated. Please use plugins/its-rtc instead.|N/A|N/A|N/A|N/A|
|[imagare]|ACTIVE|1|Plugin allows Gerrit users to upload and share images.|YES|NO|NO|YES|
|[image-diff]|ACTIVE|0|An enhanced image diff plugin for PolyGerrit.|YES|NO|NO|NO|
|[importer]|ACTIVE|3|Plugin to import projects from one Gerrit server into another Gerrit server.|YES|NO|NO|NO|
|[its-base]|ACTIVE|2|Plugin base for issue tracking systems.|YES|YES|YES|YES|
|[its-bugzilla]|ACTIVE|0|Plugin to integrate with Bugzilla.|YES|NO|NO|YES|
|[its-github]|ACTIVE|0|Plugin to integrate with GitHub Issue Tracker.|NO|NO|NO|NO|
|[its-jira]|ACTIVE|0|Plugin to integrate with Atlassian JIRA.|YES|YES|YES|YES|
|[its-phabricator]|ACTIVE|0|Plugin to integrate with Phabricator.|YES|NO|NO|YES|
|[its-redmine]|ACTIVE|0|Plugin to integrate with Redmine|YES|NO|NO|NO|
|[its-rtc]|ACTIVE|0|Plugin to integrate with IBM Rational Team Concert.|YES|NO|NO|NO|
|[its-storyboard]|ACTIVE|0|Plugin to integrate with the Storyboard Issue Tracking System|YES|NO|NO|NO|
|[javamelody]|ACTIVE|32|Plugin to monitor a Gerrit server with JavaMelody.|YES|NO|YES|YES|
|[kafka-events]|ACTIVE|6|Gerrit event producer for Apache Kafka|YES|YES|YES|YES|
|[labelui]|ACTIVE|0|The labelui plugin allows users to configure a different control for displaying the labels/approvals on the change screen.|YES|NO|NO|NO|
|[lfs]|ACTIVE|31|LFS plugin storing large objects|YES|NO|YES|YES|
|[lfs-storage-fs]|READ_ONLY|0|DEPRECATED: Use the plugins/lfs|N/A|N/A|N/A|N/A|
|[lfs-storage-s3]|READ_ONLY|0|DEPRECATED: Use the plugins/lfs|N/A|N/A|N/A|N/A|
|[log-level]|ACTIVE|26|Plugin to allow an administrator to persist configured log levels across restarts|YES|NO|YES|YES|
|[login-redirect]|ACTIVE|0|Plugin to redirect anonymous users to the login form|YES|NO|NO|NO|
|[maintainer]|ACTIVE|0|NONE|YES|NO|NO|NO|
|[manifest]|ACTIVE|0|The manifest plugin provides server side utilities to|YES|NO|NO|NO|
|[manifest-subscription]|ACTIVE|0|This plugin allows users to monitor git-repo manifests in manifest repositories and generate rev-specific manifests (similar to "repo manifest -o") and store them to a separate git repository.|YES|NO|NO|NO|
|[menuextender]|ACTIVE|0|Plugin that allows Gerrit administrators to configure additional menu entries from the WebUI.|YES|NO|NO|NO|
|[messageoftheday]|ACTIVE|27|NONE|YES|NO|YES|YES|
|[metrics-reporter-cloudwatch]|ACTIVE|0|This plugin reports Gerrit metrics to AWS Cloudwatch Service.|YES|NO|NO|NO|
|[metrics-reporter-elasticsearch]|ACTIVE|0|This plugin reports Gerrit metrics to ElasticSearch Indexes.|YES|NO|NO|NO|
|[metrics-reporter-graphite]|ACTIVE|0|This plugin reports Gerrit metrics to Graphite.|YES|NO|NO|NO|
|[metrics-reporter-jmx]|ACTIVE|5|This plugin exposes Gerrit metrics as JMX resources.|YES|NO|NO|NO|
|[metrics-reporter-prometheus]|ACTIVE|8|This plugin exposes Gerrit metrics to Prometheus (https://prometheus.io/).|YES|NO|NO|YES|
|[motd]|ACTIVE|0|Plugin that provides messages to users on fetch/pull/clone|YES|NO|NO|NO|
|[multi-master]|ACTIVE|1|Plugin(s) to enable Gerrrit multi-master operation.|YES|NO|NO|NO|
|[multi-site]|ACTIVE|98|Multi-site support for Gerrit Code Review|YES|YES|YES|YES|
|[oauth]|ACTIVE|46|OAuth2 provider plugin. Multiple providers are currently supported:|YES|NO|YES|YES|
|[out-of-the-box]|ACTIVE|0|Plugin to provide an out-of-the-box redirect for a fresh Gerrit install|YES|NO|NO|NO|
|[owners]|ACTIVE|8|Provides a Prolog predicate add_owner_approval/3 that appends label('Owner-Approval', need(_)) to a provided list.|YES|YES|YES|YES|
|[plugin-manager]|ACTIVE|4|One plugin to rule them all: install new plugins from Gerrit GUI|YES|NO|NO|YES|
|[project-download-commands]|ACTIVE|1|Plugin that adds support for project specific download commands.|YES|NO|NO|NO|
|[project-group-structure]|ACTIVE|30|This plugin enforce a project group structure and restrict project creation within this structure to project group owners only.|YES|NO|YES|YES|
|[prolog-submit-rules]|ACTIVE|0|NONE|YES|NO|NO|NO|
|[pull-replication]|ACTIVE|7|Mirror repos from other servers using the Git protocol|YES|NO|NO|NO|
|[push-pull-replication]|ACTIVE|0|Alternative Gerrit replication plugin that uses both push and pull operations as replication logic.|NO|NO|NO|NO|
|[quickstart]|ACTIVE|0|Gerrit plugin for providing a Quck-start configuration during the init phase|NO|NO|NO|NO|
|[quota]|ACTIVE|27|This plugin allows to enforce quotas in Gerrit.|YES|NO|YES|YES|
|[rabbitmq]|ACTIVE|0|Publishes Gerrit events to RabbitMQ.|YES|YES|YES|YES|
|[rate-limiter]|ACTIVE|42|Allows to enforce rate limits in Gerrit.|YES|YES|YES|YES|
|[readonly]|ACTIVE|40|A plugin to make Gerrit run in read-only mode|YES|YES|YES|YES|
|[ref-protection]|ACTIVE|0|Creates backups of refs that are deleted or non-fast-forward updated.|YES|NO|NO|YES|
|[reject-private-submit]|ACTIVE|0|Reject submission (merging) of private changes|YES|NO|NO|NO|
|[rename-project]|ACTIVE|30|A plugin which allows projects to be renamed from Gerrit via an SSH command|YES|NO|YES|YES|
|[reparent]|ACTIVE|0|Plugin that provides a self-service for reparenting projects.|YES|NO|NO|NO|
|[replication]|ACTIVE|29|Copies to other servers using the Git protocol|YES|YES|YES|YES|
|[replication-status]|ACTIVE|1|Record and display the repository's replication status without having to dig into the Gerrit replication_log|NO|NO|NO|NO|
|[repository-usage]|ACTIVE|0|Searches repositories for submodules and manifest files and saves references to a database.|YES|NO|NO|NO|
|[review-strategy]|ACTIVE|0|Provide configurations for custom Gerrit review strategies.|YES|NO|NO|NO|
|[reviewassistant]|ACTIVE|12|Gives advice to reviewers on how the review should be|YES|NO|NO|YES|
|[reviewers]|ACTIVE|28|A plugin that allows adding default reviewers to a change.|YES|NO|YES|YES|
|[reviewers-by-blame]|ACTIVE|0|A plugin that allows to automatically add reviewers to a change from the git blame computation on the changed files. It will add the users as reviewer that authored most of the lines touched by the change, since these users should be familiar with the code and can most likely review the change.|YES|NO|YES|YES|
|[reviewnotes]|ACTIVE|4|Annotates merged commits using notes on refs/notes/review.|YES|YES|YES|YES|
|[saml]|ACTIVE|0|Plugin for Gerrit authentication with a SAML provider|YES|NO|NO|YES|
|[scripting-rules]|ACTIVE|0|NONE|YES|NO|NO|NO|
|[scripting/groovy-provider]|ACTIVE|0|Allows the load Gerrit plugins implemented as Groovy scripts|YES|NO|NO|NO|
|[scripting/scala-provider]|ACTIVE|0|Allows the load Gerrit plugins implemented as Scala scripts|YES|NO|NO|NO|
|[scripts]|ACTIVE|0|Scripting plugins for providing simple and useful extensions on top of Gerrit|YES|NO|NO|NO|
|[secure-config]|ACTIVE|0|Plugin to encrypt the values of secure.config.|YES|YES|YES|YES|
|[server-config]|ACTIVE|0|This plugin enables access (download and upload) to the server config|YES|NO|NO|NO|
|[server-log-viewer]|ACTIVE|0|Displays $site_path/logs through a web browser|NO|NO|NO|NO|
|[serviceuser]|ACTIVE|43|This plugin allows to create service users in Gerrit.|YES|YES|YES|YES|
|[shutdown]|ACTIVE|0|Gerrit plugin to provide a graceful shutdown via RESTful API (intended for Windows Service integration)|NO|NO|NO|NO|
|[simple-submit-rules]|ACTIVE|1|NONE|YES|NO|NO|YES|
|[singleusergroup]|ACTIVE|0|GroupBackend enabling users to be directly added to access rules|YES|NO|YES|YES|
|[slack-integration]|ACTIVE|23|Allows for the publishing of certain Gerrit events to a configured Slack Webhook URL.|YES|NO|YES|YES|
|[supermanifest]|ACTIVE|0|Update superproject in response to manifest changes.|YES|NO|NO|NO|
|[sync-events]|READ_ONLY|0|[DEPRECATED]Allows to share stream events between two Gerrit instances|N/A|N/A|N/A|N/A|
|[sync-index]|READ_ONLY|0|[DEPRECATED]Allows to synchronize secondary indexes between between two Gerrit instances sharing the same git repositories and database.|N/A|N/A|N/A|N/A|
|[task]|ACTIVE|21|The task plugin provides a mechanism to manage tasks which|YES|NO|YES|YES|
|[uploadvalidator]|ACTIVE|26|This plugin allows to configure upload validations per project.|YES|NO|YES|YES|
|[verify-status]|ACTIVE|14|Verification status plugin to visualize different jobs status that contributed to verify vote.|YES|NO|NO|YES|
|[webhooks]|ACTIVE|14|This plugin allows to propagate Gerrit events to remote http endpoints.|YES|NO|YES|YES|
|[websession-broker]|ACTIVE|6|Plugs into the builtin Gerrit WebSession implementation and broadcast websessions to an external broker|YES|YES|YES|NO|
|[websession-flatfile]|ACTIVE|0|Replaces the builtin Gerrit WebSession implementation with one that uses a flat file based cache.|YES|NO|NO|NO|
|[wip]|ACTIVE|0|Plugin that allows to mark changes as Work In Progress.|YES|NO|NO|NO|
|[wmf-fixshadowuser]|ACTIVE|0|NONE|YES|NO|NO|NO|
|[x-docs]|ACTIVE|1|This plugin serves Markdown project documentation as HTML pages.|YES|NO|NO|NO|
|[zookeeper-refdb]|ACTIVE|0|Zookeeper-backed reference database plugin.|NO|NO|NO|NO|
|[zuul]|ACTIVE|0|Gerrit Zuul Plugin|YES|NO|NO|NO|
|[zuul-status]|ACTIVE|0|Displays zuul status on PolyGerrit change|YES|NO|YES|YES|

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
