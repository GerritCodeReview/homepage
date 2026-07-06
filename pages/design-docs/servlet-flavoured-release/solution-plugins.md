---
title: ""
permalink: design-docs/servlet-flavoured-release-solution-plugins.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Plugin flavours and plugin-manager

Plugins that touch servlet APIs publish one artifact per flavour: the EE10 jar is
marked with `Gerrit-Flavour: ee10`, while the EE8 jar may either be explicitly
marked `Gerrit-Flavour: ee8` or remain unmarked for compatibility with existing
plugins. Audited servlet-neutral plugins declare `Gerrit-Flavour: any` and ship a
single artifact.

Many plugins touch `javax.servlet` only incidentally — for example importing
`HttpServletResponse` solely for HTTP status constants. A separate
[de-leak servlet API](https://gerrit-review.googlesource.com/q/topic:de-leak-servlet-api)
effort removes that incidental surface (switching to non-servlet status constants
and the like) in both core and plugins, after which such plugins are genuinely
servlet-neutral and qualify for a single `Gerrit-Flavour: any` artifact.

## Classification

Each plugin is classified before it claims a flavour:

* **Servlet-neutral** — no servlet/filter API, no servlet namespace bytecode, no
  real servlet/filter binding, no flavour-specific JGit/Gitiles servlet
  dependency: one `any` artifact.
* **Servlet/filter-coupled** — imports `javax.servlet`/`jakarta.servlet`,
  extends `HttpServlet`, implements `Filter`, contains servlet namespace
  bytecode, or binds servlets/filters through Guice: one artifact per flavour
  (`ee8` and `ee10`).
* **Unknown** — not yet audited: treated as EE10-incompatible until classified.

For example, the **OAuth** plugin imports `HttpServletResponse` only for HTTP
status constants, so once de-leaked it falls in the **servlet-neutral** class and
ships a single `any` artifact. The **Javamelody** plugin is the
**servlet/filter-coupled** case: it extends Guice's `ServletModule` and wraps a
servlet `Filter`, so it must ship two artifacts — `javamelody` for EE8 (unmarked
or `Gerrit-Flavour: ee8`) and `javamelody-ee10` (`Gerrit-Flavour: ee10`).
`javamelody-ee10` is now built as the first **custom** dual-flavour Gerrit
plugin, alongside the migrated **core** plugins `gitiles` and `plugin-manager`
(see [End-to-end experience](/design-docs/servlet-flavoured-release-experience.html)).

Gerrit defines the flavour **contract** — one artifact per flavour, the
`Gerrit-Flavour` marker, and loader enforcement — not the per-plugin
**mechanism**. How a plugin meets the contract is left to its maintainer; in
practice there are three options:

1. **One `any` artifact** — for servlet-neutral plugins (after de-leaking); no
   per-flavour build at all.
2. **Generated per-flavour** — when the plugin is a clean namespace swap, the
   same transform the libraries use generates the other flavour from the
   canonical (major) source, so only one flavour is hand-maintained.
3. **Separately built per-flavour** — when generation cannot work because a
   bundled library is itself split across namespaces. The
   [Javamelody library](https://github.com/javamelody/javamelody), for example,
   ships in two release lines — 1.x on `javax.servlet` and 2.x on
   `jakarta.servlet`. The split is the very incompatibility this proposal
   addresses: the 1.x build fails on a jakarta container such as Tomcat 10.x
   (`NoClassDefFoundError` on `javax.servlet` types), which drove the move to
   `jakarta.servlet` in 2.0.0
   ([javamelody#1146: Configuring JavaMelody on Apache Tomcat 10.x](https://github.com/javamelody/javamelody/issues/1146)).
   So the Javamelody plugin's flavour split must follow it: `javamelody-ee8` builds
   against the 1.x line and `javamelody-ee10` against the 2.x line.

The mechanism is the plugin owner's to choose; the design does not fix one up
front. The **recommended** approach mirrors the libraries: a single source tree,
with the EE10 flavour **generated** from the canonical EE8 source by the shared
transform. The change series adds the matching plugin-API flavour, and the shared
`gerrit_plugin(flavour = "ee10", ...)` build macro does the rest in one line —
it runs the transform on the plugin's sources, injects the `Gerrit-Flavour: ee10`
manifest entry, compiles against the jakarta plugin API, and wraps the target so
it self-selects the EE10 tiers (detailed in
[End-to-end experience](/design-docs/servlet-flavoured-release-experience.html)).
Hand-maintaining a separate per-flavour build is the fallback, used only when
generation cannot express the difference (as with Javamelody's split
`javamelody` library). A long-lived per-flavour branch or a separate repository
is discouraged: it reintroduces the fork and merge burden this proposal avoids
for the libraries.

## Migration path

**Recommendation, in one line: classify your plugin first, then mark it.**

* **Servlet-neutral** (after de-leaking) — add `Gerrit-Flavour: any` and ship a
  single artifact that loads under either flavour. Nothing else to build.
* **Servlet-coupled** — ship one artifact per flavour; generate the EE10 one
  with the one-line `gerrit_plugin(flavour = "ee10", ...)`.
* **Do nothing** — an existing EE8-only plugin keeps working on the default
  flavour (its absent marker is treated as `ee8`); it is simply not offered on
  EE10 until you publish an `ee10` or `any` build.

For a plugin author the sequence is:

1. **Audit** the servlet surface (imports, `Filter`/`HttpServlet`, servlet
   namespace bytecode, Guice servlet bindings, flavour-specific library deps).
   Extending Guice's `ServletModule` is an audit trigger, not by itself proof of
   coupling; a module that only registers servlet-neutral bindings may still be
   eligible for `any` after bytecode inspection.
2. **De-leak** incidental usage; a plugin left with none is `any` and done.
3. **Classify** the rest as servlet-coupled and choose a production option above.
4. **Build** the EE10 flavour against the matching plugin API added by the change
   series, the Guice tier, and any split library release. For a clean namespace
   swap this is the one-line `gerrit_plugin(flavour = "ee10", ...)`.
5. **Test** each artifact on its matching WAR. Publish `Gerrit-Flavour: ee10`
   only after it has run on an EE10 runtime; publish `Gerrit-Flavour: any` only
   after the audit confirms the jar has no servlet namespace dependency.

## Loader and plugin-manager

A runtime is exactly one flavour, so the plugin loader checks
`Gerrit-Flavour` before classloading or injection and fails fast on a mismatch.
This enforcement now ships in core: `GerritServerFlavour` detects the running
flavour from the bundled servlet-API namespace (`jakarta.servlet` → EE10,
otherwise EE8), and `JarPluginProvider` validates each JAR's marker as it
loads. An `ee8` or `ee10` marker loads only on the matching flavour; `any`
(an audited servlet-neutral plugin) loads under both. An absent marker is
treated as `ee8`: it keeps loading unchanged on the EE8 default but is rejected
on EE10, where a stray `javax.servlet` plugin is unsafe. The marker itself is
emitted by the `gerrit_plugin` macro's `flavour` attribute.

`plugin-manager` should become flavour-aware: offering the running flavour's
artifacts plus `any`, and refusing one-click install of an incompatible plugin.
