# Solution - multi-site approach

## <a id="overview"> Overview


By adding global ref-db interface to Gerrit core we will enable Gerrit itself
and other plugins to access global ref-db provided by a plugin.
Default implementation should point to Noop.

## <a id="detailed-design"> Detailed Design

Firstly in Gerrit core we should implement global ref-db interface together 
with tests which cover all of the use cases.

Interface methods:

* `boolean isUpToDate(Project.NameKey project, Ref ref)` - Check in global ref-db 
if ref is up-to-date.

* `boolean compareAndPut(Project.NameKey project, Ref currRef, ObjectId newRefValue)` -
Compare a reference, and put if it is up-to-date with the current.

* `AutoCloseable lockRef(Project.NameKey project, String refName)` - Lock a reference.

* `boolean exists(Project.NameKey project, String refName)` - Verify if the DB contains 
a value for the specific project and ref name.

* `void remove(Project.NameKey project)` - Clean project path from global-ref db.

Once we have that, it is possible to create DynamicItem binding which points to Noop
implementation. The default Noop implementation accepts any refs without checking
for consistency. This is useful for setting up a test environment and allows to
be used independently from any additional plugins or the existence of a specific
Ref-DB installation.

The last step is to create reference implementation of a global ref-db as a plugin.
It is the responsibility of this plugin to store atomically key/pairs of refs in
order to allow detect out-of-sync refs across multi sites. This is achieved by storing
the most recent `sha` for each specific mutable refs, by the usage of some sort of atomic
Compare and Set operation.

According to the CAP theorem, which in a nutshell states that a distributed system can
only provide two of these three properties: Consistency, Availability and Partition tolerance:
the global ref-db helps achieving Consistency and Partition tolerance (thus sacrificing Availability).

When provided, the global ref-db plugin will override the DynamicItem binding exposed by the Gerrit
with a specific implementation, such as Zoekeeper, etcd, MySQL, Mongo, etc. 

## <a id="solution-to-questions"> Solution to questions

### <a id="scalability"> Scalability

Scalability depends on the global ref-db plugin implementation and it's underlying technology.

## <a id="alternatives-considered"> Alternatives Considered

## <a id="pros-and-cons"> Pros and Cons

Pros:

1. Already proven on production(multi-site plugin on gerrithub).

Cons:

## <a id="implementation-plan"> Implementation Plan

Multi-site implementation of the global ref-db can be used as a reference.

### Create a global ref-db interface in the Gerrit core

Design and implement global ref-db interface, make sure it covers all primary 
and secondary use cases.
Provide dummy implementation of the interface together with test class to document 
the basic usage of the api.

### Add DynamicItem binding 

Create binding for the global ref-db interface which points to the Noop implementation.
Noop implementation should simply accept any refs without checking for consistency.

### Create first global ref-db plugin

Extract Zookeeper implementation of the global ref-db out of the multi-site plugin to
a separate plugin.
Make sure that the new plugin is using global ref-db intefaces from the Gerrit core.

## <a id="time-estimation"> Time Estimation

