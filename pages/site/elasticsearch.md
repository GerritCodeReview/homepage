---
title: "Elasticsearch"
permalink: elasticsearch.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

The following table shows the compatibility of Gerrit Code Review with Elasticsearch.

| Elasticsearch Version | 3.1.x (EOL) | 3.2.x | Notes                                           |
|-----------------------|-------------|-------|-------------------------------------------------|
| 5.6.x                 | 3.1.0       |       | Support discontinued in 3.0.9 and 3.1.5         |
| 6.2.x                 | 3.1.0       |       | Support discontinued in 3.0.9 and 3.1.5         |
| 6.3.x                 | 3.1.0       |       | Support discontinued in 3.0.9 and 3.1.5         |
| 6.4.x                 | 3.1.0       |       | Support discontinued in 3.0.9 and 3.1.5         |
| 6.5.x                 | 3.1.0       |       | Support discontinued in 3.0.9 and 3.1.5         |
| 6.6.x                 | 3.1.0       | 3.2.0 | Support discontinued in 3.0.13, 3.1.9 and 3.2.4 |
| 6.7.x                 | 3.1.0       | 3.2.0 | Support discontinued in 3.0.13, 3.1.9 and 3.2.4 |
| 6.8.x                 | 3.1.0       | 3.2.0 | Support discontinued in 3.1.11, 3.2.6 and 3.3.1 |
| 7.0.x                 | 3.1.0       | 3.2.0 | Support discontinued in 3.1.11, 3.2.6 and 3.3.1 |
| 7.1.x                 | 3.1.0       | 3.2.0 | Support discontinued in 3.1.11, 3.2.6 and 3.3.1 |
| 7.2.x                 | 3.1.0       | 3.2.0 | Support discontinued in 3.1.13, 3.2.8 and 3.3.3 |
| 7.3.x                 | 3.1.0       | 3.2.0 | Support discontinued in 3.1.13, 3.2.8 and 3.3.3 |
| 7.4.x                 | 3.1.0       | 3.2.0 | Support discontinued in 3.2.11, 3.3.5 and 3.4.1 |
| 7.5.x                 | 3.1.1       | 3.2.0 | See note below about upgrades                   |
| 7.6.x                 | 3.1.4       | 3.2.0 |                                                 |
| 7.7.x                 | 3.1.5       | 3.2.0 |                                                 |
| 7.8.x                 | 3.1.8       | 3.2.3 |                                                 |

Indices created in Elasticsearch 5.x or earlier will need to be reindexed with
Elasticsearch 6.x in order to be readable by Elasticsearch 7.x. See
[breaking changes in Elasticsearch 7.0](https://www.elastic.co/guide/en/elasticsearch/reference/7.0/breaking-changes-7.0.html)
for details.
