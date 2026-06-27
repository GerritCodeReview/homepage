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

A single runtime loads exactly one flavour; the two are never on the same
classpath. This is the proposed end state; today the prerequisite
JGit/Gitiles/Gerrit bridge changes are still being reviewed and the EE10 WAR is
not yet shipped.

## Architecture

Each WAR is a consistent single-flavour tower:

```text
release.war (EE8 / javax.servlet)
  Gerrit (EE8)
   -> jgit-servlet-ee8 (generated)
   -> gitiles-ee8-plugin
       -> gitiles-servlet (canonical, EE8)
   -> javamelody-ee8-plugin
       -> javamelody-library 1.x (EE8)
   -> javax.servlet-api, Jetty 12 EE8

release-ee10.war (EE10 / jakarta.servlet)
  Gerrit (EE10)
   -> jgit-servlet (canonical, EE10)
   -> gitiles-ee10-plugin
       -> gitiles-servlet-ee10 (generated)
   -> javamelody-ee10-plugin
       -> javamelody-library 2.x (EE10)
   -> jakarta.servlet-api, Jetty 12 EE10
```

The bridge direction is asymmetric, because each repository starts from where
its canonical sources already sit:

* **Backward-bridge** — JGit is `jakarta.servlet` canonical, so it generates the
  older EE8 (`to_javax`) flavour for the default WAR.
* **Forward-bridge** — Gitiles is `javax.servlet` canonical, so it generates the
  newer EE10 (`to_jakarta`) flavour for the EE10 WAR.

Each repository takes the least-divergent path from its own canonical flavour;
once a repository's canonical flavour flips to `jakarta.servlet`, its bridge
becomes a backward-bridge like JGit's and the asymmetry disappears.

The servlet-facing libraries and the plugin ecosystem each provide a matching
flavour:

* [Library flavours](/design-docs/ee8-ee10-flavoured-release-solution-libraries.html)
  — JGit and Gitiles.
* [Plugin flavours and plugin-manager](/design-docs/ee8-ee10-flavoured-release-solution-plugins.html).
