---
title: "Kudos"
sidebar: gerritdoc_sidebar
permalink: kudos.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Kudos

Gerrit is an open source project and its success much depends on the Gerrit
community and the people driving it. Every day we see highly engaged and
motivated contributors and kudos is a way for you to thank them and show your
appreciation.

Kudos is a public written thank you note of appreciation. These can be given by
anyone to any Gerrit contributor and are public on the Gerrit homepage.

Kudos can be given for doing a good job (e.g. fixing an important bug, helping
someone resolve an issue, speaking at an event etc.) or living good citizenship
behavior (e.g. doing lots of reviews, actively helping users on the mailing
list, caring about releases, organizing community events, maintaining plugins
etc.).

### How to add kudos?

Upload a change to the [homepage](https://gerrit-review.googlesource.com/admin/repos/homepage)
project that adds the kudos to this page. If you don't know how to do this, just
send an email to the [repo-discuss](https://groups.google.com/forum/#!pendingmsg/repo-discuss)
mailing list that has a subject starting with '[kudos]' and a Gerrit maintainer
will take care to upload the kudos for you.

### List of kudos

Note: Please add new kudos at the top of this list.

---

**[2019-03-20] To: David Pursehouse (CollabNet); David Ostrovsky; Jonathan
Nieder (Google), Jonathan Tan (Google), Luca Milanesio (GerritForge);
Masaya Suzuki (Google), Matthias Sohn (SAP)**

```
  The Gerrit open source project had to deal with 2 severe security
  vulnerabilities ([issue 10201](https://bugs.chromium.org/p/gerrit/issues/detail?id=10201),
  [issue 10262](https://bugs.chromium.org/p/gerrit/issues/detail?id=10262) that
  required patching 6 JGit releases and 8 Gerrit releases (2.9 to 2.16). David
  Pursehouse, David Ostrovsky, Jonathan Nieder, Jonathan Tan, Luca Milanesio,
  Masaya Suzuki and Matthias Sohn were extremely supportive to deal with the
  situation. In particular they took care of:

  * Reverting the problematic code in Gerrit (David Pursehouse)
  * Implementing JGit fixes (Masaya Suzuki, Jonathan Nieder)
  * Reviewing JGit fixes (Masaya Suzuki, Jonathan Nieder, Jonathan Tan, Matthias
    Sohn)
  * Preparing fixed JGit versions (Matthias Sohn)
  * Making the fixed JGit versions available to Gerrit without breaking the
    embargo (Matthias Sohn)
  * Upgrading JGit for all affected Gerrit versions (David Ostrovsky)
  * Fixing the CI build for Gerrit 2.9 (David Ostrovsky, Luca Milanesio)
  * Writing release notes (David Pursehouse)
  * Code reviews (David Pursehouse, David Ostrovsky, Luca Milanesio)
  * Releasing fixed Gerrit 2.16 versions (David Pursehouse, Luca Milanesio)
  * Releasing fixed Gerrit 2.15 version (David Pursehouse)
  * Releasing fixed Gerrit 2.9 to 2.14 versions (Luca Milanesio)
  * Announcing and documenting the vulnerabilities for the community
    (David Pursehouse, Luca Milanesio)
  * Collaboration on a post mortem (David Pursehouse, David Ostrovsky, Luca
    Milanesio, Matthias Sohn)

  This was an extraordinary collaboration across teams, projects, companies and
  timezones and showed to the Gerrit community that the Gerrit project is taking
  security seriously.

  This engagement was especially remarkable since a lot of these actions
  happened during Christmas/New Year.
```

From: Edwin Kempin (Google)

---

**[2019-03-20] To: Luca Milanesio (GerritForge)**

```
  I want to thank Luca for setting up the
  [analytics dashboard](https://analytics.gerrithub.io/kibana/app/kibana#/dashboards)
  for Gerrit. This dashboard makes the community contributions transparent and I
  always find it interesting to look at the various statistics.
```

From: Edwin Kempin (Google)

---

**[2019-03-20] To: Luca Milanesio (GerritForge)**

```
  Luca runs the [CI server](https://gerrit-ci.gerritforge.com) for the Gerrit
  project. This supports the Gerrit development a lot because changes are
  automatically verified and change authors get quick feedback on issues with
  compilation, tests and formatting.

  Luca did not only set up builds for Gerrit across all its branches, but also
  for most of the Gerrit plugins. This makes the consumption of Gerrit plugins
  much easier since users can simply download the jars of the plugins they need,
  instead of building them themselves.

  Thank you Luca!
```

From: Edwin Kempin (Google)

---

**[2019-03-20] To: David Pursehouse (CollabNet)**

```
  David takes great care of the Gerrit releases. This is of high importance for
  the Gerrit community because it makes new features and bug-fixes available for
  everyone.

  David was driving several major releases and ensures that the release notes
  are always well-written and complete. In addition, he pays high attention to
  backporting bug-fixes that matter and ensures that release issues are quickly
  addressed by frequently releasing minor versions that include these bug-fixes.
  David also takes care of merging the stable branches back to master which can
  be a lot of work because conflicts need to be resovled.

  I really appreciate all this work. Thank you!
```

From: Edwin Kempin (Google)

---

**[2019-03-20] To: David Ostrovsky**

```
  Since years David is taking care of our build tool chain and ensures that the
  development setup to start working on Gerrit and Gerrit plugins is staying
  smooth.

  David was the main driver to adopt first Buck and then Bazel. Rewriting the
  complete build tool chain multiple times was a large amount of work and
  included tracing down and fixing many tricky issues that required
  collaboration with the Buck and Bazel teams.

  I'm happy that the Gerrit build always just works, but I know that this can't
  be taken for granted. Thanks David for all your hard work on this.
```

From: Edwin Kempin (Google)

---

**[2019-03-20] To: Shawn Pearce (Google)**

```
  I want to thank Shawn for starting the Gerrit Code Review project and
  fostering a great open source community around it.

  Shawn's passion and dedication are the source of our success. Shawn was an
  outstanding engineer who shaped the long-term vision for our project. The
  number of his contributions is beyond count, his guidance and deep technical
  knowledge were exceptional and I'm truely thankful for all his reviews that
  made me learn so much.
```

From: Edwin Kempin (Google)

---

### Template

<pre>
  ---

  **[$yyyy-MM-dd] To: $receiver-name ($receiver-company)**

  ```
    $kudos-text
  ```

  From: $sender-name ($sender-company)

  ---
</pre>
