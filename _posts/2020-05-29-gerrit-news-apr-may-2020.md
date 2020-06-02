---
title: "Gerrit Project News #10: April-May 2020"
tags: news
keywords: news
permalink: 2020-05-29-gerrit-news-apr-may-2020.html
summary: "Gerrit project news from April and May 2020."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Community Management work done

See the [dedicated news post](https://www.gerritcodereview.com/2020-04-22-community-managers-report.html).

## Cherry-picking topics

By using the same cherry-pick button on a change with a topic, it is
now possible to cherry-pick the entire topic. All that's required to
cherry-pick an entire topic is to specify the destination branch.

The limitations in this versions are the requirements to pick only
one destination branch to all changes in the topic, and that it is
not possible to cherry-pick a topic that has multiple changes in the
same repository and branch.

## Comments tab moved

We have renamed the "Comment Threads" tab to "Comments" and moved it
from next to "Change Log" to next to "Files".

![comments tab moved](/images/news-apr-may-2020-comments-tab.png)

## File status chips

We now have Added`(A),`Renamed`(R),`Copied`(C),`Deleted`(D),
`Unchanged`(U),`Rewritten`(W) chips after the file name on our file
list. We do not show "Modified" status anymore.

![File chips](/images/news-apr-may-2020-file-mods.png)

## Mark as active

We have a new `Mark as Active` button as a one-click action for changing
the state from `WIP` to `Active`. It is located where the `Submit`
button is.

## ESC and CM elections

The Engineering Steering Committee and Community Managers elections
[have been completed](https://groups.google.com/d/msg/repo-discuss/zHCT2IowQng/huv-6NsbAgAJ).
These were to elect members for the non-Google positions. The Google
positions were also confirmed alongside. The resulting elected and
Google positions, for both ESC and Community Managers, remain the
[same as the previous mandates](https://www.gerritcodereview.com/members.html).
