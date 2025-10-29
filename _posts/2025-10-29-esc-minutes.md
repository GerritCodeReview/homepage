---
title: "Gerrit ESC Meeting Minutes, October 29, 2025"
tags: esc
keywords: esc minutes
permalink: 2025-09-23-esc-minutes.html
summary: "Minutes from the ESC meeting held on October 29, 2025"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

**Participants**: Edwin Kempin [EK], Luca Milanesio [LM], Saša Živkov [SZ]

**Next meeting**: January 28, 2026

## Executive Summary

[LM] confirmed the **release plan is progressing**: RC4 is out, the final RC is next Monday, and
the process is now **fully automated with security improvements**. [SZ] confirmed the **Bazel
migration from WORKSPACE to `bzlmod`** (to simplify dependencies) is in progress, [LM] proposed to
postpone its rollout to v3.14. Key topics also included the **Lucene indexing issue** (design doc pending),
new **Gerrit tool integrations** (JJ/Git Butler), and the publication of **Gerrit Summit videos**
ahead of an upcoming Munich meetup.

## Gerrit v3.13 Release Plan Status

[LM] provided a status update on the release plan, noting that RC4 was released, and the
final RC is scheduled for the following Monday. They described the recent upgrade from
Gerrit v3.12 to v3.13 as the _"easiest upgrade ever"_ with no reported issues so far;
[GerritHub.io](https://review.gerrithub.io) is already migrated smoothly without problems.

## Bazel Migration to `bzlmod` Timeline

[SZ] confirmed that Thomas Draebing and Jacek are working on the migration to `bzlmod`.
[SZ] explained that `bzlmod` simplifies dependency management by making it easier to add
dependencies, similar to using Maven, and will eliminate the huge `WORKSPACE` file.
[LM] questioned whether updates to submit-requirements for library compliance
would be needed for the modules. [EK] suggested that the library compliance check could be
adapted later by modifying the submit requirement to check for additional files.

[LM] expressed concern that the `bzlmod` migration might cause a delay for the v3.13
release and suggested moving it to v3.14 if not merged by Friday or the following Monday.
[SZ] inquired about any potential issues with using `bzlmod` from a Google
perspective. [EK] indicated they were unaware of any issues, as nobody at Google had
looked at it yet, but noted that internally they use Blaze, the internal version of
Bazel. [SZ] stated that the migration to `bzlmod` is necessary because some features
currently used are deprecated in the next Bazel 8.x versions.

## Automation of the Release Process and Security Improvements

[LM] reported that the release process from RC2 to RC4 has been fully automated. They
explained that the release change is now done by a pipeline robot, and the GPG key
signature is also done by the robot, with the encrypted key. To ensure security, the
passphrase for the GPG key is held by the release manager and not stored, preventing
automatic builds if the box is compromised. Furthermore, [LM] described a new security
measure to destroy Sonatype keys after the v3.13.0 release and recreate new ones for every
subsequent release, eliminating the risk associated with long-term key storage, similar
to an attack faced by npm maintainers.

## Transactionality and Lucene Indexing

[LM] provided an update on the transactionality issues
(see [Issue 440360427](https://issues.gerritcodereview.com/issues/440360427),
[Issue 450577969](https://issues.gerritcodereview.com/issues/450577969)
and potentially many others in the past), mentioning that Dani is tackling
some aspects. They highlighted that when Lucene fails, there are no logs generated; actually,
Lucene does not log anything through Gerrit, because the logger is a NOOP.
Dani is working on a change to configure Lucene logging and
introduce an explicit "flush" method, as Lucene currently only uses auto-flash. [LM]
explained that an explicit flash would allow for committing to a broker like Kafka
immediately afterward, which is not possible with the current misalignment. [SZ]
questioned if this only minimizes the probability of issues. [LM] clarified that the goal
is to prevent the loss of index events by leveraging the broker's message queue if the
messages haven't been committed, acting like a transaction log in a multi-site setup.

They concluded that a design document is needed for a future version to fully address the
transactionality issue even without a Gerrit multi-site setup.

## Gerrit Summit and Upcoming Meetup

[LM] announced that the [Gerrit Summit videos](https://www.youtube.com/playlist?list=PLySCWiWz9cNuiJK2Uy3foHGvkxL3fBLUC)
and presentations are now published online.
[EK] mentioned watching one of the presentations from Martin. [LM] confirmed that the
[next meetup is scheduled in Munich](https://www.meetup.com/gerritmeets/events/310709185/)
in a couple of weeks, and [EK], Matthias, and Han-Wen will be attending.

## JJ and GitButler Integration with Gerrit

[LM] shared that Skyler presented on [JJ support for Gerrit](https://youtu.be/UwIJvXMs3_0),
enabling users to clone a Gerrit project, work with JJ, and push changes without needing hooks.

[EK] questioned if this made their design document obsolete, as JJ now supports Gerrit Change-ID
in the footer. [LM] noted that the change ID in the footer may not be sufficient if changes originate
from other version control systems where the ID is in the header. [LM] strongly
recommended watching [Scott Chacon's video on Git Butler](https://youtu.be/boJOHlJj5C0),
describing its local UI as _"really, really nice"_ and much better than GitHub's interface.

They explained that GitButler works naturally with Gerrit as a client, automatically understanding
how to interact with Gerrit for creating patch sets and amending changes. [LM] added that JJ is
more suited for advanced users, while GitButler is for everyone, but noted that GitButler
is a commercial product, whereas JJ is completely open source.
