---
title: ""
permalink: design-docs/servlet-flavoured-release-experience.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# End-to-end experience

This page walks through the **two-flavour era** as it is actually built:
the core build path is in review under the
[`ee11-flavour`](https://gerrit-review.googlesource.com/q/topic:ee11-flavour)
Gerrit topic and the canonical-source convergence under
[`jakarta-canonical`](https://gerrit-review.googlesource.com/q/topic:jakarta-canonical).
The prepared boundary changes that end this era are listed in the
[Conclusion](/design-docs/servlet-flavoured-release-conclusion.html).

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

## Flavouring a plugin: two lines per flavour (author)

If the plugin is servlet-neutral after audit, do not create twins: ship
one artifact marked `Gerrit-Flavour: any`; it needs no flavour twin —
see
[Plugin flavours and plugin-manager](/design-docs/servlet-flavoured-release-solution-plugins.html)
for the classification and the `any` path. The two-line-per-flavour
contract below is for **servlet-coupled** plugins, where each supported
runtime needs its own jar and test twin.

For a plugin author, adding the current jakarta flavour is a **two-line
contract — the artifact and its executed validation**. A servlet-coupled
plugin that already builds with:

```python
gerrit_plugin(
    name = "my-plugin",
    srcs = glob(["src/main/java/**/*.java"]),
    ...
)
```

gains its EE11 flavour in two moves: declare the **existing default
explicitly `ee8`** — jar and tests; the guard is what keeps the EE11
wildcard pass green — and add the EE11 sibling pair, all four reusing the
**same canonical sources**:

```python
gerrit_plugin(
    name = "my-plugin",
    srcs = glob(["src/main/java/**/*.java"]),
    flavour = "ee8",                           # explicit: marker + guard
    ...
)

gerrit_plugin_tests(
    srcs = glob(["src/test/java/**/*.java"]),
    flavour = "ee8",
    plugin = "my-plugin",
)

gerrit_plugin(
    name = "my-plugin-ee11",
    srcs = glob(["src/main/java/**/*.java"]),  # same canonical EE8 sources
    flavour = "ee11",
    ...
)

gerrit_plugin_tests(
    srcs = glob(["src/test/java/**/*.java"]),  # same canonical test sources
    flavour = "ee11",
    plugin = "my-plugin-ee11",
)
```

`flavour = "ee11"` makes the shared macro pair do everything the current
jakarta flavour needs:

* run the `to_jakarta` transform over the plugin's sources — main *and*
  test — (`javax.servlet` → `jakarta.servlet`), keeping package names and
  line numbers;
* inject `Gerrit-Flavour: ee11` into the plugin manifest;
* compile against the **jakarta** plugin API (and, for the tests, the
  jakarta acceptance framework);
* wrap the jar in the EE11 build configuration, so it self-selects the
  jakarta servlet/Jetty/Guice tiers;
* **guard the test twin to the ee11 configuration** — a test target cannot
  self-transition the flavour the way the `-ee11` jar targets do, so the
  guard routes it to the matching wildcard pass instead. A flavoured
  artifact without a flavoured test execution is only half migrated: it
  would be byte-audited but never run.

Both flavours then build together, again with no flag:

```sh
bazel build //plugins/my-plugin:my-plugin //plugins/my-plugin:my-plugin-ee11
```

and both flavours *test* together, one per wildcard pass. A migration stage
merges on its stakeholders' timeline and can be the live state for years,
so at **every dual-flavour stage** the per-plugin wildcard stays green with
and without the flavour flag — each pass runs its own flavour's tests and
*skips* (never fails on) the other. The obligation ends at EE8 retirement,
when the second flavour, its flag value and its test twin are all
intentionally gone:

```sh
bazel test //plugins/my-plugin/...
bazel test --@com_googlesource_gerrit_bazlets//flags:flavour=ee11 \
    //plugins/my-plugin/...
```

As the snippet shows, the default target declares `flavour = "ee8"`
explicitly once a twin exists — never leave it unflavoured: the marker is
loader-equivalent to the previously unmarked jar, and the attribute guards
the javax side — and, via Bazel's incompatibility propagation, its deploy
jar and dependency tests — to the ee8 configuration. An unguarded javax
default *fails* the EE11 pass instead of skipping.

The EE11 jar is **generated** from the canonical EE8 source — no fork,
no second source tree, no hand-maintained namespace copy. The only plugins that
need more than this are those whose bundled library is itself split across
namespaces (Javamelody): their `-ee11` targets — jar and tests — point at
the jakarta library line, and everything else is identical.

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
bridge, mirroring the JGit and Gitiles libraries. The test twins follow the
same contract — `gerrit_plugin_tests(canonical = "jakarta", flavour = ...)`
per side, each guarded to its configuration. Artifact names and both WARs'
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
   separately-built-per-flavour path (the split `javamelody` 1.x/2.x library:
   its per-flavour jar *and test* targets each resolve their own isolated
   deps repo). It also exposes a **standalone build mode** (built outside
   the Gerrit tree against the published plugin API). This makes javamelody
   the intended end-to-end proof of the publishing story: a real
   servlet-coupled custom plugin building its jakarta flavour standalone
   against the released jakarta API — which, since publication lands with
   the default flip, is the unsuffixed `gerrit-plugin-api` (no `-ee11`
   Maven name is ever minted). Its full lifecycle is staged exactly like
   the core plugins' — add-flavour → jakarta-canonical → flip naming →
   drop-ee8 → drop-marker/machinery — every stage a pending change that
   merges at its release boundary, converging on a single plain jakarta
   plugin against `javamelody-core` 2.x. (The core plugins' final stage
   sits under `drop-flavour-markers`; javamelody's combines the marker
   and machinery cleanup under `drop-flavour-machinery`.)

All three carry per-flavour **test twins at every dual-flavour stage**
(add-flavour, jakarta-canonical, flip naming): each flavoured jar is
test-executed on its own configuration, not just byte-audited. After the
EE8 retirement the chains collapse to the single remaining flavour and its
one test suite — and the two-pass invariant **ends** with it: the `ee8`
flag value retires with the flavour (and later the flag itself), so there
is no EE8 pass left to describe. Only the jakarta suite and its single
pass remain. The
plugin-manager twins even inspect the matching flavour's WAR
(`release.war` / `release-ee11.war`, later `release-ee8.war`), proving the
core-plugins listing derives names from `Gerrit-PluginName` manifests, not
from the suffixed jar file names inside the flavoured WAR.

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

Publication of the jakarta artifacts lands together with the default flip,
so no `-ee11` Maven name is ever minted: the published scheme is the JGit /
Gitiles one — the unsuffixed artifact is jakarta and the legacy flavour
carries an `-ee8` suffix for its one-train deprecation window:

| EE11 (default, from the flip) | EE8 (legacy, one release train) |
|---|---|
| `com.google.gerrit:gerrit-war` | `com.google.gerrit:gerrit-war-ee8` |
| `com.google.gerrit:gerrit-plugin-api` | `com.google.gerrit:gerrit-plugin-api-ee8` |
| `com.google.gerrit:gerrit-acceptance-framework` | `com.google.gerrit:gerrit-acceptance-framework-ee8` |

(`gerrit-extension-api` is servlet-free and stays single-flavoured.) The
legacy `-ee8` jar/sources/javadoc are each built under an ee8 transition, so
both flavours are produced and staged in one invocation. A standalone plugin
build then depends on the unsuffixed jakarta `gerrit-plugin-api`; a legacy
plugin build on `gerrit-plugin-api-ee8`.

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
`oauth-ee11`, `openid-ee11`, `init-ee11`, `jetty-ee11`), the per-flavour
test suites (`httpd_tests` / `httpd_tests-ee11`, `pgm_tests` /
`pgm_tests-ee11`, the acceptance servlet-boundary groups `filter`,
`api_plugin`, `rest_bindings` and their `-ee11` twins, ...) and the
per-flavour **plugin** test twins (`gitiles_tests` / `gitiles_tests-ee11`,
`plugin_manager_tests` / `plugin_manager_tests-ee11` before the flip;
after it the legacy twin takes the `-ee8` suffix: `gitiles_tests` /
`gitiles_tests-ee8`, `plugin_manager_tests` / `plugin_manager_tests-ee8`,
`javamelody_tests` / `javamelody-ee8_tests`) — each compile in
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
# Before the default flip (EE8 is the default):
bazelisk test //...    # EE8 side; the EE11 twins are skipped automatically
bazelisk test --@com_googlesource_gerrit_bazlets//flags:flavour=ee11 //...

# After the default flip, before EE8 retirement (EE11 is the tree
# default, set in .bazelrc; --@com_googlesource_gerrit_bazlets//flags:flavour=ee8
# becomes an invalid flag value once the ee8 flavour retires):
bazelisk test //...    # EE11 side; the EE8 twins are skipped automatically
bazelisk test --@com_googlesource_gerrit_bazlets//flags:flavour=ee8 //...
```

Because the guard is *conditional on the flavour*, each target shows up exactly
when its flavour is active — neither pass has to enumerate or exclude targets
by hand. (The `-ee11` *build/publish* targets — `release-ee11`, the `-ee11`
plugin jars and APIs — self-transition and need no flag at all; only the *test*
passes take the flag, because a test target cannot self-transition.)

So CI runs the suite twice: the default flavour's flagless wildcard plus
the other flavour under the flag — an EE8 default with an EE11 flag pass
before the default flip, and the swapped polarity after it (the flip
commit makes EE11 the tree default in `.bazelrc`, so the plain pass runs
the jakarta side and the legacy side runs under
`--@com_googlesource_gerrit_bazlets//flags:flavour=ee8`). Same invariant,
same two invocations, throughout the dual-flavour window — until EE8
retirement removes the second pass altogether. Non-servlet tests are flavour-neutral and ride along in both
passes; sources that only need HTTP status constants use
`org.apache.http.HttpStatus` instead of a servlet import, keeping them
flavour-neutral by construction.

The same two passes cover the **plugins** — nothing plugin-specific in CI.
`bazel test plugins/<plugin>/...` is green with and without the flag at
every **dual-flavour** stage: each pass executes that flavour's plugin
test twin and skips the other side (the guarded jar, its deploy chain and
its dependency tests follow via incompatibility propagation). A stage can
be the live state for years, so this per-plugin wildcard symmetry is a
per-stage gate, not a convergence milestone — and it ends at EE8
retirement, when the second targets and the `ee8` flag value are
intentionally removed and only the jakarta pass remains.
