Google developed [Mondrian]
(http://video.google.com/videoplay?docid=-8502904076440714866), a Perforce based
code review tool to facilitate peer-review of changes prior to submission to the
central code repository. Mondrian is not open source, as it is tied to the use
of [Perforce](http://www.perforce.com/) and to many Google-only services, such
as [Bigtable](http://labs.google.com/papers/bigtable.html). Google employees
have often described how useful Mondrian and its peer-review process is to their
day-to-day work.

Guido van Rossum open sourced portions of Mondrian within [Rietveld]
(http://code.google.com/p/rietveld/), a similar code review tool running on
Google App Engine, but for use with Subversion rather than Perforce. Rietveld is
in common use by many open source projects, facilitating their peer reviews much
as Mondrian does for Google employees. Unlike Mondrian and the Google Perforce
triggers, Rietveld is strictly advisory and does not enforce peer-review prior
to submission.

Git is a distributed version control system, wherein each repository is assumed
to be owned/maintained by a single user. There are no inherent security controls
built into Git, so the ability to read from or write to a repository is
controlled entirely by the host's filesystem access controls. When multiple
maintainers collaborate on a single shared repository a high degree of trust is
required, as any collaborator with write access can alter the repository.

[Gitosis](http://eagain.net/gitweb/?p=gitosis.git;a=blob;f=README.rst;hb=HEAD)
provides tools to secure centralized Git repositories, permitting multiple
maintainers to manage the same project at once, by restricting the access to
only over a secure network protocol, much like Perforce secures a repository by
only permitting access over its network port.

The [Android Open Source Project](http://source.android.com/) (AOSP) was founded
by Google by the open source releasing of the Android operating system. AOSP has
selected Git as its primary version control tool. As many of the engineers have
a background of working with Mondrian at Google, there is a strong desire to
have the same (or better) feature set available for Git and AOSP.

Gerrit Code Review started as a simple set of patches to Rietveld, and was
originally built to service AOSP. This quickly turned into a fork as we added
access control features that Guido van Rossum did not want to see complicating
the Rietveld code base. As the functionality and code were starting to become
drastically different, a different name was needed. Gerrit calls back to the
original namesake of Rietveld, [Gerrit Rietveld]
(http://en.wikipedia.org/wiki/Gerrit_Rietveld), a Dutch architect.

Gerrit2 is a complete rewrite of the Gerrit fork, completely changing the
implementation from Python on Google App Engine, to Java on a J2EE servlet
container and a SQL database.
