---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-04-07-esc-minutes.html
summary: "Minutes from the ESC meeting held on April 7th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, April 7, 2020

### Attendees

David Pursehouse, Ben Rohlfs, Alice Kober-Sotzek, Patrick Hiesel, Luca Milanesio

### Place/Date/Duration

Online, April 7, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on April 21, 12:30 CEST.

## Minutes

### Gerrit News Page

The news for February and March was published on 31st March. David will create a
draft post for the next issue which will be published at the end of May.

We did not come up with any specific items to go into the next issue, but Ben
mentioned that internally at Google they have been working on writing notes for
new features and some of that could be added. Luca also mentioned that his report
of the last user summit and hackathon is almost ready to be published.

As usual, we invite the community to propose any items that they think would
be interesting.

### Plans for Remote Hackathon

We discussed whether it makes sense to hold a hackathon remotely, and concluded
that it probably does not. One of the main advantages of attending a hackathon is
to be colocated while working on new features; a remote hackathon would not give
that, and we'd be working in the same way that we do anyway outside of a hackathon.

Another point discussed is that we often use the hackathons to work together to
finalize new releases, and we had intended to do this again for 3.2. So rather than
having a remote hackathon for new features, we will instead define a week where
core contributors and maintainers can focus on finalising work that needs to be
included, and stabilizing the branch before making the release. We will announce
a week or so in advance of the intended date to cut the stable branch.

The rough schedule is to release 3.2 at the end of April or early May, taking into
account public holidays around that time. Luca and David will coordinate this.

### Renewal of ESC for 2020/2021

It's almost one year since the ESC was founded and we held the first meeting
of the 2019/2020 term, so now it's time to call for nominations for the next
year's term.

Matthias Sohn has posted [a call for nominations](https://groups.google.com/forum/#!topic/repo-discuss/zHCT2IowQng)
to the project mailing list.

### Additional lint checks in CI

Patrick asked if it's possible to add extra checks in CI to detect common
issues like unused exceptions and unused variables.

David mentioned that recent versions of ErrorProne include checks for some of
these issues, but the version embedded in Bazel is an older version therefore
we can't take advantage of them. It would be good if we can ask the Bazel team
to upgrade the embedded ErrorProne version.

We recently upgraded to Bazel 3.0.0; David will check if that included a newer
version of ErrorProne and whether we can enable any of the new checks.

### Review of open design documents

* [Instance ID / name propagation in events](https://gerrit-review.googlesource.com/c/homepage/+/257972)

  We discussed the scope of the issue and the proposed solution but did not
  reach any conclusion. Patrick will spend more time reading the proposal to
  better understand it, and we will come back to it in the next meeting.

### Review of the Roadmap

Luca pointed out that the roadmap does not mention anything about Elasticsearch,
and in fact the support for Elasticsearch has been defined as "experimental" for
a long time. The latter has already been
[raised as an issue](https://issues.gerritcodereview.com/issues/40011610)
by David last year.

We have recently started looking into reducing the number of Elasticsearch
versions that are supported in Gerrit, particularly to remove support for those
versions that have reached EOL.  See [issue 40010718](https://issues.gerritcodereview.com/issues/40010718)
and [issue 40010717](https://issues.gerritcodereview.com/issues/40010717).

David mentioned that one of the reasons that Elasticsearch was defined as
experimental is because nobody (of the core maintainers and developers) was
actually using it in production. Recently, however, Luca has heard that there
are some users using it.

We concluded that we should find out how many users are using it, and which
versions. David will ask the community managers to help with this.

### Review of issues on the ESC component

ESC was asked to review [issue 40010542](https://issues.gerritcodereview.com/issues/40010542)
which is a request to make the reviewers plugin a core plugin. David Ostrovsky
has recently updated that issue to add the information required by the new
[process for adding a core plugin](https://gerrit-review.googlesource.com/c/gerrit/+/243027).

David asked why add this plugin rather than, for example, 'find-owners'
or 'owners'. The 'find-owners' plugin is developed by Google and is deployed
on the chromium-review site. Luca pointed out that their functionality is
different; 'reviewers' just adds reviewers to a change based on simple queries,
while the other two are more complex. 'reviewers' is deployed on 'gerrit-review'.

Patrick said we should decide based on whether it's useful for general users,
and asked Luca to check the download stats to see if it's popular. Patrick
will also have a look at the code to see if its quality meets the same standards
as core Gerrit.

Alice noted that the request mentions some known issues with the UI styling,
but does not elaborate. We should ask for clarification.

We did not reach a conclusion in this meeting, but will follow up in the
next meeting after the previously mentioned points have been resolved.

There were no other issues that require attention.
