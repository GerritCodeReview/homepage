---
title: "RoadMap"
permalink: roadmap.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Introduction

There are many ideas suggested, and discussions which lead to decisions about
the future direction and designs of Gerrit which happen in many forums: on IRC,
the ML, at the hackathons, and in the issue tracker. It can be hard for an
outsider to get a feel for where Gerrit might be headed in the near, medium, and
long term. Of course, since this is an open source project, code speaks loudly.
However there are times when the maintainers feel that certain pathes are not
the way forward, and the desired alternative may have already been proposed as
the way that Gerrit should move. It can be helpful to developers to get an idea
about these decisions before embarking on developping a feature. Naturally,
there are also times when people just want to get a feel for what might be
coming down the pike. So we will attempt to illustrate some of these decisions
here.

## Architecture

*   The REST API is viewed as the longterm stable approach for RPCs with the
    Gerrit Server. At this point new UI elements and new ssh commands should be
    developed against it. If a new service is created, it should extend the
    current REST API or implement new pieces.

*   The hooks will eventually be moved to plugins.

*   The Database will eventually be removed from Gerrit. Authoritative data will
    mostly be pushed into the project repositories. An indexing service such as
    Lucene will be used to provide fast access to data. While this is the long
    term plan, some pieces have already been moved out of the DB and into the
    repos, for example project configuration and ACLs. Newer features are
    expected to take a similar approach when possible.

*   New user preferences should be placed in a (yet to be born) repo named
    All-Users. Each users preferences will live in a gitconfig style file under
    a reference named refs/users/xxx/accountid where xxx is accountId mod 1000.
    Since users shouldn't be able to access other users' refs, this structure
    can be hidden from them and they should be able to access their refs via
    refs/heads/master

*   Groups should probably gain a similar All-Groups repo. The membership file
    could live there. See the [gitgroups plugin]
    (https://gerrit-review.googlesource.com/35780).

*   Authentication will eventually be moved entirely to plugins. Much work has
    already been done on this.
