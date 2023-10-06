---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2023-09-20-esc-minutes.html
summary: "Minutes from the ESC meeting held on Sep 20, 2023"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Sep 20, 2023

Christophe Poucet, Patrick Hiesel, Luca Milanesio, Saša Živkov

### Next meeting

November 2, 2023

### Gerrit User Summit 2023 Q&A and talks preparation

Chris and Saša will join the Q&A with the maintainers; the audience will
post questions directly to slido.com. Luca to prepare the collection of
questions early on, give some heads-up to the maintainers to prepare the
answers.

There are 65 places in Gothenburg and 20 in Sunnyvale; both sites are fully
booked.

### Prolog rules evaluated for closed changes

Patrick introduced the evaluation of Prolog rules for closed changes with
[Change 297966](https://gerrit-review.googlesource.com/297966)
on Gerrit v3.4, for fixing a caching issue for Google. It is not an issue
anymore for Google because of the switch to submit requirements; therefore
[Change 297966](https://gerrit-review.googlesource.com/297966) can be
reverted on the non-EOL releases and merged to master.

### X-Plugin dependency and interactions

The issue has been discussed for many years; Google is not part of the
active stakeholders because of the implementation of a different solution,
where all plugins are in the same Guice injector.

Luca to propose [Change 244472](https://gerrit-review.googlesource.com/c/gerrit/+/299472)
and the approval is subject to acceptance from the wider community.
Saša also proposed to analyse the solution implemented by Google. Patrick
should share a sample and simplified example.

### Proposal to nominate Antonio Barone (aka Tony) as new Gerrit Maintainer

Tony has been an active member of the Gerrit community for over five years
and has an excellent understanding of how Gerrit works inside and how to
run large Gerrit installations because of his involvement with the
implementation of large and complex setups.

Tony actively engages in Gerrit discussions and helps shape new features in
Gerrit, like the cache-chroniclemap libModule, providing a high-performance
backend instead of the default H2. He had a tremendous impact on the
improvement and stability of Gerrit releases, thanks to the contribution of
the AWS-Gerrit deployments and the Gatling test suites.
Tony has contributed around one thousand changes to the Gerrit project
overall, 46 of those on Gerrit core. He actively maintains all the
AWS-related plugins associated with the Gerrit multi-site architecture.

Tony has participated in several Hackathon either on-site or remote, and I
am sure all of you had the opportunity to work and have technical discussions
with him. He is very active in answering and helping people on the
repo-discuss mailing list, leveraging his expertise on both Gerrit and the
wider field of distributed systems, where he can leverage his seniority on
AWS, Google Cloud services and asynchronous communication and interaction.

### Gerrit v3.9 release plan

Luca proposed to release Gerrit v3.9 by November 2023, which is compatible
with the current status of the features in development.
The [draft release plan is available](https://gerrit-review.googlesource.com/c/homepage/+/388542)
and currently under review.