---
title: "Gerrit User Summit 2026 - About"
permalink: /overview.html
---

# Gerrit User Summit 2026 - About

## What is Gerrit Code Review?

Gerrit is a web-based code review system that enables teams to collaborate on
Git repositories with powerful patchset based review workflows, fine-grained
permissions, and seamless integration with CI/CD pipelines.

If you are new to Gerrit, you may read a
[Quick Introduction](https://gerrit-review.googlesource.com/Documentation/intro-quick.html)
directly from the Google-hosted documentation:

> Gerrit is intended to provide a lightweight framework for reviewing every commit before it is
> accepted into the code base. Changes are uploaded to Gerrit but don't actually become a part of
> the project until they've been reviewed and accepted.

## What is Gerrit User Summit?

Gerrit User Summit is **the** annual event for everyone in the Gerrit Code Review community —
users, admins, contributors, and maintainers from organisations large and small, all coming
together to share experience, exchange ideas, and shape the future of the project.

Past summits have featured talks on large-scale Gerrit deployments, plugin development, CI/CD
integrations, performance tuning, migration stories, and deep-dives into new Gerrit features.
Sessions range from beginner-friendly introductions to advanced technical discussions, making
the event valuable whether you're evaluating Gerrit for the first time or have been running it
at scale for years.

With 24+ events held across the USA, UK, Germany, Sweden, and France, the summit has built a
strong tradition of open, community-driven knowledge sharing.

## Who Attends?

The summit brings together a diverse cross-section of the Gerrit ecosystem:

- **Gerrit administrators** managing installations at companies of all sizes
- **Software engineers** using Gerrit day-to-day who want to get more out of it
- **Plugin and integration developers** building on top of the Gerrit platform
- **Gerrit contributors and maintainers** working on the core project
- **Engineering leaders** evaluating or evolving their code review workflow

No matter where you sit in that list, you will find sessions and conversations relevant to you.

## Gerrit Community in Numbers

Thanks to the [Gerrit Analytics platform](https://analytics.gerrithub.io) contributed by
GerritForge to the project, we have up-to-date metrics about the project, automatically
extracted from Git commits and reviews on Gerrit.

- 17 years of activity
- 24+ events in USA, UK, Germany, Sweden, and France
- 1000+ contributors worldwide from 300+ organisations
- 310+ releases
- 204 repositories
- 166+ plugins
- 60k+ commits

## Organised By

The Gerrit User Summit is organised by volunteer Gerrit community managers who give their time
to make the event happen for the community.

<div class="organiser-grid">

  <div class="organiser-card">
    <div class="organiser-name">Matthias Sohn</div>
    <div class="organiser-org">SAP</div>
    <p>Gerrit contributor and JGit maintainer, Matthias has been a central figure in the Gerrit
    community for over a decade, driving technical progress and community health at SAP and beyond.</p>
  </div>

  <div class="organiser-card">
    <div class="organiser-name">Nasser Grainawi</div>
    <div class="organiser-org">Qualcomm</div>
    <p>Gerrit contributor and community advocate at Qualcomm, Nasser brings the perspective of
    running Gerrit at scale in a large enterprise environment and has been instrumental in growing
    the summit's reach.</p>
  </div>

  <div class="organiser-card">
    <div class="organiser-name">Daniele Sassoli</div>
    <div class="organiser-org">GerritForge</div>
    <p>Gerrit contributor and community manager at GerritForge, Daniele has been organising Gerrit
    summits and fostering the open-source community around Gerrit Code Review for many years.</p>
  </div>

</div>

All three organisers are volunteering their time to bring the community together.
Questions about the event? Reach out on the
[repo-discuss mailing list](https://groups.google.com/g/repo-discuss).

<style>
  .organiser-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 24px 0 16px;
  }
  .organiser-card {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 22px;
    transition: border-color 0.2s;
  }
  .organiser-card:hover { border-color: rgba(249,115,22,0.35); }
  .organiser-name {
    font-weight: 700;
    font-size: 16px;
    color: var(--text);
    margin-bottom: 4px;
  }
  .organiser-org {
    font-family: "DM Mono", monospace;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
  }
  .organiser-card p {
    font-size: 14px;
    margin: 0 !important;
    line-height: 1.7;
  }

  @media (max-width: 680px) {
    .organiser-grid { grid-template-columns: 1fr; }
  }
</style>
