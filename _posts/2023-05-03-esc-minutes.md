---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2023-05-03-esc-minutes.html
summary: "Minutes from the ESC meeting held on May 3, 2023"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Apr 12 - May 3 2023

Christophe Poucet, Patrick Hiesel, Luca Milanesio, Saša Živkov

### Next meeting

July 12, 2023

### Spring Hackathon

There weren't enough attendees to justify a face-to-face hackathon in
Munich (Germany) this year. The Gerrit Spring Hackathon took place
remotely on Discord.

### Gerrit v3.8

The release of Gerrit v3.8 happened according to plans and was officially
[announced on May 20](https://groups.google.com/g/repo-discuss/c/VwQvtFeJxCY/m/PdiqDhFWBAAJ).

The dismissal of new [Prolog rules](https://gerrit-review.googlesource.com/c/gerrit/+/360756)
has been discussed and the common agreement is to relax the constraints and
still allow them in v3.9 but stricter afterwards.

### Future of JGit hosting on Gerrit

The Eclipse Foundation announced
[the shutdown of their Gerrit server](https://gitlab.eclipse.org/eclipsefdn/helpdesk/-/issues/680)
which would have left the JGit project without a code-review platform.

Matthias Sohn, the maintainer of JGit, proposed to move the development to
[GitHub/GerritHub](https://gitlab.eclipse.org/eclipsefdn/helpdesk/-/issues/3137) which
would allow to dog-food the JGit development and also to have a resilient
and effective code-review platform, keeping the full history of the code-reviews.

### Gerrit User Summit 2023

[Volvo Cars](https://www.volvocars.com/) has offered to host the Gerrit User Summit 2023,
from Sep 30th to Oct 1st, in Gothenburg at [Volvohallen](https://goo.gl/maps/HWHd11EkEP6YPAjD7),
co-sponsored with [Polstar](https://www.polestar.com/).

The proposal was already subject to a
[public poll on repo-discuss](https://groups.google.com/g/repo-discuss/c/kpVRz_9vQB8/m/OSc9JjL5AAAJ)
with the following results:

- 38.7% are willing to attend face-to-face at Volvo Cars in Gothenburg
- 32.3% are planning to watch the event live on [GerritForge's YouTube Channel](https://tv.gerritforge.com)
- 25.8% will be watching the recording offline
