---
title: "Elasticsearch"
permalink: elasticsearch.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

The following table shows the compatibility of Gerrit Code Review with Elasticsearch.


| Elasticsearch Version | Minimum Gerrit Version | Notes                                     |
|-----------------------|------------------------|-------------------------------------------|
| 2.4.x                 | 2.14.8 or 2.15.3       | Support discontinued in 2.15.8 and 2.16.1 |
| 5.6.x                 | 2.14.8 or 2.15.3       |                                           |
| 6.2.x                 | 2.14.8 or 2.15.3       |                                           |
| 6.3.x                 | 2.14.10 or 2.15.3      |                                           |
| 6.4.x                 | 2.14.12 or 2.15.4      |                                           |
| 6.5.x                 | 2.15.8 or 2.16.1       |                                           |
| 6.6.x                 | 2.15.10 or 2.16.5      |                                           |
| 6.7.x                 | 2.15.13 or 2.16.8      |                                           |
| 7.0.x                 | 2.15.13 or 2.16.8      | See note below about upgrades             |
| 7.1.x                 | 2.15.14                |                                           |

Indices created in Elasticsearch 5.x or earlier will need to be reindexed with
Elasticsearch 6.x in order to be readable by Elasticsearch 7.x. See
[breaking changes in Elasticsearch 7.0](https://www.elastic.co/guide/en/elasticsearch/reference/7.0/breaking-changes-7.0.html)
for details.
