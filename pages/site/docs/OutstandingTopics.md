---
title: "Outstanding Topics"
permalink: outstandingtopics.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

Following a [discussion on the mailing list]
(https://groups.google.com/forum/#!topic/repo-discuss/qKz7AtZDlC4) we decided to
create a summary page containing the list of outstanding topics that are
currently under review and deserve a particular attention because of their
nature.

The purpose of this page is to keep track of them and prevent the risk of them
being forgotten in the Gerrit changes backlog. The topics listed here are either
related to the Gerrit architecture or to some fixes to severe bugs that need
particular attention and time for being reviewed and merged.

Currently outstanding topics are: 1. [Top-menu-loading]
(OutstandingTopics#Top_menu_loading.md) 1. [auth-backends-HttpAuthProtocol]
(OutstandingTopics#Pluggable_authentication_backend.md) 1. [secure-store]
(OutstandingTopics#Secure_Store.md) 1. [angular-gerrit-integration]
(OutstandingTopics#Angular_Gerrit.md)

--------------------------------------------------------------------------------

# Top-menu loading

Refactor the top-menu loading mechanism in order to enrich the current REST-API
to fetch its entire content from the backend. Currently it is a "mixed" GWT +
REST-API driven, with part of the logic in GWT and other in the REST-API.

The inability to control the top-menu from a REST-API forbids plugins (or other
alternative Gerrit GUIs) to render Gerrit header. With this change it will be
potentially possible to box the Gerrit top-menu into a different L&F.

*   Gerrit changes: [changes]
    (https://gerrit-review.googlesource.com/#/q/status:open+project:gerrit+branch:master+topic:top-menus)
*   Owner: [Luca]
    (https://gerrit-review.googlesource.com/#/q/owner:%22Luca+Milanesio%22+status:open)
*   Status: review started (+1)
*   Issues: Need extra reviewers with +2 permissions to finalise the change.

# Pluggable authentication backend

Replace the current Gerrit authentication infrastructure, mainly based on
mega-switch/case with the list of protocols/methods supported, with a new
plugin-based authentication back-end.

These changes would allow Gerrit to be more extensible, avoiding further growth
of the mega-switch/case all over the code and support the ability to load user
plugins to support other authentication systems in the same way that Gerrit
groups have been refactored years ago.

*   Gerrit changes: [changes]
    (https://gerrit-review.googlesource.com/#/q/status:open+project:gerrit+branch:master+topic:auth-backends-HttpAuthProtocol)
*   Owner: [Dariusz]
    (https://gerrit-review.googlesource.com/#/q/owner:%22Dariusz+%25C5%2581uksza%22+status:open)
*   Status: review started, partially merged
*   Issues: after having merged part of it, the review is now stuck. Needs Shawn
    attention as the first attempt to merge it broke the Gerrit authentication.

# Angular Gerrit

Dariusz presented at the Gerrit User a prototype for leveraging the REST-API
through an AngularJS UX. It has been published to GitHub at
https://github.com/dluksza/angular-gerrit.

In order to use the Gerrit-Angular integration a set of changes in the Plugin
infrastructure are needed and have been uploaded for review.

*   Gerrit changes: [changes]
    (https://gerrit-review.googlesource.com/#/q/status:open+topic:angular-gerrit-integration)
*   Owner: [Dariusz]
    (https://gerrit-review.googlesource.com/#/q/owner:%22Dariusz+%25C5%2581uksza%22+status:open)
*   Status: changes submitted, topic created.
*   Issues: None at the moment.
