---
title: "Solution - Sub Plugins - Inter Plugin Communication"
permalink: design-docs/inter-plugin-communication-solution-sub-plugins.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Sub Plugins

## <a id="background"> Background

This solution's framework is designed to enable and help plugins achieve
these high level objectives:

1) Allow plugins to bundle related, dependent and independent, optional
and mandatory, services.

2) Allow plugins to share types, Insertions Points, and APIs with other
plugins in ways that provide type-saftey, limited scopes, and intra and
inter plugin chaining abilities between services.

3) Allow dependencies to be designated at the service level, which
allows service lifecylces to be maximized and only limited by the
availability of dependencies.

## <a id="overview"> Overview

This solution outlines a new sub-plugin framework and then outlines how
the use case can be achieved with this framework via examples.

This framework specifices a mechanism to subdivide plugins and package
the subdivisions in a way that can align with the inter and intra plugin
sharing, dependency, and lifecyle relationships outlined in objectives
1-3 above.

The new subdivision provides most of objectives #1-2 by defining 3
different sub-plugin types: main, public, and private types.  The main
sub-plugin is the standard plugin type that exists today, it becomes the
handle for all the sub-plugins in a package, it owns the name of the
plugin, and it is used to load and unload all the sub-plugins in the top
level plugin package. Public sub-plugins are primarily meant to expose
things to be shared, with the intent of fullfilling objective #.2.
Private plugins provide the scope limiting needed to help avoid
conflicts and achieve the isolation that implementations may need or
desire when sharing.  However private plugins are also intended to be
able to provide a common base layer mechanism to facilitate any intra
plugin sharing that is needed (for example for chaining) and that is
irrelevant, and does not need to be explicitly exposed as being shared
to other top level plugins.

It is envisioned that services which need to be independent would likely
live in separate sub-plugins. A dependency mechanism is outlined that
allows sub-plugins (and thus services) to define the sharing which they
need with other services while avoiding unnecessary conflicts which can
arrise from too much sharing. This dependency mechanism also enables
requiremensts based lifecyle management to help achieve objective #3, by
allowing a service to be made available as soon as its dependencies are
available, and to be disabled gracefully if a dependency is unavailable,
while still being ready to be re-enabled as soon as the dependency is
re-enabled. This dynamic service enabling is made possible by the
bundling of the services within the same plugin as the byte-code for the
disabled services can still be available when the service is disabled.

## <a id="detailed-design"> Detailed Design

### (Sub-)Plugins (Applies to all plugin types, sub-plugins and top level plugins)

* Are defined via tags in their jar (similarly to how the SYS, HTTP, and
SSH entry points are defined).

* May only be loaded after all of their dependencies are loaded.

* Must be unloaded before any of their dependencies are unloaded.

* Their lifecycle begins ("start" is called) after all of their
dependencies are loaded.

* Their lifecycle ends ("stop" is called) before any of their
dependencies are unloaded.

* Can be reloaded without interrupting their service.

* Can have their dependencies reloaded without interrupting their
service.

### Sub-Plugins

* Are packaged together in the jar of their main sub-plugin.

* Are defined via tags in their jar (similarly to how the SYS, HTTP, and
SSH entry points are defined).

* Have a name that make it possile to dinstinguish their type.

* Are all unloaded when the main sub-plugin is unloaded.

### (Sub-)Plugin Dependencies

* (Sub-)Plugins may define dependencies to other plugins via tags in
their jar.

* (Sub-)Plugins may depend on any main or public plugin in any top legel
plugin.

* (Sub-)Plugins may depend on any private plugin in the same top level
plugin.

### Plugin Parents

* All three sub-plugin types may have zero or more (sub-) plugins as
parents.

* Plugin parents are defined by defining a dependency, and any
dependency which is allowed to be a parent to the dependet plugin will
be denoted as one. This is avoids having to define parents as
dependencies also.

* Sub-plugins have their own classloaders which inherit from all of
their parents' classloaders.

* Public parents of a sub-plugin may be from any top level plugin.

* Private parents of a sub-plugin must be from the same top level
plugin.

### Main Plugins

* Share the name of their top level plugin.

* May not be a parent or an ancestor to public plugins. This avoids
exposing main plugins' internals. If a main plugin needs to share with a
public plugin, it can do so by making the public plugin a parent, or by
sharing a public or private plugin as an ancestor with the public
plugin.

### Public Plugins

* May not have a main plugin as a parent or as an ancestor.

* Injection Points definded in public plugins may have implementations
bound to them from any child plugin of the public plugin in any top
level plugin.

* Bindings of types in public plugins may only have implementations
bound to them from child plugins in the same top-level plugin. This
prevents other top-level plugins from overriding the intended
implementation of an API.

* Public plugins must be loaded once all of their dependencies are
loaded.

### Private Plugins

* Private plugins must be loaded once all of their dependencies are
loaded.

## <a id="examples"> Examples

### Create the following sub-plugins and relationships:

