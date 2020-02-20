---
title: "User Stories"
permalink: userStories.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## User Stories

The Gerrit community has a high interest in the users of the Gerrit Code Review
project. We want to understand who our users are, why they like Gerrit and how
Gerrit is integrated with their workflows. If your project or company is using
Gerrit, we would like to know about your use case, so that we are aware of it
when we evolve Gerrit further. If you use Gerrit, we kindly ask you to share
your usage below.

### How to share your story?

Upload a change to the
[homepage](https://gerrit-review.googlesource.com/admin/repos/homepage) project
that adds your story to this page. If you don't know how to do this, just send
an email to the [repo-discuss](https://groups.google.com/forum/#!forum/repo-discuss)
mailing list that has a subject starting with '[story]' and a Gerrit maintainer
will take care to upload it for you.

Your story can be as simple as you prefer it to be, as long as it positively
conveys your feedback on Gerrit.

### Stories shared

Please add new stories at the top of this list.

---

**[$2020-02-14] Gerrit at Google (Google)**

```
  Google has an in-house deployment of Gerrit, serving hundreds of teams and
  thousands of users. Our major customers are the Chrome and Android projects.

  The Android Open Source project uses Gerrit extensively for its platform
  development. The rich ACL model allows the Android project to cooperate with
  a wide range of hardware partners on a single project, while also observing
  confidentiality agreements. The configurability of workflows lets the
  Android team manage a complex release workflow across many devices and
  platform versions.

  The Chromium project uses Gerrit to work on among others the Chrome browser.
  Our in-house deployment is optimized for performance, so we can offer
  engineers a smooth workflow, despite the gargantuan size of the Chromium
  code base.
```

---

### Story template

<pre>
  ---

  **[$yyyy-MM-dd] $name ($company, $project)**

  ```
    $story-text
  ```

  ---
</pre>
