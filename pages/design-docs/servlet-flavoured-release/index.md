---
title: ""
permalink: design-docs/servlet-flavoured-release.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Design Doc - Gerrit Servlet-Flavoured Release

Gerrit's migration from `javax.servlet` to `jakarta.servlet`, executed as a
phased, provable transition instead of a flag day: both servlet flavours
build from one source tree, plugins declare compatibility through a
transitional loader marker, and every phase preserves a machine-checked
invariant (the default WAR stays byte-for-byte identical through the source
flips). The lifecycle ends where it began — a single, unflavoured,
jakarta-native codebase — with each boundary step prepared ahead of time as
a reviewable change.

### Status at a glance

| Step | Gerrit topic | State |
|---|---|---|
| Servlet API de-leak / neutral-plugin classification (prerequisite) | [`de-leak-servlet-api`](https://gerrit-review.googlesource.com/q/topic:de-leak-servlet-api) | in review |
| Flavoured build (both WARs from one tree) | [`ee11-flavour`](https://gerrit-review.googlesource.com/q/topic:ee11-flavour) | in review |
| Canonical sources → jakarta (bridges reversed) | [`jakarta-canonical`](https://gerrit-review.googlesource.com/q/topic:jakarta-canonical) | in review |
| Default flip: `release.war` = jakarta | [`flip-ee11-to-default-flavour`](https://gerrit-review.googlesource.com/q/topic:flip-ee11-to-default-flavour) | prepared; lands at a major release |
| EE8 flavour removed | [`drop-ee8-flavour`](https://gerrit-review.googlesource.com/q/topic:drop-ee8-flavour) | prepared; one train later |
| Loader marker contract removed | [`drop-flavour-markers`](https://gerrit-review.googlesource.com/q/topic:drop-flavour-markers) | prepared; one train after that |
| Last javax bridges removed (JGit, Gitiles) | [`drop-ee8-bridges`](https://gerrit-review.googlesource.com/q/topic:drop-ee8-bridges) | prepared; when javax consumers migrated |
| Flavour build machinery removed | [`drop-flavour-machinery`](https://gerrit-review.googlesource.com/q/topic:drop-flavour-machinery) | prepared; the endgame |

### The lifecycle at a glance

![Servlet-flavour lifecycle: from EE8-only through two flavours back to a single jakarta-native codebase](/images/servlet-flavoured-release-lifecycle.png)

Stage 2 is the flavoured build (`ee11-flavour`), stage 3 the canonical
flip (`jakarta-canonical`) — the pivot after which every later step is
removing scaffolding. The remaining stages are the prepared boundary
changes, tearing the scaffolding down in this exact order:
`drop-ee8-flavour` → `drop-flavour-markers` → `drop-ee8-bridges` →
`drop-flavour-machinery`.

* [Motivation](/design-docs/servlet-flavoured-release-motivation.html)
* [Proposed solution](/design-docs/servlet-flavoured-release-solution.html)
* [Library flavours](/design-docs/servlet-flavoured-release-solution-libraries.html)
* [Plugin flavours and plugin-manager](/design-docs/servlet-flavoured-release-solution-plugins.html)
* [End-to-end experience](/design-docs/servlet-flavoured-release-experience.html)
* [Implementation notes — Bazel build machinery](/design-docs/servlet-flavoured-release-implementation-notes.html)
* [Conclusion](/design-docs/servlet-flavoured-release-conclusion.html)
