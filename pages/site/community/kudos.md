---
title: "Kudos"
permalink: kudos.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Kudos

Gerrit is an open-source project and its success much depends on the Gerrit
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

### How to add kudos

Upload a change to the [homepage](https://gerrit-review.googlesource.com/admin/repos/homepage)
project that adds the kudos to this page. If you don't know how to do this, just
send an email to the [repo-discuss](https://groups.google.com/forum/#!forum/repo-discuss)
mailing list that has a subject starting with '[kudos]' and a Gerrit maintainer
will take care to upload the kudos for you.

### List of kudos

Please add new kudos at the top of this list.

---

**[2020-09-02] To: Saša Živkov (SAP)**

```
  Thanks again Saša for having helped significantly on these replication reviews
  [1] below. Once again, you were able to patiently help and iterate through a
  challenging yet relevant review then. You are among the Gerrit reviewers who
  show professional review comments, both technically and socially speaking.
  Your calm approach to a review and the attitude that follows are humble and
  exemplary. So thank you for your thorough, supportive and helpful review(s).
  You made a difference again for [1], which needed a keen stir such as yours.
```

[1] <a href="https://gerrit-review.googlesource.com/c/plugins/replication/+/267812">Don't wait for pending events to process on startup</a>

From: Marco Miller (Ericsson)

---

**[2020-07-17] To: Saša Živkov (SAP)**

```
  Thank you Saša for always helping people out when they struggle with Prolog
  submit rules. Being able to configure when a change should be submittable is
  important for many teams, but when this requires writing Prolog submit rules
  people often struggle because they are not much familiar with Prolog. When
  this happens, Saša is always there to help. This unblocks teams setting up
  their workflows and saves them quite some frustration debugging Prolog. Saša
  also wrote the Prolog cookbook in the Gerrit documentation [1] which continues
  to be a great source for everyone starting with Prolog submit rules.
```

[1] <https://gerrit-review.googlesource.com/Documentation/prolog-cookbook.html>

From: Edwin Kempin (Google)

---

**[2020-06-29] To: Christian Aistleitner (quelltextlich e.U., Wikimedia)**

```
  Often Gerrit administrators are worried about upgrading their Gerrit
  instances, especially if the upgrade is across multiple Gerrit versions and if
  it includes the migration to NoteDb. To overcome this, it's important that
  community members give feedback on performed upgrades and issues that they hit
  during the migration. Christian just shared a summary of the Gerrit upgrade
  that was done at Wikimedia, including a list of things to watch out during
  such an upgrade. Thank you Christian for sharing these insights and even more
  for contributing back fixes for the issues that you faced, making the upgrade
  smoother for others.
```

[1] <https://groups.google.com/g/repo-discuss/c/G5wucKJg9Ag/m/pLin-i3mBgAJ>

From: Edwin Kempin (Google)

---

**[2020-06-26] To: Marco Miller (Ericsson) and Matthias Sohn (SAP)**

```
  For Gerrit as an open source project it is essential to have a healthy open
  source community. To address the needs of the open source community better we
  have established the role of a community manager [1] one year ago. I want to
  thank Marco and Matthias for taking up this role and filling it with life. It
  is a pleasure to work with you as community manager and I'm amazed by the
  things that we have achieved together [2].
```

[1] <https://gerrit-review.googlesource.com/Documentation/dev-roles.html#community-manager><br>
[2] <https://groups.google.com/g/repo-discuss/c/OJYszErJwT4/m/YG9ymoL9DQAJ>

From: Edwin Kempin (Google)

---

**[2019-08-07] To: David Pursehouse (CollabNet)**

```
  For the open-source community it is very important that all discusssions are
  transparent and that findings and conclusions are clearly communicated. David
  takes care to collect and publish project news regularly on our homepage [1]
  making it easy for everyone to follow what's going on in the project.
  Previously one could get this level of insights only by closely following the
  mailing list and ongoing reviews. Thank you David, this is a great overview
  for everyone, especially for people that are not deeply involved in the
  project.
```

[1] <https://www.gerritcodereview.com/news.html>

From: Edwin Kempin (Google)

---

**[2019-03-21] To: Gert van Dijk**

```
  I want to thank Gert for actively supporting users on the repo-discuss mailing
  list [1]. Taking time to understand user issues and guide them to solutions is
  highly appreciated. This work is especially important to make the onboarding
  of new Gerrit users smooth.
```

[1] <https://groups.google.com/forum/#!forum/repo-discuss>

From: Edwin Kempin (Google)

---

**[2019-03-20] To: David Pursehouse (CollabNet); David Ostrovsky; Jonathan
Nieder (Google), Jonathan Tan (Google), Luca Milanesio (GerritForge);
Masaya Suzuki (Google), Matthias Sohn (SAP)**

```
  The Gerrit open-source project had to deal with 2 severe security
  vulnerabilities (issue 10201 [1], issue 10262 [2]) that required patching 6
  JGit releases and 8 Gerrit releases (2.9 to 2.16). David Pursehouse, David
  Ostrovsky, Jonathan Nieder, Jonathan Tan, Luca Milanesio, Masaya Suzuki and
  Matthias Sohn were extremely supportive to deal with the situation. In
  particular they took care of:

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

[1] <https://bugs.chromium.org/p/gerrit/issues/detail?id=10201><br>
[2] <https://bugs.chromium.org/p/gerrit/issues/detail?id=10262>

From: Edwin Kempin (Google)

---

**[2019-03-20] To: Luca Milanesio (GerritForge)**

```
  I want to thank Luca for setting up the analytics dashboard [1] for Gerrit.
  This dashboard makes the community contributions transparent and I always find
  it interesting to look at the various statistics.
```

[1] <https://analytics.gerrithub.io/kibana/app/kibana#/dashboards>

From: Edwin Kempin (Google)

---

**[2019-03-20] To: Luca Milanesio (GerritForge)**

```
  Luca runs the CI server [1] for the Gerrit project. This supports the Gerrit
  development a lot because changes are automatically verified and change
  authors get quick feedback on issues with compilation, tests and formatting.

  Luca did not only set up builds for Gerrit across all its branches, but also
  for most of the Gerrit plugins. This makes the consumption of Gerrit plugins
  much easier since users can simply download the jars of the plugins they need,
  instead of building them themselves.

  Thank you Luca!
```

[1] <https://gerrit-ci.gerritforge.com>

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
  fostering a great open-source community around it.

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
