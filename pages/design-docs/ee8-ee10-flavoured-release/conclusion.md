---
title: ""
permalink: design-docs/ee8-ee10-flavoured-release-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

Some major Gerrit stakeholders are not in a position to migrate to EE10 any time
soon, while others are ready to adopt it now. The proposal is to release both
the EE8 and EE10 flavours from a single source tree during the transition, so
that neither group blocks the other. This is no longer only a proposal: both
WARs already build side by side from the one source tree — `bazel build release
release-ee10` — and the complete change series is uploaded for review under the
[`ee10-flavour`](https://gerrit-review.googlesource.com/q/topic:ee10-flavour)
Gerrit topic, with three plugins already migrated (the `gitiles` and
`plugin-manager` core plugins and the `javamelody` custom plugin). Publishing the
EE10 flavour to operators is the step that remains.

Once all Gerrit stakeholders have migrated to EE10, the EE8 flavour will be
discontinued, converging the project back to a single servlet flavour.
