---
title: ""
permalink: design-docs/servlet-flavoured-release-motivation.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Motivation

## Why move at all

`javax.servlet` is a frozen namespace: its last release is 4.0.1, and all
servlet-API development happens under `jakarta.servlet` since the platform
moved to Eclipse. The dependency lines Gerrit builds on develop there too:
JGit master, Jetty's active EE environments, Guice 7, `gitiles-servlet` 2.x,
and downstream libraries such as javamelody 2.x are jakarta-only lines.
Staying on `javax.servlet` indefinitely means pinning ever-older releases of
those dependencies — cutting Gerrit off from their maintenance and security
flow — while every year widens the gap that eventually has to be crossed
anyway. The question is not *whether* to cross it, but *how*.

## The split that has to be managed

JGit master has already moved to `jakarta.servlet`, and Gitiles has since
followed — its `gitiles-servlet` library is `jakarta.servlet`-canonical as of
2.0.0 — while Gerrit's **default release** and the bulk of the plugin
ecosystem remain on `javax.servlet` (EE8). (Gerrit core's *sources* have since
converged to jakarta-canonical too, with the EE8 default transform-generated —
but the shipped default is unchanged.) The starting point is therefore already
heterogeneous — not by design, but because the libraries advanced first — so
consuming current JGit forces a servlet-namespace decision. The flavour model
does not create this split; it manages it (and, per the lifecycle, converges it
back to one).
Gerrit's stakeholders are split on the choice too, with equally legitimate
requirements:

* Some stakeholders, along with the large existing body of `javax.servlet`
  plugins, depend on the EE8 stack (Servlet API 4.0.1, `javax.servlet`,
  Jetty 12 EE8 or a proprietary EE8-compatible servlet runtime, Guice 6.0) and
  cannot migrate on an external timetable.
* Others are ready to begin the `jakarta.servlet` transition now and should not
  be blocked waiting for the slower adopters. The opt-in `ee11` build serves
  them: Servlet API 6.1.0 on the corresponding Jetty EE11 environment.

A single default cannot serve both: moving the default to the jakarta flavour
breaks the EE8 majority, while staying EE8-only indefinitely strands the early
adopters.
Producing **both flavours from one source tree** — with no long-lived fork, no
`next` branch, and no duplicated codebase — is what serves both groups at once.

The plugin ecosystem widens this further: even if every operator could switch on
a single date, third-party plugin authors migrate on their own schedules, so a
site can move to `release-ee11.war` only once *its* plugins are EE11-ready.
Parallel flavours let a site whose crucial plugins are not yet ported keep
running the EE8 flavour — with its existing plugin builds unchanged — instead of
being forced to drop a plugin or postpone its Gerrit upgrade while the ecosystem
catches up.

## Why gradual — and not a flag day

Controlling the migration schedule for Gerrit's stakeholders is the most
visible reason for the phased transition, but it is not the only one. The
gradual model was chosen because a single-cutover ("flag day") migration
fails this particular problem in four independent ways:

1. **The failure mode is silent and late.** A plugin compiled against the
   wrong servlet namespace does not fail at build or load time — it explodes
   mid-request with `NoClassDefFoundError`, in production, on whatever code
   path first touches a servlet type. The transition window's
   `Gerrit-Flavour` marker contract converts that into a load-time rejection
   with guidance; a flag day would convert it into simultaneous runtime
   breakage across every unported deployment.
2. **The plugin ecosystem is a collective-action problem.** Third-party
   plugin authors answer to no central authority and no shared timetable. A
   flag day requires every plugin a site depends on to be ready on the same
   date — the least-maintained plugin in the ecosystem sets everyone's pace.
   The phased model with per-plugin markers (`any`/`ee11`) decomposes one
   impossible coordinated migration into many independent, individually
   trivial ones.
3. **Each step is provable; a flag day is not.** Every phase of the gradual
   transition preserves a machine-checked invariant: the source flips kept
   `release.war` byte-for-byte identical (jar-set guard tests), the backward
   bridges produce class-for-class identical jars, and each retirement step
   removes only what its guards prove unused. A giant one-shot migration has
   no such invariant — it cannot be reviewed piecewise, bisected when
   something regresses, or verified beyond "the tests still pass". The
   boundary decisions themselves (default flip, retirements) shrink to
   small, loudly-announced changes prepared ahead of time.
4. **Every step is reversible until it isn't needed.** Before the default
   flip, everything is additive: abandoning the effort would have cost
   nothing. After the flip, the transitional `-ee8` artifacts are the
   fallback for one release train. Each retirement lands only after its
   consumers have demonstrably migrated — never on a prediction.

One more choice hides inside "gradual": gradual *in one source tree*. The
alternative gradual mechanisms — a long-lived `next` branch or a separate
repository — rot under dual maintenance and merge burden, which is exactly
how such migrations stall. In-tree flavours generated from one canonical
source keep a single history, a single review flow and a single CI, so the
transition never competes with ordinary development.

## Precedent

Carrying two paths through a migration — and retiring the older one once the
move is complete — is not new to Gerrit. ReviewDb and NoteDb, GWT and
PolyGerrit, and ChangeScreen and ChangeScreen2 each ran side by side during
their transitions. The lesson is that every path must be a real, supported
product (built, tested, documented), not a hidden build variant — and that the
superseded one is eventually removed, just as the EE8 flavour will be.

## Origin

This in-tree servlet-flavour approach mirrors Jetty 12's own
multiple-EE-environment architecture, where new servlet generations are
introduced as another environment in the same project. Gerrit uses the same
shape so future Jetty EE servlet flavours, such as EE12, can be added
by extending the flavour mapping rather than redesigning each boundary.

The idea was raised by Nasser Grainawi during Gerrit community discussion:

> Hmm, that's an interesting idea. Another idea geared towards the future support
> problem … was what if we followed the jetty approach in jgit/gitiles/gerrit
> and have in-tree support for both servlet-4 and servlet-6+. It's absolutely
> more overhead to maintain both and maybe it falls apart when you start looking
> at other dependencies, but it could be a path to providing a newer servlet
> version …
