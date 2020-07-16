---
title: "Design Doc - CI Reboot - Use Cases"
permalink: design-docs/ci-reboot-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/ci-reboot
---

# CI Reboot - Use Cases

The motivation and strategy of this effort was outlined at length in
[this Google doc](https://docs.google.com/document/d/1v2ETifhRXpuYlahtnfIK-1KL3zStERvbnEa8sS1pTwk/edit#).
This document is a brief summary of that. In addition this document outlines use cases and pain
points.

## <a id="objective">Objective

Improve user and admin experience for integrating Gerrit with continuous integration (CI) and
analyzer systems, with minimal disruption to client teams.

## <a id="background">Background

CI feedback is an integral part of the code review experience. Historically, Gerrit supports CI
through the “label vote” mechanism: the host admin configures a label (e.g. “Verified”). The CI
system discovers new changes and patch-sets through stream-events or query changes that needs
verification, runs tests on them, and reports the result with
Verified +1 (CI passes), or -1 (CI failed) votes. The admin can set requirements (e.g. Verified must
be +1) for merging. Prolog rules for submission requirements can enforce arbitrarily complex rules
for when changes may be submitted. Labels are integrated with Gerrit’s permission model, and the
configuration of labels and rules is managed through Project Inheritance, which provides a scalable
mechanism of administering settings across many repositories on a host. Other criteria for
submission blocking can also be added through server-side plugins.

## <a id="problem-statement">Problem Statement

The mechanism works for small deployments, but causes pain points that are a recurring theme in
Google's internal customer surveys for our complex deployments. The major pain points that we
want to address are the following:

### <a id="ps-labels">Labels

The UI for labels does not scale. If you have more than 5 labels configured, then the dashboard has
too many columns and the change page too a list such that other information is harder to find or
digest.

There is no clear concept for how overriding labels should work. Overriding a vote is different from
removing a vote or adding vote that trumps another vote. There is currently no way to enforce
providing a reason.

There is poor support for when labels are applicable to a change. To work around the missing support
for override many hosts create additional labels and prolog rules, but then users have a harder time
understanding the state of the labels and rules.

Labels that are used for CI system lack dedicated support for showing the "running" state of the CI
system and for the user to trigger a run or a re-run.

### <a id="ps-submit-rules">Submit Rules

Prolog offers an extremely flexible mechanism for orchestrating workflows and permissions. This
flexibility comes at a price: few admins are fluent in Prolog, and the majority of Prolog
code is actually copied & pasted from the Prolog cookbook. This makes supporting customers harder.
Prolog is also a source of outages: complex rules can overflow the Prolog interpreter tables,
wedging submissions in the project, a problem which requires intervention from the Gerrit team.

Surfacing the reason for a failed Prolog submit rule to the user is poorly supported, so it is hard
for a user to understand what to do if submission is not allowed.

There is no clear concept for how overriding submit rules should work, see also "Labels" above.

Submit rules only have a binary state: Fulfilled or not. There is no "not applicable to this change"
state, which would make it much easier to support many rules without cluttering the UI. 

### <a id="ps-details">Details

Large customers often have complex CI systems that run tests on dozens of platforms. They support
functionality that we do not wish to add to Gerrit. For example, some CI results may have visibility
ACLs. This has forced many partners into writing their own client-side integrations. The UX varies
by host/integration as the integrations include their own HTML. While the mental model of a CI is
the same, the integration looks vastly different across our tenant teams, and they impact the
perception of Gerrit as a product. All of these integrations are client-side only and rely on a
handful of Labels reported to Gerrit’s backend to indicate submittability of a change.

There is currently no native way for Gerrit to visualize the state and results of multiple CI
systems.

If a CI system runs mutiple builds or test suites, then there is no good way to visualize the
individual state of each build or test suite.

The only way to feed state and results into Gerrit are votes and robot comments. Both don't scale
beyond ~10 comments per patchset.

There is no support for CI warnings or robot comments to be acked. CI results can often be warnings
that do not block the submission, but that require a human to actively read it and mark it as "not
relevant in this case".

## <a id="use-cases">Use Cases

### <a id="uc-labels">Labels

As a user I would like ...

*   ... to understand which labels are voted on by users and which by robots.
*   ... to know which labels I can vote on.
*   ... to see at a glance ...
    *   ... which labels are approved or not approved.
    *   ... which labels are required for submitting the change
    *   ... which labels are relevant or not relevant for a change (e.g. because the label is not relevant to a
        particular branch)
*   ... to focus on labels that are most important to me. The order of importance is:
    *   *not* approved, required for submission
    *   *not* approved, *not* required for submission, but relevant for the change
    *   approved, required for submission
    *   approved, *not* required for submission, but relevant for the change
    *   not relevant for the change
*   ... to easily understand why a (robot) vote was not yet given. (If the bot has completed its run, then why is it
    holding back with the vote? Is the bot still running?)
*   ... to easily understand why a robot voted negatively on a label, i.e.
    *   ... negative label votes to be linked to detailed results pages, or to robot comments, or to CI runs.
*   ... the dashboard to provide a summary of the approval status of all labels.
*   ... to be able to override votes from robots on labels.
*   ... to be able to tell robots to re-evaluate a label vote.

As an admin ...

*   ... I would like to configure conditions for a label not being relevant to a change, e.g. by providing a regular
    expression of file paths that have to be matched by at least one file in the change.
*   ... I am fine with all labels and all label votes being visible to all users that can see the change. \[NON-GOAL\]

### <a id="uc-rules">Submit Rules

As an admin ...

*   ... I would like to write submit requirements using simple configuration syntax.
    *   ... I would like to keep the same submit requirements that I have currently written in Prolog.
    *   ... I don’t want to have to migrate all my Prolog rules within the next 12 months.
    *   ... I would like to simply combine predefined rules with boolean operators.
*   ... I would like to test changes I make to submit requirements by submitting a change as testdata and have my submit
    requirement be evaluated against that during automated tests.
*   ... I would like Gerrit to reject any invalid configuration I make (e.g. syntax errors in the config).
*   ... I would like to configure submit requirements both for all repos and for individual repos.
    *   ... I would like to be able to take advantage of inheritance.
*   ... I would like to write submit requirements based on other properties of the change other than labels, e.g. the
    comments and the file paths.
    *   ... I am fine with just having the change object as input for my submit requirement. \[NON-GOAL\]
*   ... I would like to write submit requirements based on multiple labels.
    *   ... I am fine with every label only being evaluated for at most one submit requirement. \[NON-GOAL\]
    *   ... I am fine with not being able to base a submit requirement on a label that has a “function” for guarding
        submit. \[NON-GOAL\]
*   ... I would like to communicate to users what the requirement is about and set an explanation, if the requirement is
    not fulfilled.
*   ... I would like to express that a submit requirement is not relevant to a change instead of just having it
    vacuously fulfilled,  e.g. by providing a regular expression of branches or file paths that have to be matched by at
    least one file in the change.
*   ... I would like to configure who can bypass a submit requirement.
    *   ... I would like to audit who bypassed submit requirements and why.
*   ... I am fine with all submit requirements being visible to all users that can see the change. \[NON-GOAL\]

As a user ...

*   ... I would like to easily understand *which* submit requirements are not satisfied.
*   ... I would like to easily understand *why* submit requirements are not satisfied and what I have to do to meet
    them.
*   ... I don’t want to be distracted by submit requirements that are not relevant to my change.
*   ... I don’t want to be confused by submit requirements and labels repeating the same information.

### <a id="uc-details">Details, CI Runs

As a user ...

*   ... I would like to have access to the status and outcome of all CI runs.
    *   ... I would like to have access to runs on previous patchsets.
    *   ... I would like to have access to previous attempts of runs on the same patchset.
    *   ... I would like to have filtering and searching features to help me find a specific run among hundreds of runs.
*   ... I want to know which CI runs failed (latest run of current patchset) and understand why.
*   ... I want to get down to the root cause of CI failures as quickly as possible with the least amount of clicks.
*   ... I don’t care much about CI runs that have completed successfully, but I still want to be able to look them up
    and find them.
*   ... I want to know which CI runs are currently running.
    *   ... I care less about CI runs in progress than about warnings and failures.
    *   ... I mostly care about CI runs being in progress on an aggregate level: When 50 presubmit are running, then the
        individual runs are not so interesting.
    *   ... I want to know for how long the CI run has been running (ideally along with a forecast about when it might
        be complete).
*   ... I want to trigger specific CI runs.
    *   ... I want to trigger a re-run of specific CI runs.
    *   ... I want to trigger runs and re-runs of an entire CI system or group of runs.

As a CI system developer ...

*   ... I would like to provide information about CI runs: A short summary, but also a detailed formatted message (could
    be more than 100 lines, e.g. a log) about the status or result of the run.
*   ... I would like to associate CI runs with a list of actions (callbacks) that the user can choose from and that are
    sent back to my system (run, re-run, cancel, ack, delete, report a bug, report as not useful, make blocking, ...).
*   ... I would like to associate CI runs with a list of links for the user about details or artifacts of the run (logs,
    help page, artifact download, ...).

### <a id="uc-robot-comments">Robot Comments

As a user ...

*   ... I would like to know which robot comments are just informational and which ones are warnings that need my
    attention.
*   ... I would like to understand the relationship between a robot comment and CI runs, labels and submit requirements,
    if such a relation exists.
    *   ... I would like to see which robot comments are associated with a submit blocking label.
    *   ... I don’t want to see duplicate information such as three different warnings coming from label, run and
        comment, which are essentially pointing to a single problem.

As a CI system developer ...

*   ... I want to have the ability to send CI results to Gerrit that ...
    *   ... are blocking submit.
        * But I would be fine with expressing the “blocking” aspect by a label and do not require a robot comment to be
        blocking by itself. \[NON-GOAL\]
    *   ... must be acknowledged by the user.
    *   ... are purely informational and will not distract or annoy the user.
*   ... I am fine with robot comments only being retained for a certain period of time (90 days?). After that all robot
    comments may be deleted. \[NON-GOAL\]
*   ... I am fine with robot comments not being shown, if they are not posted on the latest patchset. \[NON-GOAL\]
*   ... I would like to be able to replace robot comments from a previous attempt on the same patchset.
*   ... I would like to link robot comments to CI runs and labels.
