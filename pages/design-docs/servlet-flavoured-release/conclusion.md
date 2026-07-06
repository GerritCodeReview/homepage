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
`bazel build release release-ee11` — with the core change series under the
[`ee11-flavour`](https://gerrit-review.googlesource.com/q/topic:ee11-flavour)
Gerrit topic. The source base has since converged on top of it, under the
[`jakarta-canonical`](https://gerrit-review.googlesource.com/q/topic:jakarta-canonical)
topic: JGit, Gitiles and Gerrit are all `jakarta.servlet`-canonical, the EE8
default is transform-generated (`javax.servlet` survives in source only in the
hand-written `ee8/` overlay packages), and the whole tree builds and tests in
either flavour — while artifact names and the shipped default WAR remain
byte-for-byte unchanged. Publishing the jakarta flavour to operators is the
step that remains.

How the lifecycle maps onto Gerrit's release cadence — one step per release
train, with the bridge direction flipping mid-way:

![Release-by-release: EE8-only, flavours introduced, bridge direction swapped, EE11-only](/images/servlet-flavoured-release-timeline.png)

The remaining lifecycle is prepared end-to-end as reviewable changes ahead of
time, so each step becomes a merge decision at its release boundary rather
than an engineering effort — one step per release train:

* **Default flip** (major release boundary) — `release.war` becomes the
  jakarta flavour and the transitional `release-ee8.war` carries the legacy
  stack for one release train; unsuffixed Maven artifacts are jakarta and the
  legacy tier takes an `-ee8` suffix (the JGit/Gitiles scheme — no `-ee11`
  name is ever minted). Topic:
  [`flip-ee11-to-default-flavour`](https://gerrit-review.googlesource.com/q/topic:flip-ee11-to-default-flavour).
* **EE8 retirement** (one train later) — the generated bridges, the `ee8/`
  overlay packages, the javax servlet/Jetty/Guice-6 tier and the `ee8`
  flavour value itself are removed; with Guice 6 gone the isolated jakarta
  dependency resolution collapses into the main one, and `javax.inject`
  drops out by itself. Topic:
  [`drop-ee8-flavour`](https://gerrit-review.googlesource.com/q/topic:drop-ee8-flavour).
* **Marker retirement** (one train after that) — the `Gerrit-Flavour`
  loader contract was machinery for the javax→jakarta namespace chasm; once
  the upgrade window closes it is migration residue, and the loader returns
  to its pre-marker form (markers in existing jars are ignored). Future
  servlet generations are version bumps inside the stable `jakarta.servlet`
  namespace, not chasms, and need no per-plugin markers. Topic:
  [`drop-flavour-markers`](https://gerrit-review.googlesource.com/q/topic:drop-flavour-markers).
* **Bridge retirement** (when the javax consumers have migrated) — Gitiles
  drops its generated `gitiles-servlet-ee8`, JGit removes its `.ee8` bridge
  bundles upstream, and the last dormant `javax.servlet` entries leave the
  shared dependency resolutions. Topic:
  [`drop-ee8-bridges`](https://gerrit-review.googlesource.com/q/topic:drop-ee8-bridges).
* **Machinery retirement** (the endgame) — with nothing left to route, the
  flavour flag, transition, toolchain seam and twin macros are removed from
  Gerrit and bazlets; only the `to_jakarta` source transform stays, for
  late-migrating javax plugins. Topic:
  [`drop-flavour-machinery`](https://gerrit-review.googlesource.com/q/topic:drop-flavour-machinery).

At the end of the cycle the project has converged back to a single, unmarked,
`jakarta.servlet`-native codebase — no forward bridge, no backward bridge, no
overlay packages, no loader contract, and finally no flavour machinery at
all — exactly the pre-flavour shape, one namespace later. Because
`jakarta.servlet` is version-stable, the next servlet generation (EE12) is
expected to arrive as an ordinary dependency bump; should a coexistence
window ever be needed again, the complete machinery documented here is one
revert away in history.
