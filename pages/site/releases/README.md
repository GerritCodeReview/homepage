---
title: "Gerrit Code Review Releases"
permalink: releases-readme.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

Gerrit Code Review releases can be downloaded from the
[download site](https://gerrit-releases.storage.googleapis.com/index.html)
(.war files only) or from
[Maven Central](http://search.maven.org/#search%7Cga%7C1%7Cg%3A%22com.google.gerrit%22)
(.war files and API artifacts, version 2.9 and later).

Artifacts deployed to Maven Central are signed with the maintainer's key.
Please refer to the [list of maintainers' keys](/public-keys.html).

The support status of all recent Gerrit versions is
[summarized here](https://www.gerritcodereview.com/support.html#supported-versions).

## 3.11

* Java 21

* Enforce project configuration changes for code review

* New maintenance APIs

* New metrics

* New Submit requirements

[Release notes for Gerrit 3.11](/3.11.html)

## 3.10

* Rebase merge commits

* Further improve Suggest Fixes

* Import changes from other servers

* List enabled features/experiments via REST API

* Index management is now more accessible

* Less email notifications

* Support project~changeNumber when querying for changes

* Configurable H2 cache pruning

* Improved H2 Cache performances

* Allow fixes in Human comments via Rest API

* Native log deletion

* Support for secondary emails

* Update author and committer from the UI

[Release notes for Gerrit 3.10](/3.10.html)

## 3.9

* Java 17

* New stream events

* New limits

* New diff3 view

* Attention-set improvements

* Indexing improvements

* Account deletion

* User Suggested Edits

[Release notes for Gerrit 3.9](/3.9.html)

## 3.8 (EOL)

* Rebase on behalf of the uploader

* Rebase a chain of changes

[Release notes for Gerrit 3.8](/3.8.html)

## 3.7 (EOL)

* UI mostly migrated to [Lit](https://lit.dev/)

* Mention support

* Full markdown support

* Bulk actions on search results and dashboard

* Import of Projects and Changes from other Gerrit servers

* New command to check project access for other users

[Release notes for Gerrit 3.7](/3.7.html)

## 3.6 (EOL)

* Deprecation of Prolog for submit rules and introduction of Submit Requirements

* Removal of support for CentOS

* Review labels copied and used from the latest patch-set

* Performance improvements

[Release notes for Gerrit 3.6](/3.6.html)

## 3.5 (EOL)

* Java 8 support dropped

* Case-insensitive usernames

* Request cancellation and execution deadlines

* Performance improvements

[Release notes for Gerrit 3.5](/3.5.html)

## 3.4 (EOL)

* Checks UI

* Unresolved Comments ported to latest patchset

* JCraft JSch client library is disabled per default

[Release notes for Gerrit 3.4](/3.4.html)

## 3.3 (EOL)

* Java 11 by default for Gerrit

* New logs timestamp format

* Attention Set

[Release notes for Gerrit 3.3](/3.3.html)

## 3.2 (EOL)

* Polymer 3

* File Uploads in frontend

[Release notes for Gerrit 3.2](/3.2.html)

## 3.1 (EOL)

* Support for git protocol V2

* Polymer 2

* Mandatory plugins

* Performance logging and tracing

[Release notes for Gerrit 3.1](/3.1.html)

## 3.0 (EOL)

* The GWT UI is removed and PolyGerrit is now the only UI.

* The database backend for changes, accounts, groups and projects ("ReviewDb") is
removed and all metadata is now stored in git ("NoteDb").

* New quota enforcer extension point.

* Support for signed push with GPG subkeys.

* New core plugins: `delete-project`, `gitiles`, `plugin-manager` and `webhooks`.

[Release notes for Gerrit 3.0](/3.0.html)

## 2.16 (EOL - with exceptions)

* GWT UI is deprecated, and PolyGerrit is now the default UI.

* Experimental Dark Mode in PolyGerrit.

* Inline editing support in PolyGerrit UI.

* Redesigned UI for PolyGerrit based on material.

* New configuration option to ignore self-approval on labels.

* New CommonMark/Markdown parser.

[Release notes for Gerrit 2.16](/2.16.html)

## 2.15 (EOL)

* New change workflows for changes not yet ready for full review (formerly
  Drafts).

* The new PolyGerrit UI is mature enough for most uses.

* Account data is stored in NoteDb.

* NoteDb for change metadata is considered stable, and new sites use it by
  default.

* NoteDb migration for change metadata is available.

* Made several improvements and additions to the documentation to help users
  find the information they need.

[Release notes for Gerrit 2.15](/2.15.html)

## 2.14 (EOL)

* Changes can be assigned to specific users

* Open and Abandoned changes can be deleted

* HTML emails and new templating framework

* Support for receiving review comments by email

* New [Polymer](https://www.polymer-project.org/) based user interface

* Support for elliptic curve/ed25519 SSH keys

* Secondary index with Elastic Search (experimental)

[Release notes for Gerrit 2.14](/2.14.html)

## 2.13 (EOL)

* Support for Git LFS

* Metrics interface

* Hooks plugin

* Access control for git submodule subscriptions

[Release notes for Gerrit 2.13](/2.13.html).

## 2.12 (EOL)

* New change submission workflows: 'Submit Whole Topic' and 'Submitted Together'.

* Support for GPG Keys and signed pushes.

[Release notes for Gerrit 2.12](/2.12.html).

## 2.11 (EOL)

* [Issue 505](https://bugs.chromium.org/p/gerrit/issues/detail?id=505):
Changes can be created and edited directly in the browser.

* Many improvements in the new change screen.

* The old change screen is removed.

[Release notes for Gerrit 2.11](/2.11.html).

## 2.10 (EOL)

* Support for externally loaded plugins.

* Customizable `My` menu.

[Release notes for Gerrit 2.10](/2.10.html).

## 2.9 (EOL)

* The new change screen is now the default change screen.

[Release notes for Gerrit 2.9](/2.9.html).

## Older Releases

Release notes for releases prior to 2.9 can be found on the old
[documentation site](http://gerrit-documentation.storage.googleapis.com/ReleaseNotes/index.html).
