---
title: "Gerrit ESC Meeting Minutes, August 26th, 2026"
tags: esc
keywords: esc minutes
permalink: 2026-08-26-esc-minutes.html
summary: "Minutes from the ESC meeting held on August 26th, 2026"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

**Participants**: Hari Jeyamani [HJ], Luca Milanesio [LM]

**Next meeting**: August 26th, 2026.

---

# Executive Summary

The main focus of the ESC meeting was on overhauling Gerrit's security triage,
contributor permissions, and release strategy. To streamline vulnerability remediation, the
operational responsibility for routine security triage is officially transitioning from the
ESC to the Maintainers group, supported by new monthly check-ins.

Gerrit default authorization policy for reviewing changes and AI reviews is set to be
shift to the established _default deny_ as any other permission in Gerrit ACLs.
All existing multi-tenant environments like Google and GerritHub, the default
setting for AI review features must be then set at `All-Projects` level.

Finally, technical infrastructure and community planning advanced across several fronts. A tracking
document was commissioned to monitor and fund CI infrastructure gaps, while the Servlet 4 upgrade
path is being coordinated with Ivan to avoid plugin compatibility issues associated with dual
Servlet 4/6 support.

---

# Gerrit Engineering Steering Committee (ESC) Meeting Summary

## Security Management, Vulnerability Triage & Access

* **Public Bug Reporting & Ingestion**

  Recent configuration changes allow public creation of security
  bug reports without public visibility. Reports routed via the Google Open Source Engagement
  Program are expected to increase report volume, including duplicate AI-generated submissions.

* **Internal Triage Pipeline**

  Google vulnerability teams are performing initial triage to filter
  theoretical issues from actual, high-impact risks for specific hosting setups. Triage cadence will
  be set to weekly/bi-weekly to reduce the open bug backlog.

* **Access Permissions ("Trusted Contributors") for helping with security issues**

  To unblock contributors (e.g., Josh, Josie) working on security fixes without granting full
  maintainer rights, the Google contributors can be proposed to be granted the "Trusted
  Contributor" role for being entitled to access the issues and work on those.

* **Governance Shift for Security Issues**

  Day-to-day security response transitions from the ESC to the general
  Maintainer group. [LM] will lead monthly maintainer security check-ins.

* **Actions**:

  1. [HJ] will propose Josh and Josie as Trusted Contributors for security work.
  2. [LM] Schedule monthly maintainer security check-in meetings for assessing new security
     issues raised.


## Platform Policies & Documentation Clarifications

* **AI Review Default Policy**

  Default configuration for AI review and comment on changes will flip to _"denied"_
  requiring explicit host/tenant owner enablement. A rollout tracking issue and large-scale change
  management strategy will be executed.

* **AI-Generated Code Policy**

  A pending configuration change/PR for AI-generated code will be
  submitted for review, strictly adhering to established legal boundaries.

* **Actions**

  1. [HJ] Submit policy PR on AI code contribution rules in Gerrit documentation as change
     by copying and pasting the relevant legal fragments from Google AI contribution
     guidelines.

  2. [HJ] Draft tracking bug for AI review and review policy rollout timeline across the
      Google's Gerrit tenants.


## Infrastructure & Architectural Upgrades

* **CI Infrastructure Tracking**

  Commissioned a dedicated tracking document to catalog CI resource
  gaps, flakiness, and funding/capacity requirements for continuous integration.

* **Servlet 4/6 Upgrade Path**

Upgrade to Servlet 4 relies on Jetty and Google infrastructure alignment (led by Ivan Frade).
The ESC highlighted the potential confusion created in the community if Servlet 4 and 6
cohexistence would last for several years, generating plugin compatibility issues.
A short-lived compatibility overlap and migration strategy is acceptable.

* **Actions**:

  1. [HJ] To initialize CI Infrastructure gap tracking document.
  2. [HJ] Coordinate with Ivan on the Servlet 4 upgrade strategy.
