---
title: "Design Doc - CI Reboot: Composable Submit Requirements - Solution"
permalink: design-docs/ci-reboot-composable-submit-requirements-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Composable Submit Requirements

## <a id="objective"> Objective

Make clear to users why a change is not submittable and what can be done to make
it submittable. Make it easy for admins to configure what makes a change
submittable.

## <a id="background"> Background

In Gerrit, admins can write Prolog code to define what makes a change
submittable. It’s hard for admins - most of whom have never used Prolog before -
to get this right. On repo-discuss as well as googlesource.com we are paying a
constant support cost to help users. In addition, the Prolog engine has led to
outages in the past that are hard to diagnose (e.g. when reaching the max.
reduction limit). The UX also leaves a lot to be desired.

In 2018, the SubmitRule interface was added as an alternative to Prolog, but the
adoption suffered from an important shortcoming: Since SubmitRules need to be
implemented as a plugin, the plugin implementor needs to control when a given
rule is active, e.g. through a config flag. This makes them inflexible.

## <a id="overview"> Overview

Allow composing Submit Predicates to Submit Requirements using a lightweight,
boolean query language that defines when a requirement is applicable and when
it’s blocking. Provide a bridge between Submit Requirements and some existing
Change Predicates to have more out-of-the-box rules. Migrate all existing
rules.pl files on Gerrit-on-Borg to use Submit Rules. Disable Prolog on
googlesource.com deployment.

## <a id="scope"> Scope

This document defines the high-level design of the new system, but is by no
means complete. Smaller-scale decisions will be made during the implementation.

This document is part of a wider effort around CI integration.

## <a id="requirements"> Requirements

This document is based on a collection of requirements that involved many
community members and was led by Ben Rohlfs.

## <a id="interface"> Interface and Data Model

With this project, we add a layer on top of the existing `SubmitRule`
interface.
The existing interface is renamed to `SubmitPredicate`. The new layer is called
`SubmitRequirement` and references `SubmitPredicate` in different queries.
Plugins can continue to contribute `SubmitPredicate`.

Submit Requirements (SRs) are independent of each other and all submit
requirements must either pass or declare they aren't applicable for a change to
be submittable. SRs have three queries that work in the same way as change
queries do. One that defines applicability and one that defines a blocking
condition. The queries are built of Submit Predicates or Change Index Predicates
that can be composed together using AND, OR and NOT.

Similar to existing change queries, we do not support nesting of predicates
(using the result of one predicate as input for another) or variables:

```
// Example of a supported query
label:Code-Review+1 AND owner:foo@example.com

// Example of a unsupported query (nesting of functions/operators)
label:(find_label(),+2) AND owner:foo@example.com

// Example of a unsupported query (variables)
var lbl = label:Code-Review+1;
label:lbl AND owner:foo@example.com
```

SubmitRequirements are defined as (proto representation chosen only for
illustrative purposes):
```
message SubmitRequirement {
  string name = 1;                 // Name of the condition
  string description = 2;          // (Markdown, HTML?) Long-form description
  string applicable_condition = 3; // Query, that if it evaluates to false
                                   // will regard this requirement as irrelevant.
  string fulfilled_condition = 4;  // Query, that if it evaluates to false will
                                   // make this requirement block submission.
  string override_condition = 5;   // Query, that if it evaluates to true will
                                   // make this requirement not block submission
                                   // and mark it as overridden.
  bool can_override = 6            // If true, child projects can remove or modify
         [default = true];         // this requirement.
}
```


This data model was validated against large, complex `rules.pl` setups on
googlesource.com including Android, Fuchsia and Chromium's current rules.

Submit requirements are inherited by default and can be overridden and
deactivated in child projects unless “can_override” is set to false. This is
the equivalent of `submit_rule/submit_filter` in Prolog. We use the same
inheritance model as for labels: A rule can only be overridden in full or
disabled in full, never in parts.

Example Submit Requirement:

|Name                 |API Review                                                                                                                            |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------|
|Description          |This requirement ensures that changes that modify the API got an additional API review. API reviews are based on <url with guidelines>. Bot accounts are exempt from this requirement. Build cops can override this requirement by voting `Build-Cop-Override +1`.|
|Applicable Condition |`NOT commit_author:'service-account@google.com' AND commit_filepath_contains:'/api/.*'`                                               |
|Fulfilled Condition  |`label:API-Review,MAX_WITH_BLOCK`                                                                                                     |
|Override Condition   |`label:Build-Cop-Override,MAX_WITH_BLOCK`                                                                                         |
|Can Override         |`false`                                                                                                                            |

## <a id="labels"> Labels

Labels will serve solely as state definition and votes as state. Thus labels by
themselves have no impact on the submittability of a change. We will migrate
existing label functions, branch, ignoreSelfApproval out of label definitions
into their own SubmitRequirements. What remains inside the label definition is
score-copy configuration, name and scores as well as permissions on who can vote
(kept separately). **SubmitRequirements will then be the sole authority of
submitability.**

A new label SubmitPredicate allows to write a SubmitRequirement referencing
label votes and existing functions.

```
// Using existing function
label:Code-Review,MAX_WITH_BLOCK

// Working directly with votes
label:Code-Review+2 AND NOT label:Code-Review-2
```

Through this predicate, Gerrit will also know the relation between labels and
Submit Requirements and can base UX decisions on that. For example: Show a vote
button next to the SubmitRequirement or highlight labels that are currently
blocking submission.

