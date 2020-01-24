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

## Community Survey Results

The results of last year's Community Survey have been
[published](https://docs.google.com/presentation/d/e/2PACX-1vSFj7v00OS14bP64bFPsQbLIy8zP48oc9oyZNod3C7MCGyRDkCh9h64QPMiznevRNWwKRyKACSOy-Zf/pub?start=false&loop=false&delayms=3000).

## Gerrit Code Review for the Linux Kernel

Gerrit Code Review is now being used for some projects of the
Linux Kernel on [linux-review.googlesource.com](https://linux-review.googlesource.com/).

## Backup Documentation

Matthias Sohn (SAP) created a new documentation page with detailed
instructions of how to backup a Gerrit site. This was included in
the releases
[2.16.14](http://gerrit-documentation.storage.googleapis.com/Documentation/2.16.14/backup.html),
[3.0.5](http://gerrit-documentation.storage.googleapis.com/Documentation/3.0.5/backup.html),
and [3.1.1](https://gerrit-documentation.storage.googleapis.com/Documentation/3.1.1/backup.html).


## Tighter integration between Gerrit CI and the Checks plugin

Thomas Draebing (SAP), David Ostrovsky and Luca Milanesio (GerritForge) have been working
hard to improve the integration of the current [Gerrit CI](https://gerrit-ci.gerritforge.com)
with the UI of the [Checks plugin](https://gerrit.googlesource.com/plugins/checks).

That includes the ability to directly link to the build logs from the Gerrit change screen
and the possibility to re-run the build from the Checks tab.

Read the [full story on the repo-discuss mailing list](https://groups.google.com/d/topic/repo-discuss/cyGrURwY7eM/discussion).

## Zuul integration with Gerrit is coming to Gerrit CI

James E. Blair (RedHat) has been working hard to provide the automatic CI validation
of Gerrit changes using [Zuul](https://zuul-ci.org) integrated with the [Checks plugin](https://gerrit.googlesource.com/plugins/checks)
running on [Google Cloud](https://cloud.google.com).

He is currently in the environment setup phase and very soon a parallel CI environment
will be running and working side-by-side with the [Gerrit-CI](https://gerrit-ci.gerritforge.com).
We are all looking forward to seeing Zuul running and taking over Jenkins for the Gerrit change
validation in the next few months.

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
