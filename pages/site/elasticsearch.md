---
title: "Elasticsearch"
permalink: elasticsearch.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

The following table shows the compatibility of Gerrit Code Review with Elasticsearch.

| Elasticsearch Version | 2.16.x  | 3.0.x  | 3.1.x | 3.2.x | Notes                                            |
|-----------------------|---------|--------|-------|-------|--------------------------------------------------|
| 2.4.x                 | 2.16    |        |       |       | Support discontinued in 2.16.1 and 3.0.0         |
| 5.6.x                 | 2.16    | 3.0.0  | 3.1.0 |       | Support discontinued in 2.16.18, 3.0.9 and 3.1.5 |
| 6.2.x                 | 2.16    | 3.0.0  | 3.1.0 |       | Support discontinued in 2.16.18, 3.0.9 and 3.1.5 |
| 6.3.x                 | 2.16    | 3.0.0  | 3.1.0 |       | Support discontinued in 2.16.18, 3.0.9 and 3.1.5 |
| 6.4.x                 | 2.16    | 3.0.0  | 3.1.0 |       | Support discontinued in 2.16.18, 3.0.9 and 3.1.5 |
| 6.5.x                 | 2.16.1  | 3.0.0  | 3.1.0 |       | Support discontinued in 2.16.19, 3.0.9 and 3.1.5 |
| 6.6.x                 | 2.16.5  | 3.0.0  | 3.1.0 | 3.2.0 |                                                  |
| 6.7.x                 | 2.16.8  | 3.0.0  | 3.1.0 | 3.2.0 |                                                  |
| 6.8.x                 | 2.16.11 | 3.0.2  | 3.1.0 | 3.2.0 |                                                  |
| 7.0.x                 | 2.16.8  | 3.0.0  | 3.1.0 | 3.2.0 | See note below about upgrades                    |
| 7.1.x                 | 2.16.9  | 3.0.1  | 3.1.0 | 3.2.0 |                                                  |
| 7.2.x                 | 2.16.10 | 3.0.2  | 3.1.0 | 3.2.0 |                                                  |
| 7.3.x                 | 2.16.11 | 3.0.2  | 3.1.0 | 3.2.0 |                                                  |
| 7.4.x                 | 2.16.13 | 3.0.3  | 3.1.0 | 3.2.0 |                                                  |
| 7.5.x                 | 2.16.14 | 3.0.5  | 3.1.1 | 3.2.0 |                                                  |
| 7.6.x                 | 2.16.17 | 3.0.8  | 3.1.4 | 3.2.0 |                                                  |
| 7.7.x                 | 2.16.19 | 3.0.9  | 3.1.5 | 3.2.0 |                                                  |
| 7.8.x                 |         | 3.0.12 | 3.1.7 | 3.2.3 |                                                  |

Indices created in Elasticsearch 5.x or earlier will need to be reindexed with
Elasticsearch 6.x in order to be readable by Elasticsearch 7.x. See
[breaking changes in Elasticsearch 7.0](https://www.elastic.co/guide/en/elasticsearch/reference/7.0/breaking-changes-7.0.html)
for details.
