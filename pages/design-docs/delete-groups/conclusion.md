---
title: "Design Doc - Deletion of groups - Conclusion"
permalink: design-docs/delete-groups-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

Deletion of groups is a generally desired feature we'd like to support in
Gerrit. However, there seem to be two major behaviors/modes depending on host
admin/owner preferences:
1) Remove a group without keeping a Git ref to it to reduce the number of Git
refs on the Gerrit server.
2) Remove a group but keep its complete audit and add an audit entry for the
group deletion.

In core Gerrit, we can't implement 1) without offering 2) by default as existing
host admins/owners might rely on core Gerrit's audit for groups to keep
track of all modifications. Enabling traceless group deletion without explicit
consent from these persons would likely result in negative surprises.

Implementing 2) is more effort, though, and even more so if want to offer 1)
and 2) both inside of core Gerrit. The proposer of the design wishes to support
just 1). Hence, we recommend to implement 1) in a plugin. Before that plugin
can become a core plugin in the future, it needs to also support 2).
