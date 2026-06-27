---
title: ""
permalink: design-docs/ee8-ee10-flavoured-release-solution-libraries.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Library flavours

Each servlet-facing library provides both flavours from a single upstream source
tree — there is no fork — and a generated flavour keeps the original package
names:

* **JGit** is `jakarta.servlet`-canonical and owns a generated EE8
  (`javax.servlet`) module set, derived from those canonical sources by the
  shared, dependency-free bazlets transform.
* **Gitiles** is likewise `jakarta.servlet`-canonical as of `gitiles-servlet`
  2.0.0; its EE8 consumers pin the prior `javax.servlet` release line (1.6.0).
  The two flavours are published under the same Maven coordinates at different
  versions.

Because a generated flavour keeps the same class names as its canonical
counterpart, only one of the pair may sit on a given classpath — which is why
each WAR carries exactly one flavour. Duplication stays at the release boundary;
the source and maintenance model is shared.

The JGit side is specified in depth in the
[JGit EE8 Servlet Bridge design proposal](https://github.com/davido/jgit-ee8-servlet-bridge-design-proposal),
which covers the first-class EE8 module design and the same-FQDN / no-p2
constraint.
