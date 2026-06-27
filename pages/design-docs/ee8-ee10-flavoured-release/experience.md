---
title: ""
permalink: design-docs/ee8-ee10-flavoured-release-experience.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# End-to-end experience

This page walks through the flavoured release as it is **actually built and
used** today. The implementation is complete end to end and uploaded for review
under the
[`ee10-flavour`](https://gerrit-review.googlesource.com/q/topic:ee10-flavour)
Gerrit topic.

## Building both flavours in one invocation

A single Bazel command produces both WARs:

```sh
bazel build release release-ee10
```

* `bazel-bin/release.war` — the EE8 (`javax.servlet`) flavour, the **unchanged
  default**.
* `bazel-bin/release-ee10.war` — the EE10 (`jakarta.servlet`) flavour.

The same pairing exists for the other WAR targets: `gerrit` / `gerrit-ee10` and
`headless` / `headless-ee10`. The two builds run side by side in one invocation;
there is no second checkout, no `next` branch, and no separate configure step.

### How one command yields two flavours

The servlet flavour is a single Bazel build setting,
`@com_googlesource_gerrit_bazlets//flags:flavour` (`ee8` default, `ee10`). Every
flavour-bearing dependency — the servlet API, the Jetty adapter, the Guice tier,
the JGit and Gitiles servlet libraries, and Gerrit's generated `httpd` boundary —
selects on it.

The key to the single-invocation build is that the **`-ee10` targets carry their
own configuration transition**: `release-ee10` flips the flavour setting to
`ee10` for *its own* dependency graph, while `release` stays on the `ee8`
default. So both towers are built consistently in the same `bazel build`, each
entirely on its own flavour, and the EE8 default is byte-for-byte unchanged.

### The global flag is an escape hatch — not normally needed

Because the `-ee10` targets self-select the flavour, you do **not** pass a flag
to build the EE10 WAR. The flag still exists as an escape hatch to flip the
*whole* build to one flavour:

```sh
# Rarely needed: forces every target in the build to EE10.
bazel build --@com_googlesource_gerrit_bazlets//flags:flavour=ee10 release
```

In day-to-day use this is unnecessary — `bazel build release release-ee10`
already gives you both flavours.

## Running a flavour (operator)

Deploy exactly one WAR. `release.war` is the EE8 runtime for current operators
and their existing `javax.servlet` plugins, unchanged. `release-ee10.war` is the
EE10 runtime. A single runtime is exactly one flavour; the two namespaces are
never on the same classpath.

Core plugins are bundled in the matching flavour automatically: `release-ee10.war`
carries the jakarta plugin jars (for example `gitiles-ee10.jar`). The runtime
plugin **name** is unchanged — the loader reads it from the `Gerrit-PluginName`
manifest entry, not the file name — so `gitiles-ee10.jar` still loads as the
`gitiles` plugin.

## Flavouring a plugin in one line (author)

For a plugin author, adding an EE10 flavour is a one-line change. A
servlet-coupled plugin that already builds with:

```python
gerrit_plugin(
    name = "my-plugin",
    srcs = glob(["src/main/java/**/*.java"]),
    ...
)
```

gains its EE10 flavour by adding a sibling target that reuses the **same
canonical sources** and sets one attribute:

```python
gerrit_plugin(
    name = "my-plugin-ee10",
    srcs = glob(["src/main/java/**/*.java"]),  # same canonical EE8 sources
    flavour = "ee10",
    ...
)
```

`flavour = "ee10"` makes the shared macro do everything the flavour needs:

* run the `to_jakarta` transform over the plugin's sources
  (`javax.servlet` → `jakarta.servlet`), keeping package names and line numbers;
* inject `Gerrit-Flavour: ee10` into the plugin manifest;
* compile against the **jakarta** plugin API;
* wrap the jar in the EE10 build configuration, so it self-selects the jakarta
  servlet/Jetty/Guice tiers.

Both flavours then build together, again with no flag:

```sh
bazel build //plugins/my-plugin:my-plugin //plugins/my-plugin:my-plugin-ee10
```

The EE10 jar is **generated** from the canonical EE8 source — no fork, no second
source tree, no hand-maintained namespace copy. The only plugins that need more
than this are those whose bundled library is itself split across namespaces
(Javamelody): their `-ee10` target points at the jakarta library line, and
everything else is identical.

## Plugins migrated so far

Three plugins already ship the EE10 flavour through this mechanism, one of each
kind:

1. **`gitiles`** — core plugin (servlet-coupled; its EE10 flavour consumes the
   jakarta `gitiles-servlet` 2.0.0).
2. **`plugin-manager`** — core plugin.
3. **`javamelody`** — a custom (non-core) plugin classified as
   **servlet/filter-coupled**, and the first to use the
   separately-built-per-flavour path (the split `javamelody` 1.x/2.x library).
   It also exposes a **standalone build mode** (built outside the Gerrit tree
   against the published plugin API), and that mode was migrated to the EE10
   flavour too: its standalone build now consumes `gerrit-plugin-api-ee10` from
   Maven Central, so `gerrit_plugin(flavour = "ee10", ...)` produces the jakarta
   plugin standalone exactly as the in-tree build does. This makes javamelody the
   end-to-end proof of the publishing story: a real servlet-coupled custom plugin
   building its EE10 flavour standalone against the released jakarta API.

In addition, the `replication` and `webhooks` core plugins were de-leaked from
incidental `javax.servlet` use, so they remain a single servlet-neutral build.

## Publishing to Maven Central (standalone plugin builds)

In-tree builds are not the whole story: a plugin can also be built **standalone**,
outside the Gerrit source tree, against the published Gerrit plugin API on Maven
Central. For that mode to work in the EE10 flavour, the jakarta plugin API has to
be published too.

So the release publishes the EE10 artifacts **side by side** with the EE8 ones —
same group and version, distinguished by an `-ee10` artifactId suffix:

| EE8 (default) | EE10 (jakarta) |
|---|---|
| `com.google.gerrit:gerrit-war` | `com.google.gerrit:gerrit-war-ee10` |
| `com.google.gerrit:gerrit-plugin-api` | `com.google.gerrit:gerrit-plugin-api-ee10` |

The EE10 WAR comes straight from the self-transitioning `//:release-ee10` target,
and the EE10 plugin-API jar/sources/javadoc are each built under the same
`flavour=ee10` transition, so both flavours are produced and staged in one
invocation. A standalone EE10 plugin build then depends on
`gerrit-plugin-api-ee10` exactly as a standalone EE8 plugin depends on
`gerrit-plugin-api` — the `gerrit_plugin(flavour = "ee10", ...)` macro selects the
jakarta API automatically.

## Verifying a flavour

The servlet namespace is visible in the built artifact: the jars inside
`release-ee10.war` reference `jakarta/servlet` and contain no `javax/servlet`,
and the reverse holds for `release.war`. A byte comparison of the two WARs shows
the only differences are exactly the flavour boundary — the servlet API, the
Jetty adapter, the Guice tier, the JGit/Gitiles servlet jars, and the
per-flavour plugin jars — confirming the two towers are otherwise identical.
