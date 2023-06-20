---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2021-02-02-esc-minutes.html
summary: "Minutes from the ESC meeting held on Feb 2, 2021"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Feb 2, 2021

### Attendees

Ben Rohlfs, Han-Wen Nienhuys, Luca Milanesio, Saša Živkov

### Place/Date/Duration

Online, Feb 2, 11:00 - 11:45 CET

### Next meeting

March 02, 2021 - 11:00 - 12:00 CET

## Minutes

### [Selection bug](https://issues.gerritcodereview.com/issues/40011496) in Safari

Frontend team at Google added a polyfill workaround. This works for
older versions of Safari, but not for the latest version of Safari.
This is a [browser
bug](https://bugs.webkit.org/show_bug.cgi?id=163921).

Webkit is open-source, so someone with enough time could find out what
is going on, but Google users are not impacted, so Google can't prioritize a
more in-depth investigation, especially given that this is a browser bug.

Some deployments see larger shares of Safari users, and it's the
default browser for mobile iOS platforms. Luca will try to reach out
to the Safari team to get this resolved.


### 24h grace period to let others comment

Context is https://gerrit-review.googlesource.com/c/gerrit/+/294087.

There used to be an unwritten rule to let other timezones look at the
change too. For some changes (eg. fixes), it is appropriate to submit
much more quickly. This change was not a trivial fix, though.

Resolution: introduce a 24h waiting period for changes that imply a
long-term support commitment, eg. user-visible features, or API
extensions.


### ElasticSearch moved to SSPL

ElasticSearch moved releases to SSPL starting 7.11. Google is opposed
to SSPL software on principle. SAP also forbids it.

Context: index support started with Lucene and Solr. Solr was clunky,
so collabnet and ericsson worked to move to Elastic, but neither
deployed. Alibaba seems to be using it.

Long term technical solution: use ES as a module (ie. a non-swappable
part of Gerrit, compiled separately). ES also slowed down our
development, so getting rid of it may be a net positive.

Resolution: we will freeze the version for now. Han-Wen will reach out
to Jacek and Marco to see if they have interest in maintaining it.

### DoS fix for HTTP sessions.

Advance notice by large deployments was well received. Upgrade went smoothly.

Got requests to document of our advance notice process (OpenStack).
Luca will followup.

Wikimedia builds from source, and wants to see the patch. We could
create `refs/heads/security/*` in main gerrit repo, but risky: it's
easy to upload to the wrong branch, so we'll keep using the separate
repository.

Resolution: find a way to provide select individuals view permission
on our security fixes repo.

### Event rewrite at Google

Started, but we had no plan for integration into upstream, so taking
internally for now.

The rough plan is: provide diff between NoteDb SHA1s as protocol
buffer, eg. by comparing two ChangeNoteStateProto proto. Internally,
we will ship this to our internal pubsub systems.

Marcin is anxious to jump in. Han-Wen: need a plan to decide how these
diffs are generated in gerrit upstream, and then hook them up to the
event machinery.

Han-Wen will publish a sanitized version of our internal design doc.

### Inter-plugin communication?

First attempt in
https://gerrit-review.googlesource.com/c/gerrit/+/54428, but abandoned
because the scripting plugin doesn't fit.

This is a feature with potential future support implications. For
example, if we document that loading other plugins by reflection
works, we promise to not break it.

We don't want to repeat Jenkins' mistake, where every plugin can call
into everything creating a maintenance nightmare.

Do we want a designdoc? Consensus: yes. Topics to consider:

*   should plugins be testable?
*   what happens to a caller if a dependency provider is unloaded?
*   does verification (eg. type checking) happen compile time or runtime?
*   which parts of a plugin are available to callers?

Currently there are already methods that plugins can use to communicate:

1.  send events (but: very loose coupling)
2.  share a common interface loaded as libmodule.

### Long reviews leading to demotivation

[Recent
change](https://gerrit-review.googlesource.com/c/plugins/replication/+/292364)
took a lot of roundtrips; stressful experience for the uploader and reviewer.

Should we codify boy scout rules ("change should do 1 thing",
"leave code better than it was before", "reviews should enlighten")?

Consensus: the rules in abstract seem obvious, but subjective when
applied. This is a people problem, so have to escalate earlier to CMs.