depends-on(main) - exists today, already provides various services
                 - Has depends-on-resolver as its parent
                 - Additionally adds a --depends-on-resolve switch the query command
                   that will iterate over all the DeliverableResolutionCheckers in the
                   DynamicMap and call them all to resolve "depends-on" comments. If
                   the mandatory resolvers are there, then it may delete fully resolved
                   Change.Key dependencies.

depends-on(public)-resolver
                 - Defines the DeliverableResolutionChecker interface
                 - Registers a DynamicMap<DeliverableResolutionChecker>

pd-plugin(main)  - Exists today, already provides various services

pd-plugin(private)-depends-on-resolver
                 - Has depends-on-resolver as its parent
                 - Has manifest-project-revisions-cache as its parent
                 - Registers a DeliverableResolutionChecker implementation

                   bind(java...depends.on.extension.DeliverableResolutionChecker).to(java…pd.depends.on.PdDeliverableResolutionCheckerImpl);

manifest(main)   - Exists today, already provides various services
                 - Has manifest(private)-types as its parent
                 - needs to move all code implementing ProjectRevisionsCacheImpl to
                   manifest(private)-project-revisions-cacheimpl so it becomes a child
                   of manifest(public)-project-revisions-cache

manifest(public)-project-revisions-cache
                 - Has manifest(private)-types as its parent
                 - registers a ProjectRevisionsCache that can then be injected into other plugins

manifest(private)-project-revisions-cacheimpl
                 - Has manifest-project-revisions-cache as its parent
                 - binds ProjectRevisionsCacheImpl to ProjectRevisionsCache

manifest(private)-types
                 - Defines types which are used in both the main and public sub-plugins
                 - Defines ProjectRevisionsCache, ProjectRevision, and FileNameKey


### Use the following interfaces and classes definitions:

#### In the depends-on-resolver sub-plugin:

public interface DeliverableResolutionChecker {
  public interface class Result {
     boolean isFullyResolved();
     Set<Branch.NameKey> getResolvedBranches();
  }

  /**
   * dependent - is the branch of the dependent change from which the applicable deliverables
   *             can be looked up.
   *
   * dependcies - are the branches of the currently resolved dependency changes from which the
   *              applicable deliverables can be looked up. This only includes the branches
   *              which have a change on them for every Change.Key in the depends-on list.
   **/
  Result confirmResolutions(Branch.NameKey dependent, Set<Branch.NameKey> dependencies);
}

#### In the pd-plugin(private)-depends-on-resolver sub-plugin:

public class PdDeliverableResolutionCheckerImpl implements  DeliverableResolutionChecker {
  static class ResultImpl implements Result { ... }

  @Inject ProjectRevisionsCache prCache; // provided by manifest-project-revisions-cache sub-plugin

  Result confirmResolutions(Branch.NameKey dependent, Set<Branch.NameKey> dependencies) {
    Result result = new ResultImpl(dependencies);
    for (FileNameKey manifest : getDeliverableManifests(dependent)) {
      Project.NameKey project = dependent.getParentKey();
      SetMultimap<String, ProjectRevision> prByProject =
          prCache.getProjectRevisionsByProject(manifest);
      for (Branch.NameKey> dependency : dependencies) {
        boolean resolveDeliverable = false;
        for (ProjectRevision pr : prByProject.get(dependent.getParentKey())) {
          if (pr.isUpload(dependent)) { // May need to do a git repo lookup
            result.setResolved(dependency);
            resolveDeliverable = true;
          }
        }
        if (!resolveDeliverable) {
          result.setFullyResolved(false);
        }
      }
    }
    return result;
  }

  private Iterable<FileNameKey> getDeliverableManifests(Branch.NameKey dependent) {
    List<FileNameKey> manifests = new ArrayList<>();
    for (FileNameKey manifest : getAllPdManifests()) { // Custom Pd DB Lookup
      Project.NameKey project = dependent.getParentKey();
      for (ProjectRevision pr : prCache.getProjectRevisionsByProject(manifest).get(project)) {
        if (pr.isUpload(dependent)) { // May need to do a git repo lookup
          manifests.add(manifest);
        }
      }
    }
    return manifests;
  }
}

#### In the manifest-types sub-plugin:

/* This is a real existing interface */
public interface ProjectRevisionsCache {
  ...
  SetMultimap<String, ProjectRevision> getProjectRevisionsByProject(FileNameKey manifestFile);
  ...
}

/* This is a real existing concrete class */
/**
 * Handle getting project revision information from a manifest.
 */
public class ProjectRevision {
  ...
  /**
   * Returns whether Branch.NameKey matches any uploadable branch (a mutable branch that 'repo
   * upload' would try to upload to).
   *
   * @param branch
   * @return true if Branch.NameKey matches the uploadable destBranch, revision, or upstream.
   */
  public boolean isUpload(Branch.NameKey branch) throws IOException {
    ... // Potentially accesses git repos to look for sha1s
  }
  ...
}

## <a id="pros-and-cons"> Pros and Cons
## <a id="alternatives-considered"> Alternatives Considered
## <a id="implementation-plan"> Implementation Plan
## <a id="time-estimation"> Time Estimation
