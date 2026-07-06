---
title: ""
permalink: design-docs/servlet-flavoured-release-implementation-notes.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Implementation notes — the Bazel build machinery

This page explains how the flavoured build is wired in Bazel: the flag, the
`config_setting`s, the configuration transition, `select()`,
`target_compatible_with`, and the servlet-flavour toolchain — and how they fit
together.

One idea underpins all of it: **the flavour is a single build *configuration*
value.** Every other primitive either *sets* that value or *reacts* to it.

```
 A. HOW THE FLAVOUR VALUE IS CHOSEN
    (1) command line:  --@com_googlesource_gerrit_bazlets//flags:flavour=ee10
                                                        (flips the whole build)
    (2) TRANSITION:    flavoured_war(flavour="ee10")    (flips one subgraph;
                       cfg = flavour_transition          build BOTH in one run)
                                  |
                                  v
 B. THE SEAM (owned in bazlets)
    KNOWN_FLAVOURS = [ee8, ee10]
    string_flag  //flags:flavour  =  ee8 (default) | ee10
                                  |  future values first extend KNOWN_FLAVOURS
                                  |  turned into booleans by
                 +----------------+----------------+
                 v                                 v
        config_setting //flags:ee8        config_setting //flags:ee10
                 +----------------+----------------+
                                  |  read by
 C. THREE CONSUMERS

    1. select()
       flavoured_alias / flavoured_twin_alias
       = select({ee10: X, default: Y})
       routes a DEP or TWIN by flavour
       examples: httpd -> httpd-ee10, gitiles-servlet-jar

    2. target_compatible_with
       flavour_only(f) = select({ee10: [], default: [incompatible]})
       skips jakarta-only targets in `//...`
       example: httpd-ee10 is skipped in the EE8 wildcard build

    3. TOOLCHAIN
       toolchain(target_settings =
         ["@com_googlesource_gerrit_bazlets//flags:eeN"]) picks the bundle
       servlet_flavour_deps re-exports one bundle part as
       JavaInfo/DefaultInfo, plus query-visible data/license_deps
       edges for license generation
       examples: //lib:servlet-api, //lib/jetty:servlet,
                 //lib:jgit-servlet, //lib/guice:*
```

## The through-line

**`flag -> config_setting -> { select | target_compatible_with | toolchain }`**,
with the **transition** as the alternate way to set the flag for a single
subgraph. The accepted values live in **`KNOWN_FLAVOURS`** and the flag is
written **once** (in bazlets); every other primitive only *reads* the resulting
configuration. That is why a single
`bazel build release release-ee10` produces both flavours: the default target
sees `flavour=ee8`, and `release-ee10` self-transitions its subgraph to
`flavour=ee10`.

## Who does what

| Primitive | Job |
|---|---|
| `KNOWN_FLAVOURS` | supported flavour vocabulary; currently `ee8`, `ee10` |
| `string_flag //flags:flavour` | selected flavour value |
| `flavour_transition` (rule `cfg`) | flip a subgraph's flavour, so both flavours build in one invocation |
| `config_setting //flags:eeN` | make the flag usable as a boolean condition |
| `select()` / `flavoured_alias` / `flavoured_twin_alias` | **twin routing** — pick the flavour's source-divergent *compiled library*; `flavoured_twin_alias` derives `:name-ee8`/`:name-ee10` and validates flavour names |
| `flavoured_library` / `flavoured_tests` | **one-call mechanical twins** — generate the whole family (default leaf + javax→jakarta transform + guarded per-flavour leaf + `flavoured_twin_alias`) from a single call; `flavours` defaults to `KNOWN_FLAVOURS`, so a mechanical flavour needs no call-site edit once the transform produces its sources |
| `target_compatible_with` / `flavour_only` | guard — keep jakarta-only twins out of the default `//...` build |
| `toolchain` + `servlet_flavour_deps` | **dependency sets** — resolve the flavour's servlet-api / Jetty / Guice / JGit/Gitiles *jars* from one bundle |

## Worked example — `bazel build release release-ee10`

```
release            flavour flag = ee8 (default)
  config_setting //flags:ee8 -> TRUE ; //flags:ee10 -> FALSE
  - flavoured_twin_alias picks ee8 twin -> httpd-ee8
  - flavour_only(ee10) on httpd-ee10    -> INCOMPATIBLE -> skipped
  - toolchain resolution                -> ee8 servlet_flavour_toolchain
       //lib:servlet-api                 -> servlet-api-ee8 (javax, neverlink)
  => release.war = javax / Jetty-ee8 / Guice-6

release-ee10 = flavoured_war(flavour="ee10")
  flavour_transition sets //flags:flavour = ee10 for the whole subgraph
  config_setting //flags:ee10 -> TRUE
  - flavoured_twin_alias picks ee10 twin -> httpd-ee10
  - flavour_only(ee10) on httpd-ee10    -> COMPATIBLE -> built
  - toolchain resolution                -> ee10 servlet_flavour_toolchain
       //lib:servlet-api                 -> servlet-api-ee10 (jakarta, neverlink)
  => release-ee10.war = jakarta / Jetty-ee10 / Guice-7
```

