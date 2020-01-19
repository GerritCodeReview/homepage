---
title: "Gerrit Project News #6: December 2019 - January 2020"
tags: news
keywords: news
permalink: 2020-01-31-gerrit-news-dec-jan-2020.html
summary: "Gerrit project news from December 2019 and January 2020."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Backup Documentation

Matthias Sohn (SAP) created a new documentation page with detailed
instructions of how to backup a Gerrit site. This was included in
the releases
[2.16.14](http://gerrit-documentation.storage.googleapis.com/Documentation/2.16.14/backup.html),
[3.0.5](http://gerrit-documentation.storage.googleapis.com/Documentation/3.0.5/backup.html),
and [3.1.1](https://gerrit-documentation.storage.googleapis.com/Documentation/3.1.1/backup.html).

## HTTPS Required for Download from Maven Central

[Effective January 15, 2020](https://support.sonatype.com/hc/en-us/articles/360041287334),
the Central Repository no longer supports insecure communication over plain HTTP and requires
that all requests to the repository are encrypted over HTTPS.

As a result of this, older releases of Gerrit (2.15.x and older) are no longer buildable
from source on a clean development environment because the rules_closure dependency includes
a download over HTTP.
This was fixed in [change 250502](https://gerrit-review.googlesource.com/c/gerrit/+/250502)
which is included in `stable-2.14`. To build Gerrit 2.14.x and 2.15.x it is now necessary
to build from the tip of the `stable-2.14` and `stable-2.15` branches, or in an environment
where the rules_closure dependency has already been downloaded before January 15.
