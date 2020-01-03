---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

## <a id="use-cases"> Use cases

The attention-set feature described in [SDesign Doc - Attention Set - Use Cases](use-cases.md)
is an innovative functionality for the future of Gerrit Code Review because of the following
characteristics:

1. Define clarity on who is expected to take the next action on a change.
2. Allows assignment of responsibility on reviewers.
3. Optimize the prioritization of work of the reviewer with a clearer UI.

The migration phase from the assignee feature has been carefully discussed and taken into
consideration, so that existing large, heavy users of that feature can continue using it
and, at the same time, could have some exposure to the attention set and experiment for
future adoption.

## <a id="solution-design"> Solution design

The user-interface proposed looks clean and good enough as a first iteration of the new
attention set functionality. It is not expected to be perfect for everyone at the beginning
but can be later on refined in subsequent releases of Gerrit beyond v3.2. The success of
the adoption of the attention set will also be measured on how the interface will be able
to evolve based on user feedback.

The workflow proposed looks reasonable and will allow common-sense defaults that will guide
new users on what is expected from them.

The implementation would need further details on how the whole feature is going to be
designed in terms of API, plugin extensions and scalability in multi-site deployments.
Also, the migration of existing storage (e.g. reviewed flag H2 table or external DBMS) would
need to be assessed and managed properly during the design and implementation phase.

Extensions and integrations with other plugins (e.g. owners, reviewers) would need to be
at least designed and defined in the Plugin API interface.

## <a id="implementation-plan"> Implementation Plan

Ben Rohlfs <brohlfs@google.com> from Google is driving the implementation, which is expected to
involve other Google engineers and potentially external contributors. The deadline for the first
release of the attention-set is Gerrit v3.2 (Apr/May 2020).
