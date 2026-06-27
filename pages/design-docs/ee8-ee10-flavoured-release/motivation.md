---
title: ""
permalink: design-docs/ee8-ee10-flavoured-release-motivation.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Motivation

JGit master has already moved to `jakarta.servlet` (EE10), while Gerrit,
Gitiles, and the plugin ecosystem are still on `javax.servlet` (EE8). The
starting point is therefore already heterogeneous — not by design, but because
JGit advanced first — so consuming current JGit forces a servlet-namespace
decision. The flavour model does not create this split; it manages it (and, per
the lifecycle, converges it back to one). Gerrit's stakeholders are split on the
choice too, with equally legitimate requirements:

* Some stakeholders, along with the large existing body of `javax.servlet`
  plugins, depend on the EE8 stack (Servlet API 4.0.1, `javax.servlet`,
  Jetty 12 EE8 or a proprietary EE8-compatible servlet runtime, Guice 6.0) and
  cannot migrate on an external timetable.
* Others are ready to begin the EE10 (`jakarta.servlet`, Servlet API 6.1.0)
  transition now and should not be blocked waiting for the slower adopters.

A single default cannot serve both: moving the default to EE10 breaks the EE8
majority, while staying EE8-only indefinitely strands the early adopters.
Producing **both flavours from one source tree** — with no long-lived fork, no
`next` branch, and no duplicated codebase — is what serves both groups at once.

The plugin ecosystem widens this further: even if every operator could switch on
a single date, third-party plugin authors migrate on their own schedules, so a
site can move to `release-ee10.war` only once *its* plugins are EE10-ready.
Parallel flavours let a site whose crucial plugins are not yet ported keep
running the EE8 flavour — with its existing plugin builds unchanged — instead of
being forced to drop a plugin or postpone its Gerrit upgrade while the ecosystem
catches up.

## Precedent

Carrying two paths through a migration — and retiring the older one once the
move is complete — is not new to Gerrit. ReviewDb and NoteDb, GWT and
PolyGerrit, and ChangeScreen and ChangeScreen2 each ran side by side during
their transitions. The lesson is that every path must be a real, supported
product (built, tested, documented), not a hidden build variant — and that the
superseded one is eventually removed, just as the EE8 flavour will be.

## Origin

This in-tree dual-flavour approach mirrors Jetty 12's own EE8/EE10 architecture,
which ships both servlet flavours from a single project. The idea was raised by
Nasser Grainawi during Gerrit community discussion:

> Hmm, that's an interesting idea. Another idea geared towards the future support
> problem … was what if we followed the jetty approach in jgit/gitiles/gerrit
> and have in-tree support for both servlet-4 and servlet-6+. It's absolutely
> more overhead to maintain both and maybe it falls apart when you start looking
> at other dependencies, but it could be a path to providing a newer servlet
> version …
