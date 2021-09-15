---
title: "Design Doc - Case Insensitive Username Matching - Conclusion"
permalink: design-docs/case-insensitive-username-matching-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

A [survey](https://docs.google.com/presentation/d/1b68PfdGP4YvlYhAVN4CNlfFT5zmbJEN4IiTVUijEvSo/edit#slide=id.p)
was conducted to determine whether the Gerrit community would have
concerns, if case insensitive username handling would be made mandatory. One
third of the respondents voted against the feature being mandatory, mostly
because the use case sensitive identity providers. Cutting off that many users
from updating is not desired. Thus, it was decided to make this feature optional.
However, for new sites this case insensitive username handling will be enabled
by default.

Online migration of external ID notes is a desired feature to allow zero-downtime
upgrades and will be implemented at a later point in time.