## Why two dependency mechanisms (select vs toolchain)

They solve different *shapes* of boundary:

* **`select()` / `flavoured_alias` / `flavoured_twin_alias`** — for **twin
  routing**: choose between two *separately-compiled libraries whose sources
  differ* (`httpd-ee8` and the transform-generated `httpd-ee10`). A toolchain
  carries dependencies, not source-divergent compiled libraries, so these stay on
  `select()`. A **twin** is the same logical library compiled once per flavour —
  `:httpd-ee8` from the javax sources, `:httpd-ee10` from the
  transform-generated jakarta sources — sharing FQDNs, so only one is ever on a
  classpath. The convention wrapper
  `flavoured_twin_alias(name, flavours = ["ee10"])` takes a list of supported
  non-default flavours, derives the `:name-<flavour>` labels, and its `select()`
  picks the arm for the active flavour; the generic `flavoured_alias` remains for
  non-conforming routes such as `gitiles-servlet-jar` (a cross-repo maven jar).
* **toolchain + `servlet_flavour_deps`** — for **dependency sets**: choose the
  flavour's servlet-api / Jetty / Guice / JGit **jars**. The whole servlet tier
  lives in one resolved object, and the public neutral dependency labels expose
  its parts: for example `//lib:servlet-api`, `//lib/jetty:servlet`,
  `//lib:jgit-servlet`, and the `//lib/guice:*` cluster. Most Gerrit-owned
  neutral labels follow one naming convention: the **neutral** label is the plain
  name (what consumers depend on), its per-flavour backings are `:name-ee8` /
  `:name-ee10`, and a jar that is byte-identical across flavours (e.g.
  `//lib/guice:aopalliance`) stays a single neutral target with no suffix. (The
  cross-repo `//lib/gitiles:gitiles-servlet-jar` is the exception — it stays on
  the generic `flavoured_alias` because it is also consumed as a raw file.) For migrated dependency-set consumers,
  adding a future flavour starts with a `KNOWN_FLAVOURS` entry, a
  `config_setting`, and a `toolchain()` registration, with **no change at the
  consumer labels** — the extensibility payoff.

`target_compatible_with` is orthogonal to both: it is the *compile guard* that
keeps the jakarta-only twin targets out of the default `bazel build //...`, so a
plain wildcard build stays green on the EE8 default while the EE10 targets build
under the flag or their self-transition.

## Where the machinery lives

`KNOWN_FLAVOURS`, the flag, the `config_setting`s, the transition, the generic
helpers (`flavoured_alias`, `flavoured_twin_alias`, `flavour_only`,
`flavoured_java_library`, the `flavoured_library` / `flavoured_tests` one-call
family macros, …), and the servlet-flavour toolchain rule are owned in
the shared **bazlets** repository, so Gerrit — and any other consumer — shares
one flavour vocabulary rather than re-deriving it. Gerrit owns the concrete
toolchain registrations that bind those shared parts to Gerrit's labels, such as
the matching servlet API, Jetty adapter, Guice cluster, and JGit/Gitiles servlet
libraries for each flavour. The flavour is a *parameter* in the shared helpers
and resolver: dependency-set boundaries consume neutral labels, and the next
servlet generation is registered in the bundle instead of refactoring each such
consumer.

## Future servlet flavours

The current rollout supports two build values: the EE8 default and the
historical `ee10` value, which spells the **active** jakarta servlet tier
(Servlet 6.1 — bazlets keeps the `ee10` spelling for continuity even though the
honest generation name is `ee11`). The naming is deliberately more general than
that pair because the same shape should carry later servlet generations: future
work can either rename the active value to its accurate generation name or add a
later value such as `ee12`. Either way the path is the same — add the value to
`KNOWN_FLAVOURS`, then add the matching `config_setting` in bazlets and the
concrete servlet-flavour toolchain registration in Gerrit for the new bundle.

From there, most of the tree needs no edit:

* **Mechanical twins gain the new flavour with no call-site change.**
  `flavoured_library` and `flavoured_tests` default their `flavours` to the
  non-default entries of `KNOWN_FLAVOURS`, so every purely-transformable library
  and test suite grows its `:name-ee12` twin the moment the value is added —
  *provided the `to_jakarta` transform already produces that flavour's sources*
  (it maps javax→jakarta and Jetty ee8→ee10, and `jakarta.servlet` is
  version-stable; a flavour needing a different source mapping extends the
  transform first).
* **Dependency-set consumers do not change:** they keep depending on the neutral
  labels `//lib:servlet-api`, `//lib/jetty:servlet`, `//lib:jgit-servlet`, and
  `//lib/guice:*`, which the new toolchain registration re-points.

Only the genuinely per-flavour surface needs hand work: hand-written twins that
are *not* a pure transform (e.g. `pgm/http/jetty`, whose ee10 overlay has no
mechanical form, so its `flavour` and `flavoured_twin_alias` list stay explicit),
the concrete build outputs (`release-ee10`, a published `-ee10` artifact), and
plugin source-transform and manifest-marker logic.
