# Use-case

Primary use case:

Enable detection of out-of-sync refs across gerrit sites. Each change attempting 
to mutate a ref will be checked against the Ref-DB to guarantee that each node has 
an up-to-date view of the repository state.

Secondary use cases:

1. Global ref-db helps sharing the repositories refdb across all the nodes when
Gerrit masters or slaves shares repos over a shared storage (e.g. NFS).
2. It could be leveraged also to have concurrent writes on a multi-master
setup(the high-availability scenario) by enabling a shared locking
mechanism for refs across multiple nodes.


## <a id="acceptance-criteria"> Acceptance Criteria

Gerrit or other plugins can use global ref-db provided as a plugin.

## <a id="background"> Background

First implementation of the global ref-db was designed and implemented for the 
multi-site plugin. Original design document can be found [here](
https://gerrit.googlesource.com/plugins/multi-site/+/refs/heads/master/DESIGN.md).
