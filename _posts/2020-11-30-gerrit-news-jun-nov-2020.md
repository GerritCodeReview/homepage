---
title: "Gerrit Project News #10: June-November 2020"
tags: news
keywords: news
permalink: 2020-11-18-gerrit-news-jun-nov-2020.html
summary: "Gerrit project news from June to November 2020."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

# New Features

## Attention Set

We are happy to announce that the new attention set feature is now available and
turned on for Google’s hosted Gerrit sites. This feature allows users to better
understand whose turn it is in a review. Attention arrows are now displayed
beside the user name and in the dashboard. You can read more about the attention
set
[here](https://gerrit-review.googlesource.com/Documentation/user-attention-set.html#_interaction).

![Attention set arrow](/images/news-jun-nov-2020-attention-set-arrow.png)

Attention can be assigned to a user (e.g. owner, reviewer or CC) by hovering
over their name on the change page and clicking “Add to attention set”, or while
replying to a change.

The attention set will be available in the next v3.3 release.

## New Account Cache

The “accounts” cache was reworked and persisted. It holds the account details
and all the information stored under the user’s ref. The new design requires a
lot less I/O when an entry needs to be reloaded and lowered the ratio of cache
misses in case of user’s details updates.

## Projects Cache

We persisted the “projects” cache by splitting it into 2 caches: an in-memory
cache and a persisted cache. The former is keyed by the project name and does
not need to look up the ObjectId of refs/meta/config in NoteDb. The latter is a
persisted variant of the “projects” cache and allows admins to persist the
project cache - if desired - to ease cold start times.

## Ported Comments

Gerrit now supports porting comments of other revisions to a requested revision.
Two new endpoints are now available: [GET ported
comments](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-ported-comments)
and [GET ported
drafts](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-ported-drafts).
Ported comments is an important feature that will help users view unresolved
comments from all patchsets on the latest patchset, hence helping users not to
miss them.  This feature will soon be available in the polygerrit UI.

## Comment Context

The “[List Change
Comments](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-change-comments)”
endpoint now has an enable_context parameter that allows retrieving the lines of
the source file where the comment was written.  This feature will soon be
available in the polygerrit UI.

## Patchset Level Comments

We introduced a new type of comments: patchset-level comments are associated
with a specific patchset but are not attached to any file or line. So what you
are saying in the “Reply” dialog becomes a threaded conversation with an
“unresolved” flag.

![Patchset level comment](/images/news-jun-nov-2020-patchset-level-comment.png)

## Coming Next

Upcoming features for comments will soon be available in the user interface.
This includes ported comments, comment context and others.

# UI Enhancements

## Comment Links

The destination of comment links has changed to point to the diff between the
comment's patchset vs. latest instead of the comment's patchset vs. base. This
helps reviewers quickly check that their comments have been addressed. New
keyboard shortcuts were also added for quickly changing the patchset choice.

![Diff keyboard shortcuts](/images/news-jun-nov-2020-diff-keyboard-shortcut.png)

## Unresolved comments in the dashboard

A new icon was added to the dashboard in the “CR” column if the change has
unresolved comments.

![Unresolved
comments](/images/news-jun-nov-2020-unresolved-comments-in-dashboard.png)

# Plugins

## Code Owners

The new [code-owners](https://gerrit.googlesource.com/plugins/code-owners)
plugin is now available to support defining owners for files in a repository. If
the code-owners plugin is enabled, changes can only be submitted if all touched
files are covered by approvals from code owners.

## Download Commands

The “Download patch” UI now includes an option for creating a local branch. This
allows developers who are not familiar with the idiosyncrasies of repo, to
easily create a local branch when checking out changes.

## Cache ChronicleMap

We added a new non-blocking and super-fast on-disk cache to the Gerrit modules.
The cache is based on [ChronicleMap on-disk
implementation](https://github.com/OpenHFT/Chronicle-Map). More instructions on
how to build and use the new module is available
[here](https://gerrit.googlesource.com/modules/cache-chroniclemap/).

# Product Updates

## Project Members and ESC

The Engineering steering committee had changed in October 2020:

* Han-Wen Nienhuys replaced Alice Kober-Sotzek for the Google affiliation.
* Saša Živkov replaced David Pursehouse for the non-Google affiliation.

We would like to thank Alice and David once again for their uniquely significant
contibutions to Gerrit. They will be missed. Yet we are happy to welcome Han-Wen
and Saša for these new roles alongside their lasting maintainer ones. Thanks for
joining our ESC!

More information about the project members
[here](https://gerritcodereview.com/members.html#engineering-steering-committee).

## Default Java 11 Language Level

The Java language level is now set to Java 11 by default for Gerrit. Java 8 is
still supported and can be used by doing a rebuild for Gerrit.

## Typescript Migration

Gerrit’s Javascript codebase was recently migrated to Typescript. This would
allow for a lot of new benefits including class and module support, static type
checking and clear library API definition, among others.

# Community

## Virtual Contributor Summit 2020

The Gerrit community had a virtual 2-days event with various talks and
discussions. The presentation slides and notes are available from the
[agenda](https://docs.google.com/document/d/1WauJfNxracjBK3PxuVnwNIppESGMBtZwxMYjxxeDN6M).

