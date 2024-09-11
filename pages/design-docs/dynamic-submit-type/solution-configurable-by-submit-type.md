---
title: "Design Doc - Dynamic Submit Types: Configurable By Submit Type - Solution"
permalink: design-docs/dynamic-submit-types-solution-configurable-by-submit-type.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Configurable By Submit Type


## <a id="objective"> Objective

The [use cases doc](design-docs/dynamic-submit-type-use-cases.html) outlines
the use-cases this solution would adress:
* [Submit type by branch](design-docs/dynamic-submit-type-use-cases.html#uc-branch).
* [Submit type depending on changed files](design-docs/dynamic-submit-type-use-cases.html#uc-files).


## <a id="project-config"> Project Configuration

### <a id="default-type"> Default Submit Type

The concept of a default submit-type should for backwards compatibility remain the same
as how the submit-type is configured for a project:

```
[submit]
	action = rebase if necessary
```
### <a id="dynamic-type"> Dynamic Submit Type

For flexibility we could opt for a similar pattern as for Submit Requirements, i.e.
the submit type is to be applied if the change matches a query.

```
[submit-type "fast-foward-only"]
  applicableIf = -branch:refs/meta/config AND file:pom.xml
```

## <a id="issues"> Possible issues

The flexibility of this solution comes with complexity that we need to sort out.

### <a id="issues-match-order"> Match Order

Since there's no apparent order between different configurations it is unclear how
to ensure an unambiguous interpretation of the configurations.

We could evaluate them in order and break after the first match.
Is the order guaranteed once the file is loaded into a ProjectConfig?

### <a id="issues-submit-stack"> Submit Stack

When submitting a stack it is not guaranteed that all commits match the same submit-type
configuration.
How should we deal with this case?

