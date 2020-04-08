---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2020-03-25-esc-minutes.html
summary: "Minutes from the ESC meeting held on March 25th"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, March 25, 2020

### Attendees

David Pursehouse, Ben Rohlfs, Alice Kober-Sotzek, Patrick Hiesel

### Place/Date/Duration

Online, March 25, 12:30 - 13:30 CEST

### Next meeting

The next meeting will be held on April 7, 12:30 CEST.

## Minutes

### Gerrit News Page

Alice's summary of the new "preview/apply fix" feature is still pending
for the next issue which is due to be published at the end of this month.

We brainstormed and came up with a few more items:

- Recent bug fix releases
- Cancellation of Spring hackathon (more on this later)
- Announcement of "revert submission" feature
- Frontend has moved from bower to npm, and from HTML to JS for imports which
  is a major technical milestone

We also considered whether the "cherry pick topic" feature should be mentioned,
but concluded that it's not quite ready to be announced yet.

As usual, we invite the community to propose any items that they think would
be interesting.

### Review of open design documents

* [Threaded feedback in the change log](https://gerrit-review.googlesource.com/c/homepage/+/245316)

  The design was approved. Alice will update the conclusion and then it can
  be submitted.

* [Instance ID / name propagation in events](https://gerrit-review.googlesource.com/c/homepage/+/257972)

  Nobody had reviewed the design prior to the meeting, so we will postpone this
  until next time.

* [Authentication backend](https://gerrit-review.googlesource.com/c/homepage/+/246449)

  This is on hold for now. David will follow up with Jacek about plans to work on
  it. We also need to keep Edwin in the loop on the current status.

* [Subchecks](https://gerrit-review.googlesource.com/c/homepage/+/235693)

  Alice plans to look into the design in the next weeks.

### Marking REST API endpoints as 'beta' or 'UI only' during development

Patrick asked us to consider whether we should have a policy about marking
REST endpoints as 'beta' or 'UI only' during development so that they can be
changed without needing to respect the deprecation policy.

David pointed out that any APIs that are on the master branch, but not in any
released version, are already implicitly subject to change. If any APIs are
still under development and likely to change, it should be OK to leave them
either with minimal documentation or undocumented. The question is then how
do we mark those APIs such that they do get properly documented before a
release is made.

David proposed adding `TODO` comments in the code/documentation, and Alice
suggested using some kind of standardized marker (either a Java annotation
or a special string in comments). Everyone agreed that this is probably
overkill. Rather, it should be enough to:

- Formally document that APIs are subject to change until included in a release
- Any APIs that are only intended to be used by the UI are explicitly documented
  as such
- The release process should include checks that newly added APIs are properly
  documented

Patrick will propose documentation updates to formalize this.

### Proposal to change the date format in REST APIs

Sven Selberg (Axis) [wrote to the mailing list](https://groups.google.com/d/msg/repo-discuss/zqanS8yGZf0/gwi6std-HAAJ)
with a proposal to change the date format used in REST APIs to use ISO-8601
timestamps.

We dicussed the proposal and the ways in which it could be implemented:

- Just replace the currently used format with ISO-8601

  This is a no-go because it will likely break many clients that rely on
  the current format.

- Add an additional field, alongside the existing one, and deprecate the existing

  This will allow existing clients to work as before. However, clients that
  want to use ISO-8601 will need to be changed to use the new field(s). Then,
  when the old field is removed (and the new field potentially renamed to
  the old name) clients will break and/or need to be adjusted.

- Introduce a configuration option to use ISO-8601

  Clients will still need to be able to handle both formats, to work with
  servers that do/don't enable the option.

We concluded that while it would be technically possible, it doesn't bring any
significant benefit that would justify the effort and overhead, so we will reject
the proposal. Ben will follow up with Sven to get more information, i.e. if there
are any concrete benefits that we have overlooked.

### Versioning of the REST API

Versioning of the REST API has been mentioned before, on the mailing list and
at hackathons. Alice raised it again in the context of the previous discussion
about timestamp formats; if we have a versioned API it might be easier to make
such changes.

Patrick raised the point that if we maintain a versioned API, we need to keep
all the code that implements previous versions, rather than just replacing them.
David pointed out that most API frameworks (assuming we would use one) make it
easy to do that.

Ben questioned whether there is any high impact reason to do it, and we should
not buy into the additional complexity it would bring otherwise.

We concluded that we will not pursue this now. We may revisit it later.

### Localization

Teng Long (Alibaba) [posted to the mailing list](https://groups.google.com/d/msg/repo-discuss/urw3doTtMr8/f_k7P9A8AwAJ)
to ask about support for localization ("L10N") in Gerrit, which would be very
useful for users in countries like China where English ability is not as
common as in other countries.

Until now the consensus has been that Gerrit is English-only, and all the
UI texts, error messages, etc, are hard coded in English.

Ben said that it would be a huge effort to support this; the Google team is
not likely to have resources to work on it now, and it's not likely possible
for someone outside the existing community to be able to do it.

David mentioned that Teng Long is keen to work on it, and in fact has
already pushed a couple of changes related to it. Also, from prior experience
at Sony in Japan, localization to Japanese would probably also be welcomed.
David also reminded that git already supports localization, as does Jenkins.

Both Patrick and Alice pointed out that it's not only the UI and error messages
that need to be localized. Gerrit also stores hard-coded English strings in NoteDb
and it would be difficult to get around that.

Patrick mentioned that since we are constantly adding/changing error messages
and the UI, we would also need constant updates to translations. Alice said
that for missing translations it should fall back to the default, and David
mentioned that other large OSS projects have a specfic "L10N coordinator"
that deals with this.

Ben's main concern is complexity, and worries that the team is too small to
get it done. For the next quarter the team is focussing on accessibility
(A11Y); since both L10N and A11Y exist in the same space they should be done
sequentially rather than in parallel.

In conclusion, we agree that having L10N is a good idea, but for now we don't
think it's something we can realistically work on. We will reevaluate this
once the A11Y work is completed.

### Pending Library Upgrades

David asked the Googlers to follow up on some of the library upgrade changes
that are still under review pending the Library-Compliance label.

Updates to gson, junit, guice and caffeine are not critical. They are only
to keep up with the latest versions. Alice approved and submitted the guice
upgrade, and will follow up on gson later. The junit and jetty upgrades are
difficult as they require work internally at Google.

The upgrade of Lucene requires index version changes. Patrick will look into
the feasibility of doing this in Google.

### Hackathon/Summit Planning

Due to the current situation with Coronavirus (COVID-19) it will not be possible
to go ahead with a Spring Hackathon or User Summit. Instead, we will look into
the possibilty of doing a remote/virtual hackathon as proposed by Luca.

Ben and David both expressed doubts about whether it would be effective. Most
of the Gerrit contributors work remotely from each other anyway; the main
benefit of attending a hackathon is being able to allocate a block of time
exclusively for working on Gerrit, and being colocated with others.

Ben suggested we could use a permanent virtual meeting room (hangout or
similar), but this would need to be coordinated with attendees: Who would actually
want to attend virtually? What do they want to get out of it? We should reach out
to the non-Google attendees that typically come to a Hackathon and ask them
what they would like to have instead.

David will follow up with Luca to dicuss how to proceed.

### Upcoming releases

Since we usually make a new major release during the hackathon, and we had
planned to release 3.2 during the now-cancelled Spring Hackathon, we need to
consider when we will release 3.2. No conclusion was reached; we will discuss
offline.

David is planning to make new 3.0.x releases and 3.1.x releases by the end
of this week.

### Review of issues on the ESC component

There were no issues that require attention.
