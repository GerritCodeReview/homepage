---
title: ""
permalink: design-docs/ee8-ee10-flavoured-release-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Proposed Solution

Produce two release flavours from one Gerrit source tree:

| Artifact | Servlet stack | Audience |
|---|---|---|
| `release.war` (default) | Servlet API 4.0.1, `javax.servlet`, Jetty 12 EE8, Guice 6.0 | Current operators and existing plugins. |
| `release-ee10.war` (opt-in) | Servlet API 6.1.0, `jakarta.servlet`, Jetty 12 EE10, Guice 7.0 | Sites whose plugin set is EE10-ready. |

Both flavours are published to Maven Central side by side under the same group
and version, distinguished by an `-ee10` artifactId suffix — the WAR as
`gerrit-war` / `gerrit-war-ee10`, and (so that plugins can be built **standalone**
against the matching API) the plugin API as `gerrit-plugin-api` /
`gerrit-plugin-api-ee10`. See
[End-to-end experience](/design-docs/ee8-ee10-flavoured-release-experience.html#publishing-to-maven-central-standalone-plugin-builds).

A single runtime loads exactly one flavour; the two are never on the same
classpath. This end state is **now implemented end to end** and uploaded for
review under the
[`ee10-flavour`](https://gerrit-review.googlesource.com/q/topic:ee10-flavour)
Gerrit topic: the prerequisite JGit and Gitiles servlet flavours are published,
and a single `bazel build release release-ee10` produces **both** WARs from the
one source tree — the EE8 `release.war` unchanged and the opt-in
`release-ee10.war` built alongside it, with no fork, no `next` branch, and no
command-line flag. The
[End-to-end experience](/design-docs/ee8-ee10-flavoured-release-experience.html)
walks through the build, the operator runtime, and the one-line plugin
flavouring. Rolling the EE10 flavour out to operators is the remaining step.

## Architecture

Each WAR is a consistent single-flavour tower:

```text
release.war (EE8 / javax.servlet)
  Gerrit (EE8, canonical)
   -> jgit-servlet-ee8 (generated from JGit's canonical jakarta sources)
   -> gitiles-ee8-plugin
       -> gitiles-servlet 1.6.0 (javax, frozen line)
   -> javamelody-ee8-plugin
       -> javamelody-library 1.x (javax)
   -> javax.servlet-api 4.0.1, Jetty 12 EE8, Guice 6

release-ee10.war (EE10 / jakarta.servlet)
  Gerrit (EE10, generated)
   -> jgit-servlet (canonical, jakarta)
   -> gitiles-ee10-plugin
       -> gitiles-servlet 2.0.0 (canonical, jakarta)
   -> javamelody-ee10-plugin
       -> javamelody-library 2.x (jakarta)
   -> jakarta.servlet-api 6.1.0, Jetty 12 EE10, Guice 7
```

The bridge direction is asymmetric, because each repository starts from where
its canonical sources already sit:

* **Backward-bridge** — JGit and, as of `gitiles-servlet` 2.0.0, Gitiles are
  `jakarta.servlet`-canonical. JGit generates the older EE8 (`to_javax`) flavour
  for the default WAR; Gitiles froze its `javax.servlet` line at 1.6.0 when it
  made jakarta canonical, so the EE8 WAR pins that release.
* **Forward-bridge** — Gerrit core is still `javax.servlet`-canonical, so it
  generates the newer EE10 (`to_jakarta`) flavour — its `httpd` servlet boundary
  and the in-tree plugin builds — for the EE10 WAR.

Each repository takes the least-divergent path from its own canonical flavour.
Gitiles is the first to complete the predicted convergence: once a repository's
canonical flavour flips to `jakarta.servlet`, its bridge becomes a
backward-bridge like JGit's, and as the rest follow the asymmetry disappears.

The servlet-facing libraries and the plugin ecosystem each provide a matching
flavour:

* [Library flavours](/design-docs/ee8-ee10-flavoured-release-solution-libraries.html)
  — JGit and Gitiles.
* [Plugin flavours and plugin-manager](/design-docs/ee8-ee10-flavoured-release-solution-plugins.html).
* [End-to-end experience](/design-docs/ee8-ee10-flavoured-release-experience.html)
  — building both WARs, running a flavour, and one-line plugin flavouring.
