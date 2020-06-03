---
title: "Gerrit Project News #11: June-July 2020"
tags: news
keywords: news
permalink: 2020-06-03-gerrit-news-jun-jul-2020.html
summary: "Gerrit project news from June and July 2020."
hide_sidebar: true
hide_navtoggle: true
toc: true
---

## Serializing the External Groups Cache

Gerrit can be linked to external user directories like LDAP, providing Gerrit with external users and groups. External groups can be added to Gerrit to restrict access to refs and repos and are mainly used for permissions evaluation.

We implemented a significant performance improvement by serializing the external groups in-memory cache for faster lookups. We used the common serialization infrastructure used by other caches. This has an impact on Gerrit setups that require frequent server restarts, i.e. for warming up caches. For Google hosted Gerrit sites, the cache loading time for all lookup requests was reduced from a few hundreds of minutes to less than 3 minutes per day.
