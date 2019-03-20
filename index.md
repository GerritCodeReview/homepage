---
title: "Gerrit Code Review"
sidebar: gerritdoc_sidebar
permalink: index.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---
<div class="row">
        <div class="col-md-3 col-sm-6">
            <div class="panel panel-default text-center">
                <div class="panel-heading">
                    <span class="fa-stack fa-5x">
                          <i class="fa fa-circle fa-stack-2x text-primary"></i>
                          <i class="fa fa-comments fa-stack-1x fa-inverse"></i>
                    </span>
                </div>
                <div class="panel-body">
                    <h4>Discuss code</h4>
                    <p>and boost your team's code fu by talking about
                    specifics.</p>
                    <a href="intro-gerrit-walkthrough.html" class="btn btn-primary">Learn More</a>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="panel panel-default text-center">
                <div class="panel-heading">
                    <span class="fa-stack fa-5x">
                          <i class="fa fa-circle fa-stack-2x text-primary"></i>
                          <i class="fa fa-code-fork fa-stack-1x fa-inverse"></i>
                    </span>
                </div>
                <div class="panel-body">
                    <h4>Serve Git</h4>
                    <p>As an integrated experience within the larger code
                    review flow.</p>
                    <a href="user-dashboards.html" class="btn btn-primary">Learn More</a>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="panel panel-default text-center">
                <div class="panel-heading">
                    <span class="fa-stack fa-5x">
                          <i class="fa fa-circle fa-stack-2x text-primary"></i>
                          <i class="fa fa-lock fa-stack-1x fa-inverse"></i>
                    </span>
                </div>
                <div class="panel-body">
                    <h4>Manage workflows</h4>
                    <p>with deeply integrated and delagatable access controls.
                    </p>
                    <a href="project-configuration.html" class="btn btn-primary">Learn More</a>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="panel panel-default text-center">
                <div class="panel-heading">
                    <span class="fa-stack fa-5x">
                          <i class="fa fa-circle fa-stack-2x text-primary"></i>
                          <i class="fa fa-download fa-stack-1x fa-inverse"></i>
                    </span>
                </div>
                <div class="panel-body">
                    <h4>Download</h4>
                    <p>Our latest release is:<br>
                    <b><a href="2.16.html#2167">2.16.7</a></b>
                    </p>
                    <a href="https://gerrit-releases.storage.googleapis.com/gerrit-2.16.7.war" class="btn btn-primary">Download</a>
                </div>
            </div>
        </div>
    </div>

## Discuss code
Read old and new versions of files with syntax highlighting and colored
differences. Discuss specific sections with others to make the right changes.

<img src="images/sbs.png">

## Manage and serve Git repositories

Gerrit includes Git-enabled SSH and HTTPS servers compatible with all
Git clients.  Simplify management by hosting many Git repositories
together.

<table>
<tr>
 <td>
 <h4>Navigate projects</h4>
 </td>
 <td>
 <h4>Control access</h4>
 </td>
 <td>
 <h4>Update branches</h4>
 </td>
</tr>
<tr>
 <td>
 <img src="images/project-list.png">
 </td>
 <td>
 <img src="images/access.png">
 </td>
 <td>
 <img src="images/branches.png">
 </td>
</tr>
</table>

