---
title: "Gerrit's History"
sidebar: gerritdoc_sidebar
permalink: about.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Google Mondrian

Google developed [Mondrian], a Perforce based code review tool to
facilitate peer-review of changes prior to submission to the central
code repository.  Mondrian is not open source, as it is tied to the
use of [Perforce] and to many Google-only services, such as
[Bigtable].  Google employees have often described how useful Mondrian
and its peer-review process is to their day-to-day work.

[Mondrian]: https://www.youtube.com/watch?v=sMql3Di4Kgc
[Perforce]: http://www.perforce.com/
[Bigtable]: http://research.google.com/archive/bigtable.html
[Rietveld]: https://github.com/rietveld-codereview/rietveld

## Rietveld

Guido van Rossum open sourced portions of Mondrian within [Rietveld],
a similar code review tool running on Google App Engine, but for use
with Subversion rather than Perforce.  Rietveld is in common use by
many open source projects, facilitating their peer reviews much as
Mondrian does for Google employees.  Unlike Mondrian and the Google
Perforce triggers, Rietveld is strictly advisory and does not enforce
peer-review prior to submission.

## Gitosis and Gitolite

Git is a distributed version control system, wherein each repository
is assumed to be owned/maintained by a single user.  There are no
inherent security controls built into Git, so the ability to read from
or write to a repository is controlled entirely by the host's
filesystem access controls.  When multiple maintainers collaborate on
a single shared repository a high degree of trust is required, as any
collaborator with write access can alter the repository.

[Gitosis] and [Gitolite] provide tools to secure centralized Git
repositories, permitting multiple maintainers to manage the same
project at once, by restricting the access to only over a secure
network protocol, much like Perforce secures a repository by only
permitting access over its network port.

[Gitosis]: https://github.com/tv42/gitosis
[Gitolite]: http://gitolite.com/gitolite/index.html

## Android

The [Android Open Source Project][AOSP] (AOSP) was founded by Google
by the open source releasing of the Android operating system.  AOSP
has selected Git as its primary version control tool.  As many of the
engineers have a background of working with Mondrian at Google, there
is a strong desire to have the same (or better) feature set available
for Git and AOSP.

[AOSP]: http://source.android.com/

## The Rietveld fork

Gerrit Code Review started as a simple set of patches to Rietveld, and
was originally built to service AOSP.  This quickly turned into a fork
as we added access control features that Guido van Rossum did not want
to see complicating the Rietveld code base.  As the functionality and
code were starting to become drastically different, a different name
was needed.  Gerrit calls back to the original namesake of Rietveld,
[Gerrit Rietveld](http://en.wikipedia.org/wiki/Gerrit_Rietveld), a
Dutch architect.

## Gerrit 2.x rewrite

Gerrit 2.x is a complete rewrite of the Gerrit fork, changing the
implementation from Python on Google App Engine, to Java on a J2EE
servlet container and a SQL database.
