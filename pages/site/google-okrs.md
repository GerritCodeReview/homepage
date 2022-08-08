---
title: "Google quarterly objectives"
permalink: google-okrs.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

Google plans work per-quarter, using the OKR (Objective/Key-Result) framework.

# Q3 2022

## O: Increase system reliability

### KR: Make the token highlight layer more efficient.

### KR: Prevent HTML injection through commentLink feature

### KR: Add shadowdom tests for each FE component

### KR: Lit based gr-diff rendering

This increases maintainability and makes it faster.

### KR: Better plugins

Work with SAP on checks-jenkins plugin. Deprecate the checks plugin on gerrit-review.



## O: Improve Gerrit customer satisfaction

### KR: Land bulk actions

Provide actions on multiple changes from the dashboard page. Polish in
response to user feedback.

### KR: Allow patchset upload creation from textual patch

This provides a mechanism that could execute cherry-picks across gerrit hosts.

### KR: Land push notifications

Show browser notifications if the attentionset for a user changes.

### KR: Implement suggested edits

Allow reviewers to suggest changes through specially formatted
comments. Authors can apply the change as a change-edit.

### KR: Land enhanced file status information

Show file status diffs (added, removed) between patchsets.

## O: Reduce toil, increase developer velocity, and improve developer happiness


# Q2 2022

## O: Increase system reliability

### KR: Reduce overhead of Prolog

Roll them out fully on googlesource.com for Android and Chrome,
addressing any feature gaps relative to Prolog.

*result*: launched to all but one host.

## O: Improve Gerrit customer satisfaction

### KR: Polish composable submit requirements based on customer feedback

*result*: this is finished.

### KR: Launch bulk actions

Provide actions on multiple changes from the dashboard page.

*result*: code almost finished, launch pending.

### KR: Polish approval copying infrastructure

When uploading new patchsets, provide more information to users why
they need to get approvals again.

*result*: done.

## O: Reduce toil, increase developer velocity, and improve developer happiness

### Finish Lit migration

Lit is the next generation version of Polymer. Besides being nicer to
work with, it reduces cold start due to reduced code size.

*result*: done, except the code-owners plugin and gr-overlay and
gr-account-list (on Polymer due to Iron dependencies.)


# Q1 2022

## O: Increase system stability and reduce latency of critical user journeys

### KR: Remove per-user state (drafts, stars) from the change index,
    improving write latencies


### KR: Speed up median diff rendering latency for views with many files

Use multiple fidelity modes and webworkers to speed up "expand all
diffs" and "large file with many diffs" use cases.

## O: Improve Gerrit customer satisfaction from X% to Y%

### KR: Roll out composable submit requirements

Use them fully on gerrit-review.googlesource.com,
android-review.googlesource.com and chromium-review.googlesource.com.

### KR: Multi-change review: Prototype and validate a new experience
    for managing and reviewing multiple, grouped changes

### KR: Reduce P50 code review start latency

Design browser-based push notifications to reduce review latency. Let
reviewers suggest rather than make edits, leading to less lost
approvals.

### KR: Addressing top Gerrit pain points

Fix JGit and CGit merge discrepancies.


# Q4 2021

## O: Gerrit users' data and code are well protected and secure

### KR: Resolve data protection/security work in flight from Q3

A data migration has cleaned all traces of personal data (name, email) in review
metadata.

## O: Increase system stability and reduce latency of critical user journeys

### KR: Migrate to Caffeine for all caches

This is now possbile since we moved off of the old diff cache.

### KR: Investigate reasons for slow pushes, fix if possible

We want Git pushes where users currently bypass Gerrit to go through Gerrit as
well. We suspect that performance (pushes being slow) is the main reason for
bypassing. If so, we want to root cause slowness and fix it if possible.

## O: Improve Gerrit customer satisfaction from X% to Y%

### KR: Roll out composable submit requirements

Use them fully on gerrit-review.googlesource.com,
android-review.googlesource.com and chromium-review.googlesource.com.

### KR: Multi-change review: Implement MVP

Provide a page for reviewing multiple changes ("topics"), providing among others
batch actions and maybe diffs across projects/changes.

## O: Reduce toil, increase developer velocity, and improve developer happiness

### KR: Migrate 33% of remaining frontend components to Lit, remove
     all of Polymer, and get rid of or re-implement all mixins

###  KR: Migrate frontend to client models and dependency injection.

client models will centralize state-management, making the UI more
dependable. Dependency injection avoids global variables, enabling
multiple changes on a single page


# Q3 2021

## O: Gerrit users' data and code are well protected and secure

### KR: Resolve data protection/security work in flight from Q2

Gerrit stops persisting personal data (name, email) in review metadata.


## O: Increase system stability and reduce latency of critical user journeys

### KR: Keep CreateDraftcomment in SLO by removing per-user state from change index

Private user actions (writing drafts, adding stars) cause a change reindex. This
is expensive and slows down user actions. Get this data directly from All-Users
to avoid the indexing step.


###  KR: Cancelation: ensure no work happens for requests after the users have canceled or the request has timed out

Gerrit continues processing after the user hangs up. We want to solve this for
Google, but maybe we can fix it for Gerrit open source as well.

### KR: Image diffing

The Gerrit UI supports reviewing image files (including visual diffs)

###    KR: Improve gr-diff performance

Improve diff rendering performance and memory usage on many / large files.


###    KR: Plan for transactional index updates

Currently Gerrit indices are per-datacenter, and replicated asynchronously.
Create a design where the index document is created together with the ref
update, so it can be replicated together with the Git data, thus avoiding
inconsistencies between index and git data.


###    KR: Use Caffeine to reduce drift with open-source and to speed up parallel cache reads

Finish diff cache rollout, and migrate to Caffeine.


## O: Improve Gerrit customer satisfaction from X% to Y%


###    KR: Roll out composable submit requirements to Android and Chrome

Implement https://gerrit-review.googlesource.com/c/homepage/+/279176, and roll
it out to Gerrit, Chrome & Android.


###   KR: Multi-change review: Prototype and validate a new experience for managing and reviewing multiple, grouped changes

Provide a page for reviewing multiple changes ("topics"), providing among others
batch actions and maybe diffs across projects/changes.


###   KR: Code Review Latency: Reduce P50 code review start latency from Xmin to Ymin.

**Calendar integration: **extension point for FE plugins surfacing calendar data

**Push notifications**: Design proposal, work estimation, and prototype for
browser push notifications directly from Gerrit using web workers (milutin)

**Code review dashboard**: Gerrit users can understand their personal code
review performance in a dashboard as described in Gerrit Code Review Metrics for Individuals (mharbach)


###   KR: Gerrit CI Reboot: Land the new CI Results Tab

Finish CI result tab: onboarding documentation, create a Jenkins based plugin
and remove the old checks plugin from googlesource.com.


###   KR: Make headway on addressing top Gerrit pain points, as measured by surveys and internal customers

Various items:

*   Markdown support
*   Ingest textual diffs for creating or updating changes
*   Many smaller UI polish items.


## O: Reduce toil, increase developer velocity, and improve developer happiness


###   KR: Maintainable Gerrit frontend plugins: convert all Gerrit maintained frontend plugins to Typescript.


###   KR: Add Polymer template type checking (carryover)

Gerrit CI will then be able to check that Polymer bindings are valid in HTML
templates and that Polymer observers and computed Polymer properties have the
correct type.


###   KR: Publish Gerrit Q3 OKRs publicly to give guidance to the external community

note: Any Google-specific OKRs will be removed prior to publishing
