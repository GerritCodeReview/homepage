---
title: ""
permalink: design-docs/servlet-flavoured-release-experience.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# End-to-end experience

This page describes the **two-flavour era** — the tree as it builds while
both flavours ship. The prepared boundary changes that end this era are
listed in the [Conclusion](/design-docs/servlet-flavoured-release-conclusion.html).

This page walks through the flavoured release as it is **actually built** today.
The core build path is uploaded for review under the
[`ee11-flavour`](https://gerrit-review.googlesource.com/q/topic:ee11-flavour)
Gerrit topic, the canonical-source convergence under
[`jakarta-canonical`](https://gerrit-review.googlesource.com/q/topic:jakarta-canonical),
with remaining publication wiring called out below.

## Building both flavours in one invocation

A single Bazel command produces both WARs:

```sh
bazel build release release-ee11
```

* `bazel-bin/release.war` — the EE8 (`javax.servlet`) flavour, the **unchanged
  default**.
* `bazel-bin/release-ee11.war` — the EE11 (`jakarta.servlet`) flavour.

The same pairing exists for the other WAR targets: `gerrit` / `gerrit-ee11` and
`headless` / `headless-ee11`. The two builds run side by side in one invocation;
there is no second checkout, no `next` branch, and no separate configure step.

### How one command yields two flavours

The servlet flavour is a single Bazel build setting,
`@com_googlesource_gerrit_bazlets//flags:flavour` (`ee8` default, `ee11`). Every
flavour-bearing dependency — the servlet API, the Jetty adapter, the Guice tier,
the JGit and Gitiles servlet libraries, and Gerrit's generated `httpd` boundary —
selects on it.

The key to the single-invocation build is that the **`-ee11` targets carry their
own configuration transition**: `release-ee11` flips the flavour setting to
`ee11` for *its own* dependency graph, while `release` stays on the `ee8`
default. So both towers are built consistently in the same `bazel build`, each
entirely on its own flavour, and the EE8 default keeps the same servlet
dependency tier and jar set as a non-flavoured build.

For the full wiring — how the flag, `config_setting`s, the transition,
`select()`, `target_compatible_with`, and the servlet-flavour toolchain fit
together — see
[Implementation notes — Bazel build machinery](/design-docs/servlet-flavoured-release-implementation-notes.html).

### The global flag is an escape hatch — not normally needed

Because the `-ee11` targets self-select the flavour, you do **not** pass a flag
to build the EE11 WAR. The flag still exists as an escape hatch to flip the
*whole* build to one flavour:

```sh
# Rarely needed: forces every target in the build to EE11.
bazel build --@com_googlesource_gerrit_bazlets//flags:flavour=ee11 release
```

In day-to-day use this is unnecessary — `bazel build release release-ee11`
already gives you both flavours.

## Running a flavour (operator)

Deploy exactly one WAR. `release.war` is the EE8 runtime for current operators
and their existing `javax.servlet` plugins, unchanged. `release-ee11.war` is the
EE11 runtime. A single runtime is exactly one flavour; the two namespaces are
never on the same classpath.

Core plugins are bundled in the matching flavour automatically:
`release-ee11.war` carries either a jakarta plugin jar (for example
`gitiles-ee11.jar`) or an audited servlet-neutral jar marked
`Gerrit-Flavour: any`. The runtime plugin **name** is unchanged — the loader
reads it from the `Gerrit-PluginName` manifest entry, not the file name — so
`gitiles-ee11.jar` still loads as the `gitiles` plugin.

## Flavouring a plugin in one line (author)

For a plugin author, adding the current jakarta flavour is a one-line change. A
servlet-coupled plugin that already builds with:

```python
gerrit_plugin(
    name = "my-plugin",
    srcs = glob(["src/main/java/**/*.java"]),
    ...
)
```

gains its EE11 flavour by adding a sibling target that reuses the
**same canonical sources** and sets one attribute:

```python
gerrit_plugin(
    name = "my-plugin-ee11",
    srcs = glob(["src/main/java/**/*.java"]),  # same canonical EE8 sources
    flavour = "ee11",
    ...
)
```

`flavour = "ee11"` makes the shared macro do everything the current jakarta
flavour needs:

* run the `to_jakarta` transform over the plugin's sources
  (`javax.servlet` → `jakarta.servlet`), keeping package names and line numbers;
* inject `Gerrit-Flavour: ee11` into the plugin manifest;
* compile against the **jakarta** plugin API;
* wrap the jar in the EE11 build configuration, so it self-selects the
  jakarta servlet/Jetty/Guice tiers.

Both flavours then build together, again with no flag:

```sh
bazel build //plugins/my-plugin:my-plugin //plugins/my-plugin:my-plugin-ee11
```

The EE11 jar is **generated** from the canonical EE8 source — no fork,
no second source tree, no hand-maintained namespace copy. The only plugins that
need more than this are those whose bundled library is itself split across
namespaces (Javamelody): their `-ee11` target points at the jakarta library
line, and everything else is identical.

### After migrating the plugin's sources: reverse the bridge

When the plugin later migrates its canonical sources to `jakarta.servlet`, the
same macro reverses direction — the canonical sources feed the EE11 jar
directly, and the EE8 jar becomes the generated one:

```python
gerrit_plugin(
    name = "my-plugin",            # EE8 jar, generated via to_javax
    srcs = SRCS,                   # canonical jakarta sources
    canonical = "jakarta",
    flavour = "ee8",
    ...
)

gerrit_plugin(
    name = "my-plugin-ee11",       # EE11 jar, from the canonical sources
    srcs = SRCS,
    canonical = "jakarta",
    dir_name = "my-plugin",
    flavour = "ee11",
    ...
)
```

This is how the two servlet-coupled core plugins, `gitiles` and
`plugin-manager`, build today: jakarta-canonical with a generated EE8 backward
bridge, mirroring the JGit and Gitiles libraries. Artifact names and both WARs'
contents are unchanged by the flip — only which side is source and which is
generated swaps.

## Plugins migrated so far

Three plugin migrations exercise the mechanism, one of each kind:

1. **`gitiles`** — core plugin (servlet-coupled; jakarta-canonical with a
   generated EE8 twin; its EE11 flavour consumes the canonical jakarta
   `gitiles-servlet` 2.x).
2. **`plugin-manager`** — core plugin (likewise jakarta-canonical with a
   generated EE8 twin).
3. **`javamelody`** — a custom (non-core) plugin classified as
   **servlet/filter-coupled**, and the first to use the
   separately-built-per-flavour path (the split `javamelody` 1.x/2.x library).
   It also exposes a **standalone build mode** (built outside the Gerrit tree
   against the published plugin API), and that mode extends to the EE11 flavour:
   once its module deps declare `gerrit-plugin-api-ee11`,
   `gerrit_plugin(flavour = "ee11", ...)` produces the jakarta plugin standalone
   exactly as the in-tree build does. This makes javamelody the intended
   end-to-end proof of the publishing story: a real servlet-coupled custom plugin
   building its EE11 flavour standalone against the released jakarta API. (The
   standalone `-ee11` artifact dependency and the Maven Central publication of
   `gerrit-plugin-api-ee11` are the remaining wiring.) Its endgame is
   prepared too: with the flavour machinery retired, javamelody converges to
   a single plain jakarta plugin against `javamelody-core` 2.x — the same
   convergence the core plugins make.

Every other core plugin bundled in `release-ee11.war` is servlet-neutral and is
now marked `Gerrit-Flavour: any`, so the EE11 loader accepts it under either
flavour: `replication`, `webhooks`, `hooks`, `reviewnotes`, `singleusergroup`,
`download-commands`, `commit-message-length-validator`, `codemirror-editor` and
`delete-project`. Only the two servlet-coupled core plugins — `gitiles` and
`plugin-manager` — are built per-flavour (`ee11`). So `release-ee11.war` loads
its full bundled plugin set: `gitiles-ee11` / `plugin-manager-ee11` by their
`ee11` marker, and the rest by `any`.

## Publishing to Maven Central (standalone plugin builds)

In-tree builds are not the whole story: a plugin can also be built **standalone**,
outside the Gerrit source tree, against the published Gerrit plugin API on Maven
Central. For that mode to work in the EE11 flavour, the jakarta plugin API has to
be published too.

So the release should publish the jakarta artifacts **side by side** with the
EE8 ones — same group and version, distinguished by the current `-ee11`
artifactId suffix:

| EE8 (default) | EE11 (jakarta) |
|---|---|
| `com.google.gerrit:gerrit-war` | `com.google.gerrit:gerrit-war-ee11` |
| `com.google.gerrit:gerrit-plugin-api` | `com.google.gerrit:gerrit-plugin-api-ee11` |

The EE11 WAR comes straight from the self-transitioning `//:release-ee11` target,
and the EE11 plugin-API jar/sources/javadoc are each built under the same
`flavour=ee11` transition, so both flavours can be produced and staged in one
invocation. Once published, a standalone EE11 plugin build depends on
`gerrit-plugin-api-ee11` exactly as a standalone EE8 plugin depends on
`gerrit-plugin-api` — the `gerrit_plugin(flavour = "ee11", ...)` macro selects the
jakarta API automatically.

## Verifying a flavour

The servlet namespace is visible in the built artifact: the jars inside
`release-ee11.war` reference `jakarta/servlet` and contain no `javax/servlet`,
and the reverse holds for `release.war`. A byte comparison of the two WARs shows
the only differences are exactly the flavour boundary — the servlet API, the
Jetty adapter, the Guice tier, the JGit/Gitiles servlet jars, and the
per-flavour plugin jars — confirming the two towers are otherwise identical.

## CI/CD implication: the test suite runs twice

A servlet-facing test is only meaningful in one servlet namespace at a time, so
each one has an EE8 and an EE11 incarnation, and CI covers both. The key to
keeping this painless is that **both passes are plain wildcards**.

The per-flavour targets — the servlet-boundary libraries (`httpd-ee11`,
`oauth-ee11`, `openid-ee11`, `init-ee11`, `jetty-ee11`) and the per-flavour
test suites (`httpd_tests` / `httpd_tests-ee11`, `pgm_tests` /
`pgm_tests-ee11`, the acceptance servlet-boundary groups `filter`,
`api_plugin`, `rest_bindings` and their `-ee11` twins, ...) — each compile in
exactly one configuration: the `-ee11` targets from the canonical jakarta
sources against the Guice-7/jakarta tier, the default targets from the
transform-generated javax sources against the EE8 tier. So each carries a
**`target_compatible_with` guard on its flavour**: in the other flavour's
configuration Bazel reports it *incompatible* and **skips** it (it does not
fail), and in its own configuration it runs.

Since the tree-wide source convergence, `javax.servlet` exists only inside the
`ee8/` overlay packages and every servlet-bearing target is flavoured, so the
EE11 pass is a full wildcard too:

```sh
# EE8 (default): the EE11 twins are skipped automatically -- stays green.
bazelisk test //...

# EE11: the same wildcard under the flavour flag; the EE8 twins are skipped.
bazelisk test --@com_googlesource_gerrit_bazlets//flags:flavour=ee11 //...
```

Because the guard is *conditional on the flavour*, each target shows up exactly
when its flavour is active — neither pass has to enumerate or exclude targets
by hand. (The `-ee11` *build/publish* targets — `release-ee11`, the `-ee11`
plugin jars and APIs — self-transition and need no flag at all; only the *test*
passes take the flag, because a test target cannot self-transition.)

So CI runs the suite twice: one flagless EE8 wildcard and one EE11 wildcard
under the flag. Non-servlet tests are flavour-neutral and ride along in both
passes; sources that only need HTTP status constants use
`org.apache.http.HttpStatus` instead of a servlet import, keeping them
flavour-neutral by construction.
