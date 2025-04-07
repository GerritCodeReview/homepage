---
title: "Design Doc - Support posting changes from Jujutsu - Conclusion"
permalink: design-docs/support-jujutsu-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

We agree that we want to support Jujutsu as a client for working with Gerrit as
outlined in the [solution doc](solution.html).

If Git decides to preseve the `change-id` header on rebase and cherry-pick (see
[here](solution.html#git-does-not-preserve-jj-change-ids)) we do not need to
implement any of the mitigations to reach
[compatibility](solution.html#compatibility) between Git users and Jujutsu
users.

If Git decides to not add any support for the `change-id` header (as it is now)
we still agree to the design. In this case we would implement some of the
discussed mitigations.
