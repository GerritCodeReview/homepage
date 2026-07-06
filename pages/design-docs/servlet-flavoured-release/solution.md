---
title: ""
permalink: design-docs/servlet-flavoured-release-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Proposed Solution

This page describes the **two-flavour era**; the prepared boundary changes
that end it are listed in the
[Conclusion](/design-docs/servlet-flavoured-release-conclusion.html).

Produce two release flavours from one Gerrit source tree:

| Artifact | Servlet stack | Audience |
|---|---|---|
| `release.war` (default) | Servlet API 4.0.1, `javax.servlet`, Jetty 12 EE8, Guice 6.0 | Current operators and existing plugins. |
| `release-ee11.war` (opt-in) | Servlet API 6.1.0, `jakarta.servlet`, Jetty 12 (jakarta), Guice 7.0 | Sites whose plugin set is jakarta-ready. |

Within the tree the jakarta targets carry the working `-ee11` suffix, but no
`-ee11` name is ever *published*: Maven publication of the jakarta artifacts
lands together with the default flip, so the shipped scheme is the JGit /
Gitiles one — unsuffixed artifacts are jakarta (`gerrit-war`,
`gerrit-plugin-api`) and the legacy flavour carries an `-ee8` suffix for its
one-train deprecation window. See
[End-to-end experience](/design-docs/servlet-flavoured-release-experience.html#publishing-to-maven-central-standalone-plugin-builds).

A single runtime loads exactly one flavour; the two are never on the same
classpath. The core build path is implemented and uploaded for review under the
[`ee11-flavour`](https://gerrit-review.googlesource.com/q/topic:ee11-flavour)
Gerrit topic, and the canonical-source convergence on top of it under the
[`jakarta-canonical`](https://gerrit-review.googlesource.com/q/topic:jakarta-canonical)
topic: the prerequisite JGit and Gitiles servlet flavours are published,
and a single `bazel build release release-ee11` produces **both** WARs from the
one source tree — the EE8 `release.war` unchanged and the opt-in
`release-ee11.war` built alongside it, with no fork, no `next` branch, and no
command-line flag. The
[End-to-end experience](/design-docs/servlet-flavoured-release-experience.html)
walks through the build, the operator runtime, and the two-line plugin
flavour contract (the jar and its executed test twin). Finishing the remaining plugin and publication wiring, then rolling
the EE11 flavour out to operators, are the remaining steps.

## Architecture

Each WAR is a consistent single-flavour tower:

```text
release.war (EE8 / javax.servlet)
  Gerrit (EE8, generated from the canonical jakarta sources)
   -> jgit-servlet-ee8 (generated from JGit's canonical jakarta sources)
   -> gitiles plugin (EE8, generated from the canonical jakarta plugin sources)
       -> gitiles-servlet 1.6.0 (javax, frozen line; successor:
          the bridged gitiles-servlet-ee8 2.x)
   -> javamelody plugin (EE8)
       -> javamelody-library 1.x (javax)
   -> javax.servlet-api 4.0.1, Jetty 12 EE8, Guice 6

release-ee11.war (EE11 / jakarta.servlet)
  Gerrit (jakarta, canonical)
   -> jgit-servlet (canonical, jakarta)
   -> gitiles-ee11 plugin (canonical sources)
       -> gitiles-servlet 2.x (canonical, jakarta)
   -> javamelody-ee11 plugin
       -> javamelody-library 2.x (jakarta)
   -> jakarta.servlet-api 6.1.0, Jetty 12 (jakarta), Guice 7
```

All bridges now point the same way — **backward** (`to_javax`), the shape JGit
pioneered:

* **JGit** is `jakarta.servlet`-canonical and generates its `.ee8` bundles for
  the default WAR.
* **Gitiles** is `jakarta.servlet`-canonical as of `gitiles-servlet` 2.0.0 and
  generates a `gitiles-servlet-ee8` twin from the same sources, so EE8
  consumers keep tracking current Gitiles code instead of the frozen 1.6.x
  line.
* **Gerrit** core completed the convergence in the `jakarta-canonical` series:
  the servlet boundary (httpd, `util/http`, `pgm/http/jetty`, the plugin
  loader's servlet layer, and the servlet-facing tests) is written against
  `jakarta.servlet` 6.1, and the EE8 twins behind the unchanged `release.war`
  are transform-generated. The few classes with no mechanical javax form live
  as hand-written twins in `ee8/` overlay packages.

The design originally predicted this as a convergence — each repository would
start with the least-divergent bridge from wherever its canonical sources sat
(Gerrit began `javax`-canonical with a *forward* bridge), and flip to the
backward bridge once its sources migrated. That prediction has now played out
for all three repositories: no forward bridge remains, and the migration
changed neither artifact names nor WAR contents, which the per-WAR jar-set
guard tests prove. Tree-wide, `javax.servlet` imports exist **only** inside the
`ee8/` overlay packages; every other source file is jakarta (or servlet-free),
so the whole tree also builds and tests under the global
`--flavour=ee11` flag.

The servlet-facing libraries and the plugin ecosystem each provide a matching
flavour:

* [Library flavours](/design-docs/servlet-flavoured-release-solution-libraries.html)
  — JGit and Gitiles.
* [Plugin flavours and plugin-manager](/design-docs/servlet-flavoured-release-solution-plugins.html).
* [End-to-end experience](/design-docs/servlet-flavoured-release-experience.html)
  — building both WARs, running a flavour, and the two-line plugin flavour contract (jar + tests).
