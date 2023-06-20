---
title: "Gerrit Project News #1: June-August 2018"
tags: ux
keywords: ux
permalink: 2018-09-06-gerrit-ux-newsletter-jun-aug-2018.html
summary: "This is the first in a series of newsletters we’ll send out each
quarter to update you on the UX related stuff that we have been working on in
Gerrit, and things that you can expect to see in Gerrit in the near future."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

<p style="text-align: center;">
<img src="images/code-review-icon.png" width="" alt="Gerrit Code Review Icon" title="Gerrit Code Review">
</p>

Hello, Gerrit users! This is the first in a series of newsletters that we'll
send out each quarter to update you on the UX related stuff that we have been
working on in Gerrit. We'll also discuss features and changes that you can
expect to see in the near future.

## Things we worked on this quarter

### Updated labels interface

<img style="max-width: 50%; max-height: 50%" src="images/updated-labels-interface.png" width="" alt="Screenshot of Updated Labels Interface feature" title="Updated Label Interface Feature">

The presentation of labels was updated to make better use of space, and address
issues such as
<a href="https://issues.gerritcodereview.com/issues/40008971">this bug</a>.
All labels now appear in two sections, Required labels and Other labels. This
design solves two UX issues:

+  Merging the submit requirements and votes sections has helped us avoid
   repeating all the labels under both sections, reducing the vertical real
   estate required to display a large number of labels.
+  The Other labels section can now be collapsed so in case of a large number of
   labels, users can collapse the list to get to the file list quickly.

### Image diff

<img src="images/image-diff.png" width="" alt="Screenshot of Image Diff feature" title="Image Diff Feature">

You now have more tools to compare images. The new
<a href="https://gerrit.googlesource.com/plugins/image-diff/">image diffing plugin</a>
adds new modes that make it easier to quickly locate small differences between
similar images.

### Gerrit dark theme

<img src="images/dark-theme.png" width="" alt="Screenshot of Gerrit Dark Theme feature" title="Gerrit Dark Theme">

This was actually added in April during the Lund Hackathon. It can be enabled
via the Settings menu.

## What we're working on

### New metadata layout

<img src="images/metadata-layout.png" width="" alt="Screenshot of metadata layout feature" title="Metadata Layout Feature">

The new metadata design horizontally arranges some of the metadata information
about a change just below the change title. This frees up vertical space from
the left section on the UI, which reduces the scrolling needed to get to the
file list. The left section of the change is now dedicated to data about people
and votes.

### Draft comments

<img src="images/draft-comments.png" width="" alt="Screenshot of draft comments feature" title="Draft Comments Feature">

Have you ever drafted comments in Gerrit, but lost track of them before
publishing? This design makes unpublished drafts more discoverable, more
convenient to publish, and easier to navigate.

We're taking them out of the Reply dialog and placing them at a more prominent
location on the UI. This decouples the Start review action for WIP changes with
the Publish drafts. The design also enables users to easily jump from one draft
comment to another from the file view using the Draft comments panel.

### Patchset navigation

<img src="images/patchset-navigation.png" width="" alt="Screenshot of patchset navigation feature" title="Patchset Navigation Feature">

Informed by bug reports <a href="https://issues.gerritcodereview.com/issues/40006192">like this one</a>,
the redesign adds:

+  A single drop-down to select patchsets that reduces visual focus shifts and
   clicks to compare two patchsets.
+  Showing a better representation of patchset history that shows when the
   rebases happened and more prominent indication for unresolved comments.
+  An expandable Patchset info panel that shows a lot of other relevant
   information about the patchsets such as commenters, number of total and
   unresolved comments and votes for each patchset.
+  A quick way to view all the unresolved comments for a selected patchset by
   clicking the number link under the unresolved comments column inside the
   Patchset Info panel.

Authors: <a href="mailto:arnabb@google.com">arnabb@google.com</a>,
<a href="mailto:kaspern@google.com">kaspern@google.com</a>,
<a href="mailto:wyatta@google.com">wyatta@google.com</a>

Bugs? Feedback? <a href="https://issues.gerritcodereview.com/issues/new?component=1369968&template=1834342">File it here!</a>

