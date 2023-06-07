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

To save audit log within the core Gerrit implementation, one approach is
to save all audit records in a new branch called refs/meta/deleted-group or store
them in a data directory if necessary. The core Gerrit implementation
already has established structures and functions for manipulating group data, such
as rename and group creation, which makes it more readable and coherent to include
the delete group functionality within the core.
Implementing group deletion as a core feature also offers scalability benefits as
it requires less maintenance compared to an external plugin. By reusing existing
core functions and maintaining all group-related operations in one place, the
system becomes easier to manage in the long run.

Implementing 2) is more effort, though, and even more so if want to offer 1)
and 2) both inside of core Gerrit. The proposer of the design wishes to support
just 1). Hence, we recommend to implement 1) in core Gerrit.