It will still be possible to have labels that serve only as markers (e.g.
CQ-Ready) and have no impact on submittabilty.

## <a id="auditability"> Persistence, Auditability and Caching

Submit requirements are persisted in NoteDb when a change gets merged to enable
after-the-fact audits. SubmitRequirements don’t get re-evaluated for merged
changes, instead the state-upon-merge is presented.

SubmitRequirements will not be cached since the evaluation of the boolean
expressions is cheap. The evaluation of most predicates is cheap as well since
they are solely based on cached state of the change. Complex predicates - such
as Code Owners - have to define a caching strategy on their own, based on the
domain knowledge of the implementation.

We will continue to store the evaluation result of submit requirements in the
change index but switch from JSON to proto serialization to be in line with how
we serialize the Change entity and have a standard model for field deprecation.

## <a id="predicates"> Predicates and Evaluation

We will implement a bridge between change index predicates and submit predicates
that allows us to expose selected change index predicates as submit predicates.
This allows for a good set of base predicates. We’ll further implement any
remaining predicates from the Prolog implementation. Plugins can contribute
their own SubmitPredicates.

```
// Example of a plugin-provided predicate used together with a core predicate
pluginName:argument AND NOT label:Code-Review-2
```


The evaluation of Submit Requirements will use the existing Antlr integration
used for search queries to evaluate submit requirement queries.

## <a id="prolog"> Prolog Support

We will implement a “prolog()” SubmitPredicate that can be used to call out to
the Prolog engine from a requirement. This predicate will be able to return an
additional field (“labels”) that we serve as “labels” alongside the actual
labels on the API. This preserves the current behavior and allows for an online
migration of each rule implemented in Prolog to a new Submit Requirement. We
will continue to support this behavior for the time being.

## <a id="submit-types"> Conditional Submit Type

The current Prolog implementation allows to define the SubmitType at runtime.
We will therefore implement a plugin endpoint to allow plugins to change the
submit type of a change. The two use cases (change in directory, branch or by
certain user) will be catered by a single plugin. This will also allow moving
the Prolog interpreter into a plugin.

## <a id="submittability-mergeability"> Submittability and Mergeability

Submittability is whether or not a change has all required approvals and meets
the bar for being submitted. Mergeability is whether or not a change is
mergeable without a conflict in git, irrespective of any approvals it might
need. While this distinction will remain, the UI will show ‘Mergeability’ as an
additional submit requirement. Computing ‘Mergeability’ is much slower than
evaluating submit requirements, which is why we keep these concepts separate and
augment them only on the change page.

## <a id="ui"> UI Support for project owners

Gerrit currently offers a poor experience for admins that want to write and test
their Prolog rules forcing them to write rules.pl locally and perform a Git push
and debug in production.
For composable submit requirements, we will offer a UI to write, test and save
submit requirements. The UI will allow for project owners to add SRs. Illegal
queries will be called out directly and the UI will offer to test the
modifications against existing changes to see if they would pass or fail on
these changes. Direct modification of the configs will still be possible and
Gerrit will ensure that SRs contain valid queries using validation listeners
that act upon push.

## <a id="migration"> Migration
There are three flavours that we have to migrate to the new world:

1)  Projects that only use Labels and functions, no Prolog and no custom SubmitRules
    We’ll implement a SchemaMigration to migrate existing label functions to
    SubmitRequirements as an online migration. The migration will create one
    submit requirement for each existing, blocking label. A cleanup will remove
    Label functions.
2)  Projects that use Prolog
    We’ll implement a PrologPredicate as outlined above. The migration from (1)
    will create a “Prolog requirement” for each project that has a rules.pl file
    on the evaluation path. This allows for an online migration 1-by-1 of parts
    of the Prolog rule to a dedicated SubmitRequirement.
    Plugins that currently expose a custom prolog fact will need to expose a
    custom submit predicate instead.
3)  Projects that use custom SubmitRules by implementing the existing interface
    There aren’t many implementations of SubmitRule as of now. We’ll change the
    API of SubmitRules to SubmitPredicates. The new interface is very close to
    the old. This requires implementers of SubmitRule to make only minimal
    changes.

On the REST API and in the Gerrit UI, we will work only with the new entities.
The Prolog glue code will be contained in the backend and is narrow-scoped.
While we want to remove Prolog support from Gerrit-on-Borg, we will continue to
support the existing implementation in an open-source plugin, so that projects
that like Prolog aren't forced to move over.

## <a id="futurework"> Future Work

In a future iteration, we want to allow SubmitRequirements to expose actions
to the frontend. These turn into buttons for the user to work towards resolving
an unfulfilled requirement. For example: Users can invite reviewers who have
the permission to vote on a required label or code-owners whose approval is
missing.

## <a id="alternatives"> Alternatives Considered

* **Single query, no separation**: Instead of having individual submit rules
that are composed of predicates, we could just have a single query per project
composed of predicates that defines submittability. This would make it much
harder to show actionable results to the user or would complicate the query
evaluation to generate actionable output.
* **One query per requirement**: We could skip the
applicability_query/override_query and just have a single query that blocks if
it evaluates to false. However, we think it’s an important UX decision to make
that not all requirements apply to a given change. It also allows admins to
write simpler, more concise queries.

## <a id="commitment"> Project Plan and Commitment

The Gerrit@Google team will work on this in Q4/2020 and Q1/2021. The target
release is 3.4.