---
title: "Design Doc - CI Reboot - Use Cases"
permalink: design-docs/dynamic-submit-type-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
folder: design-docs/dynamic-submit-type
---

# Dynamic Submit Type - Use Cases

This is a continuation of the efforts to replace Prolog in
[Composable Submit Requirements](/design-docs/ci-reboot-composable-submit-requirements-solution.html).

## <a id="objective">Objective

Improve user, admin and project owner experience when configuring dynamic submit-type.

## <a id="background">Background

Prolog has historically been a powerful way to configure setting dynamic submit types.
However Prolog's flexibility comes with a large complexity and readability price and
the submit-rule parts of Prolog were replaced by [Composable Submit Requirements](/design-docs/ci-reboot-composable-submit-requirements-solution.html)
in [Gerrit v3.6](https://www.gerritcodereview.com/3.6.html#submit-requirements),
Prolog rules have been deprecated since then.

One use-case that Composable Submit Requirements doesn't solve is that Prolog allows
you to dynamically set submit-type.
When investigating the possibility to move all Prolog evaluation into a plugin, using
existing Extension points for submit-rules, it was discovered that there's no
extension-point for dynamically setting submit-type.
Removing Prolog support in Gerrit core would leave this use-case unfulfilled.

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

