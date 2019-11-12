---
title: "Design Doc - Attention Set - Solution 1 - User Interface"
sidebar: gerritdoc_sidebar
permalink: design-doc-attention-set-solution-1-user-interface.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/attention-set
---

# Solution 1 - User Interface

## <a id="overview"> Overview

We will add a new section at the top of every dashboard called "Needs Attention" that displays all
changes that currently need attention from the user, including both incoming and outgoing reviews.

On the dashboard and on the change page users that are in the attention set will be highlighted by
some kind of arrow icon next to their username.

Hovering over a username or the arrow (and maybe also clicking on it) will open a dialog with the
following functionality:

*   Adding to or removing the user from the attention set.
*   Showing the timestamp along with the reason when and why the user was added to the attention
    set.
*   For users not in the attention set showing the rules that will add them back and optionally
    editing them.

## <a id="detailed-design"> Detailed Design

TBD

## <a id="alternatives-considered"> Alternatives Considered

TBD (suggestions welcome)

## <a id="pros-and-cons"> Pros and Cons

TBD (suggestions welcome)

## <a id="implementation"> Implementation Plan and Time Estimation

Will be implemented by Google and be ready for the 3.2 release.
