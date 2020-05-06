---
title: ""
permalink: design-docs/instance-id-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

The [solution of introducing an instanceId configuration](/design-docs/instance-id-solution.html)
was chosen for the following reasons:

1. It is a simple solution that allows to define an instance-id.
2. It does not impact any existing Gerrit functionality, as the instance-id
   would be null by default.
3. It also creates additional flexibility for multi-master use-cases to populate
   the instance-id as preferred.
4. It does not impact 3rd party integrations (e.g. CI) because the instance-id
   won't be present in the event if not defined.
5. If instance-id is defined but not used by other 3rd party, it can be simply
   ignored.
6. There might be better fitting alternatives that require much more engineering
   work in both design and implementation. However, the proposed solution is much
   simpler and solves a problem immediately
   (see [complexity](https://gerrit-review.googlesource.com/Documentation/dev-contributing.html#_complexity)
   and [impact](https://gerrit-review.googlesource.com/Documentation/dev-contributing.html#_impact)).
7. The solution was proposed and implementation guaranteed by a long-standing
   community member (GerritForge) who can be trusted with implementation and
   benefits from the solution
   (see [community](https://gerrit-review.googlesource.com/Documentation/dev-contributing.html#_community)
   and [commitment](https://gerrit-review.googlesource.com/Documentation/dev-contributing.html#_commitment)).

## <a id="implementation-plan"> Implementation Plan

Fabio Ponciroli <ponch78@gmail.com> is driving the implementation, and it will
be ready for review in max 2 days.
If the timelines of the review process would allow it, it could be included in
Gerrit v3.2 or, worst case scenario, in v3.3.
