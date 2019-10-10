---
title: "Elasticsearch"
permalink: elasticsearch.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

The following table shows the compatibility of Gerrit Code Review with Elasticsearch.


| Elasticsearch Version | 2.14.x  | 2.15.x  | 2.16.x  | 3.x   | Notes                                            |
|-----------------------|---------|---------|---------|-------|--------------------------------------------------|
| 2.4.x                 | 2.14.8  | 2.15.3  |         | 3.0.0 | Support discontinued in 2.15.8, 2.16.1 and 3.0.0 |
| 5.6.x                 | 2.14.8  | 2.15.3  |         | 3.0.0 |                                                  |
| 6.2.x                 | 2.14.8  | 2.15.3  |         | 3.0.0 |                                                  |
| 6.3.x                 | 2.14.10 | 2.15.3  |         | 3.0.0 |                                                  |
| 6.4.x                 | 2.14.12 | 2.15.4  | 2.16    | 3.0.0 |                                                  |
| 6.5.x                 |         | 2.15.8  | 2.16.1  | 3.0.0 |                                                  |
| 6.6.x                 |         | 2.15.10 | 2.16.5  | 3.0.0 |                                                  |
| 6.7.x                 |         | 2.15.13 | 2.16.8  | 3.0.0 |                                                  |
| 6.8.x                 |         | 2.15.16 | 2.16.11 | 3.0.2 |                                                  |
| 7.0.x                 |         | 2.15.13 | 2.16.8  | 3.0.0 | See note below about upgrades                    |
| 7.1.x                 |         | 2.15.14 | 2.16.9  | 3.0.1 |                                                  |
| 7.2.x                 |         | 2.15.15 | 2.16.10 | 3.0.2 |                                                  |
| 7.3.x                 |         | 2.15.16 | 2.16.11 | 3.0.2 |                                                  |
| 7.4.x                 |         |         |         | 3.0.3 |                                                  |

Indices created in Elasticsearch 5.x or earlier will need to be reindexed with
Elasticsearch 6.x in order to be readable by Elasticsearch 7.x. See
[breaking changes in Elasticsearch 7.0](https://www.elastic.co/guide/en/elasticsearch/reference/7.0/breaking-changes-7.0.html)
for details.
