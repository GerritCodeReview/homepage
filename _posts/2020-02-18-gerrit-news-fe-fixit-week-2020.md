---
title: "Gerrit Project News #7: Gerrit Frontend Fixit Week 2020"
tags: news
keywords: news
permalink: 2020-02-18-gerrit-news-fe-fixit-week-2020.html
summary: "Gerrit project news from Frontend Fixit Week."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Fixit Week Summary
In first week of February 2020 was Fixit Week for the frontend team. We focused
on fixing all the little things that pile up and otherwise don't get attention.
We were able to fix around 36 issues. Big thanks to all contributes who join us.

## Fixit Highlights
### Hovercard for blame annotation 
[Change](https://gerrit-review.googlesource.com/c/gerrit/+/253121) 
introduces new hovercard with commit message when hovering over blame annotation.

![Blame Hover Card](/images/fixit-week-2020-blame-hovercard.png)


### Improving layout of label scores
[Change](https://gerrit-review.googlesource.com/c/gerrit/+/253165)
improves layout to table so the buttons are not so far away from label name.
Also add a background-color on hover to highlight which label you are about to vote on.

![Label Scores](/images/fixit-week-2020-label-scores.png)

### Warn user in submit dialog about unresolved comments
[Change](https://gerrit-review.googlesource.com/c/gerrit/+/253130)
introduces new warning when submitting change with unresolved comments.
It's not blocking submit, it's just the last notification about unresolved comments.

![Warn about unresolved comments](/images/fixit-week-2020-unresolved.png)

### Honor date format from preference when display dates
[Change](https://gerrit-review.googlesource.com/c/gerrit/+/253116)
fixes some places where we didn't honor date format that user set in user settings.
For example if user set date format `3.Jun` instead of default `Jun 3` dashboard
will be change as in screenshot below.


![Honor date format](/images/fixit-week-2020-dates.png)

## All Fixit Improvements
* [Process links if leading whitespace are missed](https://gerrit-review.googlesource.com/c/gerrit/+/253169)
* [Show files with comments in diff-view file list](https://gerrit-review.googlesource.com/c/gerrit/+/253221)
* [Improve error dialog for 404 errors](https://gerrit-review.googlesource.com/c/gerrit/+/253225)
* [Add patchset navigator for findings tab](https://gerrit-review.googlesource.com/c/gerrit/+/252762)
* [Change button in gr-reply-dialog: Rename Save to Send](https://gerrit-review.googlesource.com/c/gerrit/+/253220)
* [Small redesign of diff expansion row](https://gerrit-review.googlesource.com/c/gerrit/+/252614)
* [Replace circled i from Unicode with proper icon](https://gerrit-review.googlesource.com/c/gerrit/+/252944)
* [Add title and shortcuts for some links and buttons](https://gerrit-review.googlesource.com/c/gerrit/+/253544)
* [Issue linkification should not work across two line breaks](https://bugs.chromium.org/p/gerrit/issues/detail?id=12277)
* [Add tracking (metrics) on keyboard shortcut usage](https://gerrit-review.googlesource.com/c/gerrit/+/253653)
* [Show X-Gerrit-Trace in error dialog if exists](https://gerrit-review.googlesource.com/c/gerrit/+/253541)
* [Link in Blame annotation to commit should go directly to commit](https://gerrit-review.googlesource.com/c/gerrit/+/253127)
* [Allow delete change message from the UI](https://gerrit-review.googlesource.com/c/gerrit/+/253412)
* [Add a proper message for no threads in findings tab](https://gerrit-review.googlesource.com/c/gerrit/+/253224)
* [Support ctrl+enter for move change dialog](https://gerrit-review.googlesource.com/c/gerrit/+/253414)