---
title: ""
hide_sidebar: true
hide_navtoggle: true
toc: false
---
# Conclusion
The solution described in [Solution Configurable Indexing](solution-configurable-indexing.md.md)
was chosen for the following reasons:
1. 'mergeable' is a scaling bottleneck that can turn into a regression as
   instances grow.
2. It does work well for smaller instances and we want Gerrit to serve
   projects of every shape and color. Smaller instances can still benefit
   from the 'is:mergeable' operator.

## <a id="implementation-plan"> Implementation Plan
hiesel@ is driving the implementation. It will be ready by YE2019.
