Solution: Child Plugins

Extend the plugin infrastructure to support a way to package and subdivide a plugin internally
with child plugins with the following properties:

* A single plugin can have an internal division into a parent plugin, and zero or more child
plugins.

* A child plugin must have one and only one primary parent plugin.

* A child plugin must have at least one secondary parent plugin.

* A child plugin shares the packaging of their primary  parent (they live in the same jar as the
primary parent), and will be loaded and unloaded with their parent plugin.

* Child plugins must specify their secondary parents via jar properties (“pom” entries).

* A child plugin’s name consists of a first, a middle, and a last name. The first name is defined by
the developer, the middle name consists of the primary parent, and the last name consists of a list
of all its parents in order.

* Like a regular plugin, a child plugin may be defined as mandatory, by default it is non-mandatory.

* If a mandatory child plugin cannot be found, along with all its parents at Gerrit startup, then
Gerrit will fail to start.

* The lifecyle of a non-mandatory child plugin begins after all of its parents are loaded, and ends
before any of its parents are unloaded.

* A child plugin may have the same entry points that a plugin can have today: a SYS, an HTTP, and an
SSH module entry point.

* Child plugins have a multi-parent classloader that will use all their parents in order.

* Definitions of Dynamic<X>s in a parent plugin will be seen by all children of the parent plugin in
the same Module type, whether that parent is a primary or a secondary parent. Child plugins may bind
implementations to these Dynamic<X>s and they will be seen by the parent plugin. To avoid collisions
between multiple parent plugins defining Dynamic<X>s of a core type, either don’t allow, or ignore
definitions of these by plugins.

* Three new entry points of type API-SYS, API-HTTP, and API-SSH for parent plugins will be added to
live along with the existing SYS, HTTP, and SSH module entry points. Bindings in these modules will
be visible to all child plugins of this parent plugin in their respective SYS, HTTP, and SSH
contexts.
