---
title: ""
permalink: design-docs/inter-plugin-communication-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## <a id="background"> Background

We want an approach to expose an API from one plugin such that, the same API is consumable
by another plugin (given that the API is not exposed to Gerrit users directly). One can
expose an API from a plugin by implementing the PluginProvidedApi interface. Also, bind
the implementation class to PluginProvidedApi interface to expose the API using an export
name for other plugins to look up.

Currently methods that plugins can use to communicate:
  * share a common interface loaded as libmodule.

Problems with Existing Approach:

1. We believe having to use libmodule to enable a communication between two plugins is not
a complete solution, as one must install an additional jar into the lib directory of the
gerrit site to make the communication possible. Whereas in the new approach, there is no
need for the user to perform any additional steps other than the providing plugin registering
the API and the consuming plugin consuming it.

2. To install a new jar into lib dir, the release and deployment process must be updated
which takes time and effort which can be completely avoided by PluginProvidedApi approach.

# Use-cases

## Use-case 1:

Consider the replication plugin exposing the"replication start" command as an API that another
plugin could use. This would allow another plugin to run replication start for a custom set
of projects only on server startup.

## Use-case 2:

Consider a plugin called as depends-on which exposes a functionality which resolves dependencies
given a change and a set of deliverables. Dependencies are maintained in latest comments of change
prefixed with "Depends-on:". Set<Branch.NameKey> is considered to be a deliverable. A dependency
is said to be resolved when it is destined for the same deliverable(s) as the dependant change(s).
This plugin is a generic plugin and is upstream-able. This functionality needs to be exposed as an
API to other plugins (not exposed to Gerrit users directly). This functionality can be used by an
organization specific plugin (not upstream-able) which knows how to operate on org specific
deliverables and invoke generic API exposed by depends-on plugin. The org specific plugin thus
exposes a concrete SSH command or HTTP API for the users of Gerrit.

sample API exposed from depends-on plugin:

public interface DependencyResolver {
  public boolean resolveDependencies(PatchSet.Id patchSetId, Set<Set<Branch.NameKey>> deliverables)
    throws InvalidChangeOperationException, OrmException, NoSuchChangeException;
}

## Use-case 3:

Si plugin needs to get sets of branches in a manifest from the manifest plugin to resolve
dependencies.

## Use-case 4:

The task plugin namesfactories need a way based on configuration (not compiled) to dynamically
get data from other plugins (SI, component, PW, and manifest plugins) to get a list of tasknames.
