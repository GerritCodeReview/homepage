---
title: "Design Doc - Dynamic Submit Types: Configurable By Branch - Solution"
permalink: design-docs/dynamic-submit-types-solution-configurable-by-branch.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Configurable By Branch


## <a id="objective"> Objective

The [use cases doc](design-docs/dynamic-submit-type-use-cases.html) outlines
the use-cases this solution would adress:
* [Submit type by branch](design-docs/dynamic-submit-type-use-cases.html#uc-branch).
* [Submit type depending on changed files](design-docs/dynamic-submit-type-use-cases.html#uc-files).


## <a id="project-config"> Project Configuration

### <a id="default-type"> Default Submit Type

The concept of a default submit-type should for backwards compatibility remain the same
as how the submit-type is currently configured for a project:

```
[submit]
	action = rebase if necessary
```
### <a id="dynamic-type"> Dynamic Submit Type

Reuse the pattern of ref-access and set submit-type for all matching refs

```
[submit "refs/heads/master"]
  action = Fast Forward Only
[submit "refs/heads/dev/*]
  action = Rebase If Necessary
[submit "^refs/heads/topic.*$]
  action = Merge Always
```

## <a id="issues"> Possible issues

### <a id="issues-match-order"> Match Order

This solution has the same strengths and drawback as the access-rules evaluation.
It is unclear which configuration has the "last say".

Suggestion is to opt for "most explicit match", same as the access system.

### <a id="issues-flexibility"> Flexibility

This caters to a specific use-case and has less of the flexibility that Prolog offers today.
