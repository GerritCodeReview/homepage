---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2025-02-26-esc-minutes.html
summary: "Minutes from the ESC meeting held on February 26, 2025"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

# Engineering Steering Committee Meetings, February 26, 2025

**Participants**: Edwin Kempin [EK], Luca Milanesio [LM], Saša Zivkov [SZ], Matthias Sohn [MS]

**Next meeting**: March 26, 2025

# Executive Summary

The meeting covered Google AI's use for meeting minutes ([LM] 
reported 80% time savings but noted accuracy issues), Gerrit's upgrade to 
JGit master and servlet upgrade challenges ([SZ] approved Thomas's 
[password rotation design document](https://gerrit-review.googlesource.com/c/homepage/+/455521),
postponing the dynamic submittable 
conditions document), and JGit's Servlet 4 downgrade ([MS] 
successfully downported, needing master branch verification; Jetty 12 
upgrade confirmed with [EK], requiring executive sponsorship for 
Servlet API upgrade). [SZ] also discussed Java 21 adoption, including 
virtual threads and record usage, suggesting similar Gerrit core updates.

# Gemini AI for Meeting Minutes

[LM] reported that using Gemini AI for meeting minutes saved at 
least 80% of their time, although they needed to double-check for accuracy 
in assigning action items. They also experimented with using AI for release 
notes but found that the results contained hallucinations and required more 
time to fix than writing them manually. [LM] prefers writing 
release notes as a learning exercise and to prepare presentations, rather 
than for efficiency alone.

# Gerrit Upgrade and Design Documents

The meeting primarily focused on upgrading Gerrit to the latest JGit master, 
addressing servlet upgrade challenges. [SZ] approved Thomas's design 
document for rotating passwords, as they were happy with its content and it 
was well-received. A document summarizing feature requests for dynamic 
submittable conditions lacked conclusions and was postponed until a proper 
design document is available; [SZ] will likely review it in the 
coming months, as they are already working on removing Prolog code.
[SZ] also announced a Git-based support message of the day plugin, which 
could be useful for multi-site deployment.

# JGit Update and Servlet Upgrade

[MS] presented their work on downgrading to Servlet 4 in JGit. They 
created a new branch [servlet-4](https://github.com/eclipse-jgit/jgit/tree/refs/heads/servlet-4)
based on the master branch and successfully 
downported it. The update involved addressing deprecated methods and 
adapting to API changes in several interfaces and plugins. [LM] 
noted that some changes needed verification after merging with the master 
branch. 

[MS] discussed upgrading Jetty to version 12 with [EK], who 
confirmed it wouldn't be a problem for Google. [MS] successfully 
solved a problem in the test class used for testing the HTTP protocol by 
reverting the Servlet 6 update and noted that Jetty 12 offers performance 
improvements and allows for the optional use of Servlet APIs. 

The team agreed that upgrading the Servlet API is a significant undertaking 
that needs to be funded and prioritized; it is unlikely to happen without 
executive sponsorship. They also discussed approaches to the upgrade 
process, including an atomic approach or batch updates using tools. There is 
no current formal voting system for such decisions; instead, central teams 
often handle them and coordinate with other teams.

# Java 21 and Virtual Threads

[SZ] mentioned that they are now using Java 21 and replaced AutoValue 
with records in the message of the day plugin. They suggested considering a 
similar approach for Gerrit core, potentially using a migration tool first. 
[SZ] also introduced the concept of virtual threads in Java 21, 
highlighting the simplification they offer to concurrent programming and 
their potential application within Gerrit. 

[MS] mentioned the need to update to a site engine that supports 
virtual threads before implementing them.
