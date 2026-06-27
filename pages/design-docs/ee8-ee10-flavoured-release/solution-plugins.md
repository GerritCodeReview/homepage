---
title: ""
permalink: design-docs/ee8-ee10-flavoured-release-solution-plugins.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Plugin flavours and plugin-manager

Plugins that touch servlet APIs publish one artifact per flavour, each marked
with a `Gerrit-Flavour: ee8` or `Gerrit-Flavour: ee10` entry in the plugin JAR's
`META-INF/MANIFEST.MF`; audited servlet-neutral plugins may declare
`Gerrit-Flavour: any` and ship a single artifact.

Many plugins touch `javax.servlet` only incidentally — for example importing
`HttpServletResponse` solely for HTTP status constants. A separate
[de-leak servlet API](https://gerrit-review.googlesource.com/q/topic:de-leak-servlet-api)
effort removes that incidental surface (switching to non-servlet status constants
and the like) in both core and plugins, after which such plugins are genuinely
servlet-neutral and qualify for a single `Gerrit-Flavour: any` artifact.

## Classification

Each plugin is classified before it claims a flavour:

* **Servlet-neutral** — no servlet/filter API, no Guice servlet binding, no
  flavour-specific JGit/Gitiles servlet dependency: one `any` artifact.
* **Servlet/filter-coupled** — imports `javax.servlet`/`jakarta.servlet`,
  extends `HttpServlet`, implements `Filter`, or binds servlets/filters through
  Guice: one artifact per flavour (`ee8` and `ee10`).
* **Unknown** — not yet audited: treated as EE10-incompatible until classified.

For example, the **OAuth** plugin imports `HttpServletResponse` only for HTTP
status constants, so once de-leaked it falls in the **servlet-neutral** class and
ships a single `any` artifact. The **Javamelody** plugin is the
**servlet/filter-coupled** case: it extends Guice's `ServletModule` and wraps a
servlet `Filter`, so it must ship two artifacts — `javamelody-ee8`
(`Gerrit-Flavour: ee8`) and `javamelody-ee10` (`Gerrit-Flavour: ee10`).
`javamelody-ee10` is now built as the first **custom** dual-flavour Gerrit
plugin, alongside the migrated **core** plugins `gitiles` and `plugin-manager`
(see [End-to-end experience](/design-docs/ee8-ee10-flavoured-release-experience.html)).

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
transform. Gerrit now exposes both plugin-API flavours, and the shared
`gerrit_plugin(flavour = "ee10", ...)` build macro does the rest in one line —
it runs the transform on the plugin's sources, injects the `Gerrit-Flavour: ee10`
manifest entry, compiles against the jakarta plugin API, and wraps the target so
it self-selects the EE10 tiers (detailed in
[End-to-end experience](/design-docs/ee8-ee10-flavoured-release-experience.html)).
Hand-maintaining a separate per-flavour build is the fallback, used only when
generation cannot express the difference (as with Javamelody's split
`javamelody` library). A long-lived per-flavour branch or a separate repository
is discouraged: it reintroduces the fork and merge burden this proposal avoids
for the libraries.

## Migration path

For a plugin author the sequence is:

1. **Audit** the servlet surface (imports, `Filter`/`HttpServlet`, Guice
   `ServletModule`, flavour-specific library deps).
2. **De-leak** incidental usage; a plugin left with none is `any` and done.
3. **Classify** the rest as servlet-coupled and choose a production option above.
4. **Build** the EE10 flavour against the matching plugin API — now exposed by
   Gerrit — the Guice tier, and any split library release. For a clean namespace
   swap this is the one-line `gerrit_plugin(flavour = "ee10", ...)`.
5. **Test** each artifact on its matching WAR, and publish the
   `Gerrit-Flavour: ee10` marker only after it has run on an EE10 runtime.

## Loader and plugin-manager

A runtime is exactly one flavour, so the plugin loader should check
`Gerrit-Flavour` before classloading or injection and fail fast on a mismatch.
The marker itself is already emitted by the `gerrit_plugin` macro; the
loader-side enforcement is the remaining piece. A missing marker would be
permissive (with a warning) on the EE8 default but rejected on EE10, where a
stray `javax.servlet` plugin is unsafe.

`plugin-manager` should become flavour-aware: offering the running flavour's
artifacts plus `any`, and refusing one-click install of an incompatible plugin.
