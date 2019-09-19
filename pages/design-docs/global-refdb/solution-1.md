# Solution - multi-site approach

## <a id="overview"> Overview

By adding global ref-db interface to Gerrit core we will enable Gerrit
and other plugins to access global ref-db provided by a plugin.
Default implementation should point to Noop. Noop implementation will be
be linked to the global ref-db interface by DynamicItem in Gerrit sysModule.
Having Noop implementation allows Gerrit and other plugins to be installed independently
from any global ref-db plugin or the existence of a specific Ref-DB installation.

## <a id="detailed-design"> Detailed Design

Firstly in Gerrit core we should implement global ref-db interface together
with tests which can be used as a "validation suite" for documenting and
checking the expected behaviour.

Interface methods:

* `boolean isUpToDate(Project.NameKey project, Ref ref)` - Check if ref is the same as
the one in the global ref-db.

* `boolean compareAndPut(Project.NameKey project, Ref currRef, ObjectId newRefValue)` -
Compare a reference, and put if it is the same as the one in the global ref-db.
This is done as a single atomic operation.

* `AutoCloseable lockRef(Project.NameKey project, String refName, Long timeout) throws TimeoutException` -
Acquires the exclusive lock for a reference if it is not held by another client within
the given waiting time.
The TimeoutException is thrown when the time specified by `timeout` parameter has expired.

* `boolean exists(Project.NameKey project, String refName)` - Verify if the DB contains
a value for the specific project and ref name.

* `void remove(Project.NameKey project)` - Clean project path from the global ref-db.

* `void remove(Project.NameKey project, String refName)` - Clean ref path for a given
project from the global ref-db.

Once we have that, it is possible to create DynamicItem binding which points to Noop
implementation. The default Noop implementation accepts any refs without checking
for consistency. This is useful for setting up a test environment and allows to
be used independently from any additional plugins or the existence of a specific
Ref-DB installation.

The last step is to create reference implementation of a global ref-db as a plugin.
It is the responsibility of this plugin to store atomically key/pairs of refs in
order to allow detection of out-of-sync refs across multi sites. This is achieved by storing
the most recent `sha` for each specific mutable refs, by the usage of some sort of atomic
Compare and Set operation.

According to the CAP theorem, which in a nutshell states that a distributed system can
only provide two of these three properties: Consistency, Availability and Partition
tolerance: the global ref-db helps achieving Consistency and Partition tolerance
(thus sacrificing Availability).

When provided, the global ref-db plugin will override the DynamicItem binding exposed
by the Gerrit with a specific implementation, such as Zookeeper.

## <a id="solution-to-questions"> Solution to questions

### <a id="scalability"> Scalability

Scalability depends on the global ref-db plugin implementation and it's underlying
technology.

## <a id="alternatives-considered"> Alternatives Considered

1. Global ref-db can be moved to JGit, as its own Eclipse project and built as an
independent artifact, than can be consumed by plugins, that depend on this functionality.

JGit doesn't seems to be the right choice because current classes are not covering all required functionalities. DfsRefDatabase and DfsReftableDatabase doesn't have a method which allows to aquire lock on a single reference. It is implemented downstream in the execution of the ref-updates. Unfortunately none of the mentioned classes is an interface, DfsRefUpdate and DfsReftableDatabase are abstract classes and contain a lot of functionalities that are not suitable for the global ref-db use case, DfsRefUpdate is a **final** class so it cannot be extended.

To cover all functionalities, refactoring of the existing JGit code by extracting interfaces out of an abstract classes is required. Making all those incompatible changes to cover use case which is not required by JGit is going to be very difficult to justify. On the other hand we can create new interface in JGit project, but this approach has downsides as well. New interface is not going to be used by local RefDatabase or DfsRefDatabase only by Gerrit and it's plugins. With this approach Gerrit specific code is placed in JGit so has to follow JGit release cycle which I believe is completely different than the Gerrit one. This is a significant limitation in the ability to release fixes and new functionalities.

Similar issue was faced during the implementation of [PermissionAwareRefDatabase](https://gerrit-review.googlesource.com/c/gerrit/+/212874/28) as a result of that RefDatabase wrapper was implemented in Gerrit instead of JGit.

2. It can be extracted into its own library and then be consumed by plugins that need
this functionality.

We will have parts of Gerrit core (e.g. master and slave) that would depend on a plugin
library, which would make building Gerrit a bit more complex and, potentially, reviews
across Gerrit and global-refdb more difficult to follow.

3. Multi-site plugin can be linked as a 3rd party dependency by plugins that need
global-refdb functionality.

Multi-site plugin contains much more than just global ref-db interface, including full
multi-site functionality in a plugin which requires just global ref-db would bring
unnecessary complexity.

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Flexible solution which covers all the use cases.
2. Easy Gerrit build without plugin library dependency.
3. Easy solution for plugins without need to include unneeded dependency.

Cons:

## <a id="implementation-plan"> Implementation Plan

Multi-site implementation of the global ref-db can be used as a reference.

### Create a global ref-db interface in the Gerrit core

Design and implement global ref-db interface, make sure it covers all primary
and secondary use cases.
Provide dummy implementation of the interface together with test class to document
the basic usage of the api.
Initial implementation can be found in this [change](https://gerrit-review.googlesource.com/c/gerrit/+/237606/7)

### Add DynamicItem binding

Create binding for the global ref-db interface which points to the Noop implementation.
Noop implementation should simply accept any refs without checking for consistency.

## <a id="time-estimation"> Time Estimation

Interface definition (finishing [change](https://gerrit-review.googlesource.com/c/gerrit/+/237606/7)) - 5 man-days.
Adding Noop implementation and DynamicItem binding - 2 man-days.
