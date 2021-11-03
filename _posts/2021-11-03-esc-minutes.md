---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-10-06-esc-minutes.html
summary: "Minutes from the ESC meeting held on Nov 3, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---



## Engineering Steering Committee Meeting, Nov 3, 2021

Han-Wen Nienhuys, Luca Milanesio, Saša Živkov, Patrick Hiesel

### Next meeting

Dec 1, 2021

## Minutes

## Action items

Discuss the proposed new maintainer(s) and send nomination(s) for the new maintainer(s).

Check with Milutin about a solution for the Trojan source issue.

## Request from RedHat for a dedicated channel for notifying about the security releases

We discussed some proposals how to use existing communication means:
- add something to the email subject, for example [SECURITY]
- use CVEs

Additional feedback from RedHat is necessary to make a decision.


## Removal of the ElasticSearch support code from Gerrit 3.5

That code was never production ready. The consensus is to remove it.

## Roadmap

The Roadmap on the homepage is likely obsolete. Current roadmap which the ESC considers in
every meeting is too detailed. ESC should only maintain a higher-level roadmap, all other
details in the issue tracker. We should discuss the roadmap on a quarterly basis and on demand.

## Trojan source issue

Using special unicode characters may render a diff view in Gerrit UI which is different from
what the compiler sees.

## Scoped credentials

OpenStack requested a "scoped credentials" feature. Currently, the generated http password is
a kind of scoped credentials where the allowed set of actions is defined by the allowed set
of actions of the user owning these credentials. OpenStack would like to have the possibility
to generate multiple credentials and assign different scopes to each, similar to the OAuth scopes.

We discusssed this requirement. It is not clear how would the "scoped credentials" feature
work together with the (fine grained) permission system in Gerrit and what exactly the possible
set of scopes would be. For example, a "Git" scope which would allow only Git operations could
be imagined. However, in Gerrit it is possible to do many things over the Git protocol, including
setting topics, reviewers, hashtags, etc...

Luca will reach out OpenStack and propose a plugin-like implementation strategy, which could satisfy
their requirements.
