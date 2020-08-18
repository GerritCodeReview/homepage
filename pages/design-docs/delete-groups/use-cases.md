---
title: ""
permalink: design-docs/delete-groups-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Use-cases

Allow complete deletion of groups.

## <a id="acceptance-criteria"> Acceptance Criteria

Groups can be deleted simply and without problems. Initially, deletion should
not have an audit trail and it should not be possible to undelete a group.
Audit trail will become an objective (outside of this design doc) once the
initial implementation is finished. In terms of the undelete operation it can
be achieved by group re-creation under the original name.

## <a id="background"> Background

Some hosts, especially those that are around for quite a long time, have many
groups that are no longer used at all. There is currently no way to completely
delete a group and that means that the host keeps an unnecessarily high number
of refs. Also, it is a nuisance for the user to see so many different groups,
when most of those are unused.
