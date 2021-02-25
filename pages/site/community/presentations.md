---
title: "Presentations"
permalink: presentations.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Presentations

Community members willing to learn about Gerrit may find useful resources on this single page.
The listed presentations can be tutorials, slides, videos, channels or other relevant formats.
There are [tutorials also in the Gerrit documentation](https://gerrit-review.googlesource.com/Documentation/index.html#_tutorials).

[GerritForge](https://www.gerritforge.com) also publishes the recordings of the talks of the
Gerrit summits on a dedicated [YouTube channel](https://www.youtube.com/gerritforgetv).

### List of presentations

Please add new presentations at the top of this list.

---

**[2020-11-20] Virtual Contributor Summit 2020**

The Gerrit community had a virtual 2-days event with various talks and
discussions. The presentation slides and notes are available from the
[agenda](https://docs.google.com/document/d/1WauJfNxracjBK3PxuVnwNIppESGMBtZwxMYjxxeDN6M).

---

**[2020-08-26] End-to-end tests**

This [presentation](https://docs.google.com/presentation/d/1xZShuNKHmqeKAtfLzxwllQWze9P18i2nHbTzX_lQ9r4/edit?usp=sharing")
introduces a [framework component for end-to-end
tests](https://gerrit-review.googlesource.com/Documentation/dev-e2e-tests.html)
and explains how to start using it from Gerrit core and plugins. This framework
was based on the [original work done by
GerritForge](https://gitenterprise.me/2019/12/20/stress-your-gerrit-with-gatling/).

A recording of the presentation is available
[here](https://drive.google.com/file/d/19YvJbPHDmwmMVcaehI1ot6xVdoQY0QxY/view?usp=sharing">gerrit/e2e-tests Recording).

From: Marco Miller (Ericsson)

---

**[2020-04-08] Summit & Hackathon 2019 in Sunnyvale**

This is the
[summary](https://www.gerritcodereview.com/2020-04-08-user-summit-sunnyvale-summary.html)
of the Gerrit User Summit & Hackathon 2019 in Sunnyvale, with links to the
available presentations.

From: Luca Milanesio with contributors (Gerrit)

---

**[2019-09-11] Summit 2019 in Gothenburg**

This is the
[summary](https://www.gerritcodereview.com/2019-09-11-user-summit-gothenburg-summary.html)
of the Gerrit User Summit 2019 in Gothenburg, with links to the available
presentations.

From: Luca Milanesio (GerritForge)

---

**[2019-01-14] Concepts and Workflows**

These slides explain
[Git](https://docs.google.com/presentation/d/1IQCRPHEIX-qKo7QFxsD3V62yhyGA9_5YsYXFOiBpgkk/edit?usp=sharing)
and [Gerrit](https://docs.google.com/presentation/d/1C73UgQdzZDw0gzpaEqIC6SPujZJhqamyqO1XOHjH-uk/edit?usp=sharing)
concepts and workflows and are meant for self-studying how Git and Gerrit work.

From: Edwin Kempin (Google)

### How to add presentations

Upload a change to the [homepage](https://gerrit-review.googlesource.com/admin/repos/homepage)
project that adds the presentation to this page. If you don't know how to do this, just
send an email to the [repo-discuss](https://groups.google.com/forum/#!forum/repo-discuss)
mailing list that has a subject starting with '[presentation]' and a Gerrit maintainer
will take care to upload the presentation for you.

### Template

<pre>
  ---

  **[$yyyy-MM-dd] Topic**

  $presentations-text

  From: $sender-name ($sender-company)

  ---
</pre>
