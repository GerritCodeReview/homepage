---
title: ""
permalink: design-docs/servlet-flavoured-release-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

Some major Gerrit stakeholders are not in a position to migrate from EE8 any
time soon, while others are ready to adopt the jakarta servlet stack now. The
proposal is to release both flavours from a single source tree during the
transition, so that neither group blocks the other. This is no longer only a
proposal: both WARs already build side by side from the one source tree —
`bazel build release release-ee11` — and the core change series is uploaded for
review under the
[`ee11-flavour`](https://gerrit-review.googlesource.com/q/topic:ee11-flavour)
Gerrit topic, with plugin migration and publication wiring being completed
around it. Publishing the jakarta flavour to operators is the step that remains.

Once all Gerrit stakeholders have migrated to the jakarta servlet stack, the EE8
flavour will be discontinued, converging the project back to a single servlet
flavour.
