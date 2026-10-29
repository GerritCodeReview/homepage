---
title: "Gerrit ESC Meeting Minutes, October 28th, 2026"
tags: esc
keywords: esc minutes
permalink: 2026-10-28-esc-minutes.html
summary: "Minutes from the ESC meeting held on October 28th, 2026"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

**Participants**: Hari Jeyamani [HJ], Luca Milanesio [LM], Saša Živkov [SZ]

**Next meeting**: November 25th, 2026.

---

# Executive Summary

The October 2026 Monthly Engineering Steering Committee (ESC) meeting for the Gerrit Code Review
project centered heavily on project governance, security enhancements, and codebase maintenance. A
significant portion of the discussion focused on evaluating a new spam reduction proposal leveraging
inheritable feature flags, as well as addressing ongoing debates regarding the adoption of
artificial intelligence contribution guidelines. Both of these initiatives require further offline
review and legal clarification before final implementation.

On the administrative and technical fronts, the committee successfully aligned on several key items.
The ESC agreed to shift the recurring monthly meeting schedule earlier by one hour to better
accommodate global participants. Additionally, the committee reviewed the nomination of [HJ] as a
project maintainer, pending final trust-building at the upcoming user summit, and approved the
adoption of the Pine Leaf library to seamlessly replace the deprecated Soy/Closure templates within
Gerrit and Gitiles.

# Gerrit Engineering Steering Committee (ESC) Meeting Summary

## Security & Anti-SPAM Measures

[LM] introduced a
[new spam reduction proposal](https://docs.google.com/document/d/1GCioZymU01gacga2PKk3olM4KHvSVpeZyHVQ2b7NwUQ/edit?tab=t.0#heading=h.p2kyuzmeun5d)
from David Ostrovski aimed at addressing SPAM traffic and comments affecting Gerrit Code Review.
This replaces an older, [proposal by Dani](https://gerrit-review.googlesource.com/c/gerrit/+/454501)
that relied on complex Access Control Lists (ACLs) and resulted in problematic corner cases
and complex rollout plans.
David's approach utilizes a simpler, inheritable feature flag to block or allow spam at the project
level which is inspired by [SZ] ideas coming from the reviews of the previous change attempt.

**Implementation and Permissions:** 

The new spam-blocking feature flag can be inherited across projects, empowering administrators to 
disable spam at the `All-Projects` level or tailor it per project. Spammers are identified by their 
lack of explicit write permissions on change metadata ([LM] clarified that write permissions on any 
reference are sufficient).
Since this feature is not enforced by default, no manual migration is required unless it is explicitly
enabled. The committee deferred final approval pending a review of corner cases.

## Project Governance & Maintainership

**AI Contribution Guidelines:** 

[LM] highlighted that the [proposed AI contribution policy](https://gerrit-review.googlesource.com/c/gerrit/+/641963)
is currently going through multiple series of reviews, not converging yet, despite having already
a +2 from Matthias.
Gerrit isn't the only community discussing the AI contribution policy; the Git project is
going through the same process and found opposite ideas that do not seem to be easy to reconcile.
The Git community is deciding a different style of agreement which involves open voting of
proposals and agreement through _qualified_ majority rather than unanimity.

[HJ] compared the policy to Google's open-source guidelines and Contributor License Agreement
terms, raising questions about whether internal terms must be copied verbatim or can be modified.
The policy's adoption is currently on hold while [HJ] seeks clarification from Google's legal team.

## SOY Templates Replacement

[HJ] provided an update on the upstream deprecation of Soy templates by Google, which 
impacts both Gitiles and Gerrit. Google has successfully tested the Pine Leaf library as a replacement, 
verifying full functionality with pixel-match UI tests. [LM] approved the replacement library, 
aligning the project to transition away from the deprecated templates as long as they function 
comparably to the previous ones.

## Action Items

* **[HJ] [SZ] Review Spam Proposal:** Analyze David's spam reduction design proposal to identify any 
  potential corner cases and evaluate the feasibility of integrating it with future AI comment 
  control functionalities.

* **[HJ] Clarify AI Guidelines:** Follow up with Google's legal team by the end of the week to 
  secure confirmation regarding AI contribution guidelines and ensure alignment with corporate 
  open-source policies.
