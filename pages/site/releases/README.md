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

Latest release: **[3.1.0](/3.1.md)**.

## 3.1.0

* Support for git protocol V2

* Polymer 2

* Mandatory plugins

* Performance logging and tracing

[Release notes for Gerrit 3.1.0](/3.1.md)

## 3.0.0

* The GWT UI is removed and PolyGerrit is now the only UI.

* The database backend for changes, accounts, groups and projects ("ReviewDb") is
removed and all metadata is now stored in git ("NoteDb").

* New quota enforcer extension point.

* Support for signed push with GPG subkeys.

* New core plugins: `delete-project`, `gitiles`, `plugin-manager` and `webhooks`.

[Release notes for Gerrit 3.0.0](/3.0.md)

## 2.16

* GWT UI is deprecated, and PolyGerrit is now the default UI.

* Experimental Dark Mode in PolyGerrit.

* Inline editing support in PolyGerrit UI.

* Redesigned UI for PolyGerrit based on material.

* New configuration option to ignore self-approval on labels.

* New CommonMark/Markdown parser.

[Release notes for Gerrit 2.16](/2.16.md)

## 2.15

* New change workflows for changes not yet ready for full review (formerly
  Drafts).

* The new PolyGerrit UI is mature enough for most uses.

* Account data is stored in NoteDb.

* NoteDb for change metadata is considered stable, and new sites use it by
  default.

* NoteDb migration for change metadata is available.

* Made several improvements and additions to the documentation to help users
  find the information they need.

[Release notes for Gerrit 2.15](/2.15.md)


## 2.14

* Changes can be assigned to specific users

* Open and Abandoned changes can be deleted

* HTML emails and new templating framework

* Support for receiving review comments by email

* New [Polymer](https://www.polymer-project.org/) based user interface

* Support for elliptic curve/ed25519 SSH keys

* Secondary index with Elastic Search (experimental)

[Release notes for Gerrit 2.14](/2.14.html)

## 2.13

* Support for Git LFS

* Metrics interface

* Hooks plugin

* Access control for git submodule subscriptions

[Release notes for Gerrit 2.13](/2.13.html).

## 2.12

* New change submission workflows: 'Submit Whole Topic' and 'Submitted Together'.

* Support for GPG Keys and signed pushes.

[Release notes for Gerrit 2.12](/2.12.html).

## 2.11

* [Issue 505](https://bugs.chromium.org/p/gerrit/issues/detail?id=505):
Changes can be created and edited directly in the browser.

* Many improvements in the new change screen.

* The old change screen is removed.

[Release notes for Gerrit 2.11](/2.11.html).

## 2.10

* Support for externally loaded plugins.

* Customizable `My` menu.

[Release notes for Gerrit 2.10](/2.10.html).

## 2.9

* The new change screen is now the default change screen.

[Release notes for Gerrit 2.9](/2.9.html).

## Older Releases

Release notes for releases prior to 2.9 can be found on the old
[documentation site](http://gerrit-documentation.storage.googleapis.com/ReleaseNotes/index.html).
