---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2019-10-01-esc-minutes.html
summary: "Minutes from the ESC meeting held on October 1st"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, October 1, 2019

### Attendees

David Pursehouse, Alice Kober-Sotzek, Luca Milanesio, Ben Rohlfs, Patrick Hiesel

### Place/Date/Duration

Online, October 1, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on October 15, 12:30 CEST.

## Minutes

### Gerrit News Page

The latest issue of the project news was
[published on September 27](https://www.gerritcodereview.com/2019-09-27-gerrit-news-aug-sep-2019.html).

A [draft has been created](https://gerrit-review.googlesource.com/c/homepage/+/239186)
for the next issue which is to be published on November 29.

There were no news items proposed during this meeting. Members of the community
may propose items by adding a change on the draft post.

### Renaming of 'reviewdb' package to something else

Since we migrated from ReviewDb to NoteDb it doesn't make sense to have
classes in the `reviewdb` package any more. David Ostrovsky proposed a
[series of change](https://gerrit-review.googlesource.com/q/topic:rename-reviewdb-package)
to rename the packge to `entities`.

We all agreed that `reviewdb` is no longer an appropriate name for the
package and that it should be renamed. Ben also pointed out that it can
cause confusion for new developers.

Alice mentioned that we should also consider that some of the classes may
not really need to be kept in the `entities` package and can be moved to
other, more appropriate packages.

We concluded that we should do this in two steps. First, rename the package,
which can be included in the upcoming 3.1 release. And second, move classes
to more appropriate packages.  The latter should be deferred until after 3.1,
so it goes into 3.2.

### Make the reviewers plugin a core plugin

[Issue 10732](https://bugs.chromium.org/p/gerrit/issues/detail?id=10732)
proposes to make the reviewers plugin a core plugin.

We discussed this without reaching any concrete conclusion. We will defer
to the newly formed Plugin Working Group to define criteria for promoting
a plugin to core, and then revisit this issue.

### Make checks a core feature instead of a plugin

[Issue 11534](https://bugs.chromium.org/p/gerrit/issues/detail?id=11534)
proposes to make the checks plugin a core plugin. In that issue David
Ostrovsky suggested the alternative of making checks a core feature
rather than a plugin, with the motivation being that a number of current
design limitations in checks plugins are coming from its nature being a
plugin and not a pure gerrit core feature.

Several points were raised during the discussion:

- Checks is a useful feature that should be core (either actually in core
or as a plugin).

- There are some user bases who have their own custom solutions and hence
might not be interested in checks.

- If it were a core feature it could be switched off with a config setting,
but on the other hand this is the reason we have plugins: if someone doesn't
want the feature they don't install it.

- Long term it might be better as a core feature, i.e. at the point where
gerrit-review is using it rather than labels.

- Does the community want this as a core feature?

We didn't reach a concrete conclusion as to whether checks should be a
core feature, nor whether checks should be promoted to a core plugin. We
will revisit the discussion when the integration with gerrit-review
is more complete.

If any community members have opinions on whether checks should be a
core feature, we ask them to add comments on
[issue 11534](https://bugs.chromium.org/p/gerrit/issues/detail?id=11534).

### Follow up on blocking issues for 3.1

Per the release plan for 3.1 we expect to be cutting the stable-3.1 branch
and making the first release candidate in a couple of weeks. We had a look
at the list of issues that are labelled
[Blocking-3.1](https://bugs.chromium.org/p/gerrit/issues/list?q=label%3ABlocking-3.1).

Ben confirmed that all the Polymer 2 related issues are expected to be fixed
in time.

Patrick will review the changes related to
[issue 11643](https://bugs.chromium.org/p/gerrit/issues/detail?id=11643)
("Replace deprecated numeric types with new dimensional numeric types").

For [issue 11550](https://bugs.chromium.org/p/gerrit/issues/detail?id=11550)
we decided that reducing the default SSH idle timeout will be a breaking
change for many users, and we prefer to only submit that change on master
after stable-3.1 has been cut.

### Support for deletion of groups

[Change 129130](https://gerrit-review.googlesource.com/c/gerrit/+/129130) adds
the framework of a new REST endpoint to delete groups. This is addressing one
of the oldest still open issues on the issue tracker:
[issue 44](https://bugs.chromium.org/p/gerrit/issues/detail?id=44).

David implemented the framework of the endpoint, but the actual deletion
of the group is not done. The reason for adding it in the ESC agenda was
to confirm whether or not this feature is actually still wanted.

Alice confirmed that the feature is OK, but we need to be careful that all
references to groups are handled when they are deleted. She will be involved
in the review, but only when content is added (i.e. when the actual deletion
is implemented).

### Support for role-based access controls

Support for role-based access controls was started by Sven Selberg and
Gustaf Lundh during one of the previous hackathons, but the changes got stale
and were abandoned. See
[change 104743](https://gerrit-review.googlesource.com/c/gerrit/+/104743) and the
[acl-refs-for-removal topic](https://gerrit-review.googlesource.com/q/topic:acl-refs-for-removal).

This was added into the ESC agenda for discussion on whether or not this
feature is still wanted and can be revived.

We all agreed that role-based access controls is a great idea, and would
be very useful to reduce confusion around Gerrit's permissions system, however
it is something that should be done carefully and would need to be designed
properly.

Luca suggested that this would be a good topic for a hackathon.

### Roadmap

We are almost ready to release 3.1 so there's no point including it
in the roadmap. We will just write the release notes.

We will define the roadmap for 3.2, and continue to add features there
until there is anything that we know will not make it into 3.2, then
start the roadmap for 3.3.

For any more long term (than 3.3) features we will keep a backlog which will
be cleaned regularly.

We will set up a dedicated meeting to discuss this in more detail.

### Review of issues on the ESC component

We briefly went over the issues that have been added to the
[ESC component](https://issues.gerritcodereview.com/issues?q=status:open%20componentid:1371029)
on the issue tracker.

Urgent or important issues will typically already have been added to the agenda
for the meeting, and we did cover a couple of them today.
[Issue 11528](https://bugs.chromium.org/p/gerrit/issues/detail?id=11528) was not
on the agenda and we discussed that (see next section).

We added this activity as a standing item on the ESC meeting agenda.

### Browsing repository should be a first class citizen

[Issue 11528](https://bugs.chromium.org/p/gerrit/issues/detail?id=11528) requests
that finding and browsing code repositories should be provided by the Gerrit UI.

Alice commented that 'first class' means there is a code browser in Gerrit, and
it's difficult to get that right because browsing is a product on its own. Maybe
we can improve the integration while keeping it separate. Ben also agreed that
since Gerrit is a code review tool, browsing should be separate.

Patrick also raised the point that some people might expect that a code browser
provides cross reference and search capabilities.

Everyone agreed that code browsing should be kept separate, but there is the
possibility to improve the integration with plugins such as gitiles.
