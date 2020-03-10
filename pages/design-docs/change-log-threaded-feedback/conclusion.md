---
title: "Design Doc - Change Log: Threaded Feedback - Conclusion"
permalink: design-docs/change-log-threaded-feedback-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

We're aware that it's currently difficult to follow discussions on change level
as the change messages shown in the `Change Log` don't have any explicit
relation to each other beyond the included quotes. In addition, such messages
can contain action items which can easily be missed. Hence, we welcome
improvements to this.

By suggesting to use comments for the human-written part of a change message,
the proposed solution nicely makes use of existing Gerrit concepts. Thus, it
can directly benefit from existing features such as threading for comments and
their unresolved state as well as an appropriate visualization in the
`Comment Threads` view. The future maintenance effort should also be lower due
to the reuse of existing code. Of course, some adjustments will be necessary
to allow to post comments without attaching them to a file but we don't expect
any major rework for this.

## <a id="implementation-remarks"> Implementation Remarks

We haven't agreed on the exact backend implementation or UI/UX for this effort
yet. We'll do so while iterating on the implementation of the solution. This
effort will only be considered done if the new kind of comments are properly
integrated in the UI of Gerrit, meaning that users can see and interact with
them on all relevant views.

## <a id="implementation-plan"> Implementation Plan

Jacek Centkowski will drive this implementation, mentored by Alice Kober-Sotzek.
The implementation is scheduled to start in the 13th week of 2020.
