---
title: "Design Doc - CI Reboot - Use Cases"
permalink: design-docs/dynamic-submit-type-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/dynamic-submit-type
---

# Dynamic Submit Type - Use Cases

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



## <a id="use-cases"> Use Cases

### <a id="uc-topics">UC1: Merging topics

As a user I would like ...

*   ... [to merge the whole topic if topic is set regardless of the default submit-type.](https://groups.google.com/g/repo-discuss/c/TVOrZW9-vVQ/m/e8aFZucLAwAJ)

### <a id="uc-branch">UC2: Branch restriction level

As a user I would like ...

*   ... [to set submit-type based on how restricted the branch is.](https://groups.google.com/g/repo-discuss/c/mRAiu0gJfDM/m/OIUYwZXmAgAJ)

### <a id="uc-files">UC3: Files changed

As a user I would like ...

*   ... [to set submit-type based on which files are changed.](https://groups.google.com/g/repo-discuss/c/TVOrZW9-vVQ/m/-cqQYdX3AwAJ)

