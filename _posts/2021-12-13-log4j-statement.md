---
title: "Statement about Log4J v2 vulnerability CVE-2021-44228"
tags: cve
keywords: cve
permalink: 2021-12-13-log4j-statement.html
summary: "Statement about Log4J v2 vulnerability CVE-2021-44228 on Dec 13, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

Gerrit v3.5 uses [log4j 1.2.17](https://gerrit.googlesource.com/gerrit/+/refs/heads/stable-3.5/WORKSPACE#278),
this means it's not affected by the [Log4J v2 vulnerability CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228).

Log4j 1.2.17 is affected by [CVE-2019-17571](https://nvd.nist.gov/vuln/detail/CVE-2019-17571)
and [CVE-2020-9488](https://nvd.nist.gov/vuln/detail/CVE-2020-9488) however,
both of them require a specific log4j configuration that Gerrit does not use out
of the box.

Should you have used a [custom log4j configuration](https://gerrit-documentation.storage.googleapis.com/Documentation/3.5.0.1/config-gerrit.html#container.javaOptions)
you should also check that your configuration is not impacted by the above
vulnerabilities and look at the associated mitigation actions.
