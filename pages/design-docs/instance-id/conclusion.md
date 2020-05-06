---
title: ""
permalink: design-docs/instance-id-conclusion.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Conclusion

The [solution of introducing an instanceId configuration](/design-docs/instance-id-solution.html) 
was chosen for the following reasons:

1. It is a simple solution that allows to define an instance-id.
2. It does not impact any existing Gerrit functionality, as the instance-id would be null by default.
3. It also creates additional flexibility for multi-master use-cases to populate the instance-id as preferred.
4. It does not impact 3rd party integrations (e.g. CI) because the instance-id won't be present in the event if not defined.
5. If instance-id is defined but not used by other 3rd party, it can be simply ignored.

## <a id="implementation-plan"> Implementation Plan

Fabio Ponciroli <ponch78@gmail.com> is driving the implementation, and it should be ready for review in max 2 days.
