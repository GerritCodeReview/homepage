---
title: "Design Doc - Dynamic Submit Types: Topic Configuration - Solution"
permalink: design-docs/dynamic-submit-types-solution-topic-configuration.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Configurable For Topic


## <a id="objective"> Objective

The [use cases doc](design-docs/dynamic-submit-type-use-cases.html) outlines
the use-cases this solution would adress:
* [Submit type for topic](design-docs/dynamic-submit-type-use-cases.html#uc-topics).


## <a id="project-config"> Project Configuration

### <a id="default-type"> Default Submit Type

The concept of a default submit-type should for backwards compatibility remain the same
as how the submit-type is configured for a project:

```
[submit]
	action = rebase if necessary
```
### <a id="dynamic-type"> Topic submit-type

A specific setting under `submit` configuration that sets the submit-type for topic.

```
[submit]
  action = Fast Forward Only
  topicAction = Merge Always
```

## <a id="issues"> Possible issues

### <a id="issues-match-order"> Part of topic or whole topic

Should the configuration only take effect when `submit whole topic` is used?
`submitWholeTopicAction`?
