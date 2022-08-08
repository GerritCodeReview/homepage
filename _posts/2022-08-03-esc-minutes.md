---
title: "Gerrit ESC Meeting Minutes"
tags: esc
keywords: esc minutes
permalink: 2022-08-03-esc-minutes.html
summary: "Minutes from the ESC meeting held on Aug 3, 2022"
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Engineering Steering Committee Meeting, Aug 3, 2022

Han-Wen Nienhuys, Luca Milanesio, Saša Živkov

### Next meeting

Sept 7, 2022

### Clarification of rolling version upgrade policy

Confusion at Google regarding support status for rolling upgrades.

This was documented [in the 3.2 release
notes](https://www.gerritcodereview.com/3.2.html#zero-downtime-upgrade),
as an experimental feature. As it relies on the HA plugin which itself
is not a core plugin, this remains experimental.

Upgrades, including 'rolling upgrades', must be planned with care. A
new version might write data for new features, or enforce submission
criteria with different business logic, leading to unpredictable
behavior changes.

### Public sector use of Gerrit

Han-Wen: heard that in Europe, there is interest in open source from
the Public Sector, as it quells fears over being dependent on US
companies. Does anyone know of public sector Gerrit users?

In the UK, there are laws to promote open source in government. Luca
will check if there are public references we could mention on the website.

### Roadmap

Han-Wen will document quarterly objectives from Google.

SAP is busy moving Gerrit deployment to k8s. Gerritforge is focused on
JGit changes affecting performance.

