---
title: "Gerrit ESC Meeting Minutes, April 1st, 2026"
tags: esc
keywords: esc minutes
permalink: 2026-04-01-esc-minutes.html
summary: "Minutes from the ESC meeting held on April 1st, 2026"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

**Participants**: Daniele Sassoli [DS], David Ostrovsky [DO], Ivan Frade [IF], Matthias Sohn [MS], Nasser Grainawi [NG], Terry Parker [TP], Luca Milanesio [LM]

**Next meeting**: May 6th, 2026

### Executive Summary

During our latest Gerrit Code Review sync, we addressed critical operational, security, and
technical initiatives, alongside a leadership transition as [TP] hands over management of the Google
Gerrit Team to [IF]. To safeguard the platform and combat spam, we are rolling out a two-step
deployment plan to restrict voting and commenting to trusted contributors, while concurrently
exploring enhanced moderation permissions for community managers. On the technical front, we
successfully resolved JGit replication failures by clearly defining the synchronization scope
(specifically `servlet-4` and `master`), and outlined a clear roadmap to make Java 25 the
mandatory standard by Gerrit v3.16. Finally, acknowledging the recent loss of key historical
contributors, the team highlighted the urgent need to collaboratively build "guardrails" — such as
targeted load tests and automated invariants to ensure project stability and quality as we
evolve.

---

### 1. Team Updates at Google
[TP] announced an upcoming move to a different position within Google. Management of the Gerrit
Team at Google will be officially handed over to [IF], who has been an active committer in the
JGit project for several years.

### 2. Spam Prevention
To combat spam on `gerrit-review.googlesource.com` and other public-facing Gerrit setups (e.g.,
GerritHub.io), the team discussed restricting the ability to vote or comment on changes. The
objective is to ensure that only members of a "trusted contributors" group (such as those in
"repo-discuss") have these permissions.

An initial change drafted by [DS] was reviewed and merged, but ultimately had to be reverted due
to rollout difficulties on Google's infrastructure. To resolve this, [NG] has prepared a new
two-step deployment strategy:
* **Step 1:** [One change](https://gerrit-review.googlesource.com/c/gerrit/+/454501/4) adds the
necessary permissions to the system without actively enforcing them.
* **Step 2:** A [second change](https://gerrit-review.googlesource.com/c/gerrit/+/450463/16) will
subsequently require and enforce these permissions.

### 3. Content Moderation
There is ongoing concern regarding spam on closed changes and the current inability of community
managers to remove offensive, discriminatory, or inappropriate content. Currently, only system
administrators hold the permissions required to perform these actions.

The group agreed that better moderation tools are necessary. We plan to consult with Google's
internal trust teams regarding the potential elevation of permissions for community managers. This
would allow them to remove spam while ensuring all compliance-relevant records
can't be modified.

### 4. Replication and Infrastructure Issues
The team addressed recent failures in the replication mechanism on
`gerrit-review.googlesource.com`. Specifically, replication  from the upstream JGit repository to
`gerrit-review.googlesource.com` of the `servlet-4` and some security fix branches was failing.

* **Resolution:** [LM] and [MS] clarified that the intent is *not* to replicate all internal JGit
branches (e.g., `refs/changes/*/meta`), which are correctly blocked for security reasons on
`gerrit-review.googlesource.com`. Rather, the goal is to synchronize only the branches required
to build Gerrit Code Review with JGit from source (specifically, `servlet-4` and `master`).
* **Status Update:** [TP] confirmed that replication for the security fix branches from
`gerrit-security-fixes` to `gerrit` has successfully resumed. Synchronization for the JGit
branches was pending a finalized list of necessary branches, which has now been clearly defined.

### 5. Java 25 Migration
Java 25 is the new LTS release, and the project is preparing to migrate. [TP] confirmed that Java
25 is available internally and Google has no objections to the project moving forward with
this upgrade.

**Migration Roadmap:**
* The team will utilize two CI jobs on the Gerrit `master` branch during the transition phase to
ensure backward compatibility.
* **Gerrit v3.15** will be released on Java 25, but will retain source-level compatibility with
Java 21.
* Starting from **Gerrit v3.16**, Java 25 will become mandatory, and support for Java 21 will end.

### 6. General Maintenance and Collaboration
Maintainers expressed their solidarity with Google regarding the recent loss of major historical
contributors to the project. This transition has understandably created challenges in maintaining
stability and evolving the codebase.

To mitigate risk moving forward, [TP] requested cross-team assistance in implementing stronger
*"guardrails,"* such as targeted load tests and automated invariants, to guarantee code quality
as the project scales.

---

### Action Items

1. **spam Prevention Implementation:**
    * **[IF]:** Contact Edwin to discuss removing a "-2" vote on the
    [proposed change](https://gerrit-review.googlesource.com/c/gerrit/+/450463/16) that
    introduces the new commenting permissions.
    * **Google Team Members:** Audit the `All-Projects` access settings to verify that no code
    review permissions are being inadvertently inherited by standard registered users.
    * **All:** Once the initial permission changes are successfully merged, evaluate follow-up
    actions, such as automatically blocking reviews on read-only projects.

2. **Content Moderation:**
    * **Project Leadership:** Initiate discussions with internal trust teams at Google to
      determine if spam-removal permissions (including the ability to remove `+1` spam votes and
      comments) can be extended to designated community managers outside of Google.
    * **Engineering Team:**: Review [proposed change](https://gerrit-review.googlesource.com/c/gerrit/+/569641),
      which introduced the dedicated global Delete Comment capability for removing comments and change messages.
    * **Engineering Team:**: Define or propose a dedicated global capability for removing votes on closed changes.

3. **Replication and Synchronization:**
    * **[TP]:** Execute the re-establishment of the broken mirroring/replication mechanisms now
    that the required branch lists have been provided.
    * *(Note: [LM] and [MS] have confirmed that only regular `refs/heads/` branches — specifically
    `master`, `servlet-4`, and the `stable-*` branches are required).*

4. **Java 25 Migration:**
    * **Engineering Team:** Proceed with the Java 25 transition, starting with the `master`
      branch where it will be set as the default output bytecode.
    * **Engineering Team:** Add a new Jenkins job on the `master` branch that enforces Java 21 source and
      target compatibility, failing if the codebase inadvertently moves to Java 25.