Schedule [git gc](https://gerrit-documentation.storage.googleapis.com/Documentation/2.16.7/config-gerrit.html#gc)
over all managed repositories and
[replicate](https://gerrit.googlesource.com/plugins/replication/+doc/v2.16.7/src/main/resources/Documentation/config.md)
to geographical mirrors for latency reduction and backup servers for hot
spare redundancy.

## Extensible through plugins

Gerrit Code Review can be extended and further customized by installing
[server-side plugins](https://gerrit-documentation.storage.googleapis.com/Documentation/2.16.7/config-plugins.html).
Source code for additional plugins can be found through the
[project listing](https://gerrit.googlesource.com/plugins/).

## Support

The Gerrit open source community actively supports the last 2 releases
on a best effort basis. Older releases are not actively maintained but
may still receive important fixes (e.g. security fixes), but there is
no guarantee for this. Which fixes are backported to these old
releases is decided on a case by case basis.

End of life for old releases is not announced but happens implicitly
when a new Gerrit version is released.

For questions write to the mailing list (<a href="https://groups.google.com/group/repo-discuss">repo-discuss on Google Groups</a>),
join the IRC channel <a href="https://echelog.com/logs/browse/gerrit/">#gerrit</a>, or
check the questions tagged with <a href="https://stackoverflow.com/questions/tagged/gerrit">[gerrit]</a>
on Stack Overflow.

The repo-discuss mailing is managed to prevent spam posts. This means
posts from new participants must be approved manually before they
appear on the mailing list. Approvals normally happen within 1 work
day. Posts of people that participate in mailing list discussions
frequently are approved automatically.

## Social Media

Follow us on Twitter (<a href="https://twitter.com/gerritreview">@gerritreview</a>) and
<a href="https://plus.google.com/communities/111271594706618791655">Google+</a>.

## Training Slides

The following slides explain Git and Gerrit concepts and workflows and are meant
for self-studying how Git and Gerrit work:

* <a href="https://docs.google.com/presentation/d/1IQCRPHEIX-qKo7QFxsD3V62yhyGA9_5YsYXFOiBpgkk/edit?usp=sharing">Git explained: Git Concepts and Workflows</a>
* <a href="https://docs.google.com/presentation/d/1C73UgQdzZDw0gzpaEqIC6SPujZJhqamyqO1XOHjH-uk/edit?usp=sharing">Gerrit explained: Gerrit Concepts and Workflows</a>

## Kudos

Gerrit is an open source project and its success much depends on the Gerrit
community and the people driving it. Every day we see highly engaged and
motivated contributors and kudos is a way for you to thank them and show your
appreciation.

Kudos is a public written thank you note of appreciation. These can be given by
anyone to any Gerrit contributor and are public on the Gerrit homepage.

Kudos can be given for doing a good job (e.g. fixing an important bug, helping
someone resolving an issue, speaking at an event etc.) or living good
citizenship behavior (e.g. doing lots of reviews, actively helping users on the
mailing list, caring about releases, organizing community events, maintaining
plugins etc.).

### How to add kudos?

Upload a change to the [homepage](https://gerrit-review.googlesource.com/admin/repos/homepage)
project that adds the kudos to this page. If you don't know how to do this, just
send an email to the [repo-discuss](https://groups.google.com/forum/#!pendingmsg/repo-discuss)
mailing list that has a subject starting with '[kudos]' and a Gerrit maintainer
will take care to upload the kudos for you.

### List of kudos

Please add new kudos at the top of this list.

---

**To: David Pursehouse, david.pursehouse@gmail.com (CollabNet), David Ostrovsky,
david.ostrovsky@gmail.com, Luca Milanesio, luca.milanesio@gmail.com
(GerritForge), Matthias Sohn, matthias.sohn@sap.com (SAP)**

```
  The Gerrit open source project had to deal with 2 severe security
  vulnerabilities ([issue 10201](https://bugs.chromium.org/p/gerrit/issues/detail?id=10201),
  [issue 10262](https://bugs.chromium.org/p/gerrit/issues/detail?id=10262) that
  required patching 2 JGit releases and 8 Gerrit releases (2.9 to 2.16). David
  Pursehouse, David Ostrovsky, Luca Milanesio, Matthias Sohn were extremely
  supportive to deal with the situation. In particular they took care of:

  * reverting the problematic code in Gerrit (David Pursehouse)
  * preparing fixed JGit versions (Matthias Sohn)
  * making the fixed JGit versions available to Gerrit without breaking the
    embargo (Matthias Sohn)
  * upgrading JGit for all affected Gerrit versions (David Ostrovsky)
  * fixing the CI build for Gerrit 2.9 (David Ostrovsky, Luca Milanesio)
  * writing release notes (David Pursehouse)
  * code reviews (David Pursehouse, David Ostrovsky, Luca Milanesio)
  * releasing fixed Gerrit 2.16 versions (David Pursehouse, Luca Milanesio)
  * releasing fixed Gerrit 2.15 version (David Pursehouse)
  * releasing fixed Gerrit 2.9 to 2.14 versions (Luca Milanesio)
  * announcing and documenting the vulnerabilities for the community
    (David Pursehouse, Luca Milanesio)
  * collaboration on a post mortem (David Pursehouse, David Ostrovsky, Luca
    Milanesio, Matthias Sohn)

  This was an extraordinary collaboration across teams, projects, companies and
  timezones and showed to the Gerrit community that the Gerrit project is taking
  security seriously.

  This engagement was especially remarkable since a lot of these actions
  happened during Christmas/New Year.
```

From: Edwin Kempin, ekempin@google.com (Google)

---

**To: Luca Milanesio, luca.milanesio@gmail.com (GerritForge)**

```
  I want to thank Luca for setting up the
  [analytics dashboard](https://analytics.gerrithub.io/kibana/app/kibana#/dashboard/f8f0c720-23b6-11e9-ae14-1dc4e23b60c3)
  for Gerrit. This dashboard makes the community contributions transparent and I
  always find it interesting to look at the various statistics.
```

From: Edwin Kempin, ekempin@google.com (Google)

---

**To: Luca Milanesio, luca.milanesio@gmail.com (GerritForge)**

```
  Luca runs the [CI server](https://gerrit-ci.gerritforge.com) for the Gerrit
  project. This supports the Gerrit development a lot because changes are
  automatically verified and change authors get quick feedback on issues with
  compilation, tests and formatting.

  Luca did not only setup builds for Gerrit across all its branches, but also
  for most of the Gerrit plugins. This makes the consumption of Gerrit plugins
  much easier since users can simply download the jars of the plugins they need,
  instead of building them themselves.

  Thank you Luca!
```

From: Edwin Kempin, ekempin@google.com (Google)

---

**To: David Pursehouse, david.pursehouse@gmail.com (CollabNet)**

```
  David takes great care of the Gerrit releases. This is of high importance for
  the Gerrit community because it makes new features and bug-fixes available for
  everyone.

  David was driving several major releases and ensures that the release notes
  are always well-written and complete. In addition he pays high attention to
  backporting bug-fixes that matter and ensures that release issues are quickly
  addressed by frequently releasing minor versions that include these bug-fixes.
  David also takes care of merging the stable branches back to master which can
  be a lot of work because conflicts need to be resovled.

  I really appreciate all this work. Thank you!
```

From: Edwin Kempin, ekempin@google.com (Google)

---

**To: David Ostrovsky, david.ostrovsky@gmail.com**

```
  Since years David is taking care of our build tool chain and ensures that the
  development setup to start working on Gerrit and Gerrit plugins is staying
  smooth.

  David was the main driver to adopt first Buck and than Bazel. Rewriting the
  complete build tool chain multiple times was a large amount of work and
  included tracing down and fixing many tricky issues that required
  collaboration with the Buck and Bazel teams.

  I'm happy that the Gerrit build always just works, but I know that this can't
  be taken for granted. Thanks David for all your hard work on this.
```

From: Edwin Kempin, ekempin@google.com (Google)

---

**To: Shawn Pearce, sop@google.com (Google)**

```
  I want to thank Shawn for starting the Gerrit Code Review project and
  fostering a great open source community around it.

  Shawns passion and dedication are the source of our success. Shawn was an
  outstanding engineer who shaped the long-term vision for our project. The
  number of his contributions is beyond count, his guidance and deep technical
  knowledge were exceptional and I'm truely thankful for all his reviews that
  made me learn so much.
```

From: Edwin Kempin, ekempin@google.com (Google)

---

### Template

```
  ---

  **To: <receiver-name>, <receiver-email> (<receiver-company>)**

  ```
    <kudos-text>
  ```

  From: <sender-name>, <sender-email> (<sender-company>)

  ---
```
