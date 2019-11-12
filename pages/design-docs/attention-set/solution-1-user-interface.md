---
title: "Design Doc - Attention Set - Solution 1 - User Interface"
sidebar: gerritdoc_sidebar
permalink: design-doc-attention-set-solution-1-user-interface.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/attention-set
---

*Please read these other parts of the solution before this doc:*

*   [Use Cases](use-cases.md)
*   [Workflow](solution-1-workflow.md)

# Solution 1 - User Interface

## <a id="overview">Overview

We will add a new section at the top of every dashboard called "Needs Attention" that displays all
changes that currently need attention from the user, including both incoming and outgoing reviews.

On the dashboard and on the change page users that are in the attention set will be highlighted by
some kind of arrow icon next to their username.

Hovering over or clicking a username or the arrow will open a dialog with the following
functionality:

*   Adding to or removing the user from the attention set.
*   Showing the timestamp along with the expectation message and the snoozing condition, if they
    exist.
    
The reply dialog will contain a section for showing the default changes applied to the attention
set when clicking "Send", and it will allow to modify them. 

## <a id="detailed-design">Detailed Design

TBD. This also has to cover how email notifications are going to change exactly.

## <a id="alternatives-considered">Alternatives Considered

TBD (suggestions welcome)

## <a id="pros-and-cons">Pros and Cons

TBD (suggestions welcome)

## <a id="implementation">Implementation Plan and Time Estimation

Will be implemented by Google and be ready for the 3.2 release.
