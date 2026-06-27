---
title: ""
permalink: design-docs/ee8-ee10-flavoured-release-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

Some major Gerrit stakeholders are not in a position to migrate to EE10 any time
soon, while others are ready to adopt it now. The proposal is to release both
the EE8 and EE10 flavours from a single source tree during the transition, so
that neither group blocks the other. This is a design proposal; the
EE10 WAR is not yet shipped.

Once all Gerrit stakeholders have migrated to EE10, the EE8 flavour will be
discontinued, converging the project back to a single servlet flavour.
