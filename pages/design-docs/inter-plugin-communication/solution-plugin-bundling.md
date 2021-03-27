---
title: "Solution - Plugin Bundling - Inter Plugin Communication"
permalink: design-docs/inter-plugin-communication-solution-plugin-bundling.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - Plugin Bundling

## <a id="background"> Background

This solution's framework is designed to enable and help plugins achieve
these high level objectives:

1) Allow plugins to bundle related, dependent and independent, optional
and mandatory, services.

2) Allow plugins to share types, Guice bindings, and APIs with other
plugins in ways that provide type-saftey, limited scopes, and intra and
inter plugin chaining abilities between services.

3) Allow dependencies to be designated at the service level, which
allows service lifecycles to be maximized and only limited by the
availability of dependencies.

## <a id="overview"> Overview

This solution outlines a new plugin bundling framework and then outlines
how the use case can be achieved with this framework via examples.

The bundling framework specifies mechanisms to subdivide a plugin
easily, declare relationships between plugins, and to bundle subdivided
plugins in a way that can align with the inter and intra plugin sharing,
dependency, and lifecyle relationships outlined in the objectives above.

This subdivision creates three plugin types: main, public, and private
types. The main plugin is the standard plugin type that exists today,
and its name becomes the handle used to represent the bundle. This name
is used to load and unload the bundle.  Public plugins are primarily
meant to expose things to be shared across bundles, and private plugins
provide a place for intra plugin needs and are not intended to be
visible or shareable outside of the bundle (except for debugging
purposes). It is envisioned that services which need to be independent
would likely live in separate plugins, and if they are related they will
share a bundle.

A dependency mechanism is outlined that allows plugins (and thus
services) to declare the sharing which they need with other services
while avoiding unnecessary conflicts which can arrise from too much
sharing. This dependency mechanism also enables dynamic requirements
based lifecyle management by allowing a service to be made available as
soon as its dependencies are available, and to be disabled gracefully if
a dependency becomes unavailable, while still being ready to be
re-enabled as soon as the dependency is re-enabled. This dynamic service
enabling is made possible by the bundling of the services within the
same jar as the byte-code for the disabled services can still be
available when the service is disabled.

## <a id="detailed-design"> Detailed Design

### Splitting and bundling

Plugin splitting via public and private plugins allows different pieces
to be isolated from each other into different classloaders. This is
useful when there is a need to load conflicting classes, for example
when different versions of a third party library are needed. One way to
deal with this would be to create two completely separate plugins in
separate jars, however this may not be desirable if the functionality is
related and the developer would otherwise want them in the same plugin.
To achieve this split previously, administrators would have to manage
more plugins, more jar files, more potential version mismatches, and
they would have the need to understand dependencies that only developers
should have to care about.

The ability to split plugins internally not only helps reduce the
sharing scope of plugins, but it also provides the possibility of
dynamic requirements based (re/un)loading of independent services within
plugins.

Bundling allows multiple plugins to be (re/un)loaded together as a unit
via a single jar file. This will help avoid plugin proliferation so that
splitting will not be discouraged when it is useful. This is done by
allowing more than one Module MANIFEST entry of each type (Sys, Http,
Ssh) to be declared at build time like this:

  manifest_entries = [
    "Gerrit-PluginName: example-bundle",
    "Gerrit-Module: com.googlesource.gerrit.plugins.example.bundle.MainModule",
    "Gerrit-SshModule: com.googlesource.gerrit.plugins.example.bundle.MainSshModule",
    "Gerrit-Module: com.googlesource.gerrit.plugins.example.bundle.PublicModule",
    "Gerrit-SshModule: com.googlesource.gerrit.plugins.example.bundle.PrivateSshModule",
    ...
  ]

Only a single Module that is not public or private will be allowed, this
will be the main plugin.

### Plugin Module Annotations

The following annotations for plugin Modules will be introduced:

* @RequiresPlugin("plugin-name") Declares a load dependency on another plugin
* @PrivatePlugin("plugin-name")  Names and makes a plugin private
* @PublicPlugin("plugin-name")   Names and makes a plugin public
* @ParentPlugin("plugin-name")   Causes plugin to inherit classloaders and injectors from a plugin
* @DynamicPlugin                 Makes the lifecyle of the plugin dynamic

Using annotations to qualify plugins allows compile time verification of
plugin names. Compile time verification should make plugin development
easier as declaring names as MANIFEST entries for plugin Modules
correctly can be a tedious trial and error process with no feedback when
it is wrong.

### Dependencies

The @RequiresPlugin("plugin-name") annotation declares a load dependency
on another plugin, and can be used on any plugin type. Dependencies may
be linked to any main and public plugin, however only plugins from the
same bundle may depend on a private plugin. Cyclic dependencies are
allowed between dynamic plugins only.

Declaring inter plugin dependencies is useful to prevent plugins from
being loaded if their service depends on a service such as a REST API,
classes, or an API from another plugin.

Unlike the mandatory plugin mechanism, the dependency mechanism is meant
to not only by helpful at Gerrit startup time, but also later on, on the
fly, when using the APIs to (re/un)load plugins. This mechanism also has
the advantage that it allows plugin developers to be the ones declaring
inter plugin dependencies, whereas the mandatory mechanism requires
server administrators, who may lack this knowledge, to declare which
plugins are required.

### Private plugins

The @PrivatePlugin("plugin-name") annotation, associates the Module with
a private plugin by name. Private plugins will only be exposed for
debugging purposes. They will inherently depend on their main plugin,
and they may not be depended upon from other bundles!

Private plugins provide the scope limiting needed to help avoid
conflicts and to achieve the isolation that implementations may need or
desire when sharing. However private plugins are also intended to be
able to provide a common base layer mechanism to facilitate any intra
plugin sharing that is needed (for example for chaining) that does not
need to be explicitly exposed as being shared to other bundles.

### Public plugins

The @PublicPlugin("plugin-name") annotation, associates the Module with
a public plugin by name. Any plugin may depend on, or inherit from any
public plugin.

Public plugins are the heart of inter plugin communication.  They allow
a developer to explicity express that sharing with their pieces is
desirable. They enable sharing of classloaders, and sharing of Guice
injectors across plugin bundle boundaries.

### Parent Plugins

The @ParentPlugin("plugin-name") annotation causes the annotated Module
to inherit classloaders from the named plugin and its injector from the
Module of the same type (Sys, Http, or Ssh) of that same plugin. Plugins
may inherit from one or more of the plugins in the same bundle, and any
public plugin in any bundle. Since parent plugins must be loaded in
order for a plugin to share their classloader, declaring a parent plugin
relationship inherently also declares a dependency relationship between
plugins. Any plugin which defines a parent plugin is considered a child
of that parent plugin.

### Plugin classloader inheritance

Without inheritance, plugins only inherit their classloaders from core.
Classloader inheritance is designed to enable sharing of class types
internally and across bundles. Internal sharing makes it possible to
split plugins without having to duplicate classes which are needed in
more than one internal plugin.

The ability to share classloaders between plugins, when explicitly
requested, allows sharing APIs across plugin bundles in a limited way to
help reduce conflicts.

### Plugin injector inheritance

Without inheritance, plugins only see their own Guice bindings, those
from core, and those to Dynamic types from other plugins.

By inheriting a injector from parent plugins, it allows child plugins to
see all Guice bindings, including Dynamic definitions, from them so that
they may inject these types, and bind to and get from the Dynamic types.
This allows plugins to define APIs, similar to how core does, which they
expect other plugins to register and provide implementations for, and/or
to get implementations from. When used in combination with public
plugins, this enables producer and consumer relationships for non core
types to span plugin bundle boundaries.

By only exporting bindings to child plugins, it not only makes sharing
these bindings opt-in only, but it ensures that any non core types in
these bindings will be visible to all the plugins seeing the bindings
since as child plugins of the exporting plugin, they will also inherit
their classloader from the exporting plugin.

Although plugins can use bindings to export an API to other plugins,
this would require the implementation of that API to be implemented by
the plugin binding it, and this would expose the implementation to the
child plugins of the API defining plugin. To encourage the use of a
DynamicItem by plugins instead to export API services from a public
plugin which only a private plugin from the same bundle is meant to
implement, a restriction mechanism will be added to the DynamicItem
class so that when one is defined from a plugin, it can force its
provider to be implemented by a plugin from the current bundle. This is
needed to allow implementations to have dynamic dependencies (which may
never get loaded), while avoiding potential impersonation of the API
implementation by a plugin in another bundle.

### Dynamic Lifecycles

The @DynamicPlugin("plugin-name") annotation, makes the lifecyle of the
named plugin dynamic, and thus makes the plugin optional with respect to
plugins it depends on. This annoatition may be used on public or private
plugins only.

Bundling makes it possible to load a plugin on-demand at anytime after
the bundle has been loaded since all the classes in the bundle are
readily available if any plugin from the bundle is already loaded, and
dynamic plugins take advantage of this.

Dynamic lifecycles are requirements based and automatic. This means that
their (re/un)load behavior need not be explicitly invoked by an admin.
Instead, Gerrit will (re/un)load them whenever a (re/un)load invocation
of another plugin triggers their requirements to be met, or no longer
met. For the actions on other plugins required by dynamic plugins to
succeed without administrators having to manage the dynamic plugin also,
these plugins need to become optional, which means they will no longer
exhibit blocking behavior normally enforced by dependencies.

Dynamic lifecycles make it easy to design services to gracefully be
disabled when their dependencies are no longer met instead of failing.

## <a id="example"> Example

### Create the following plugins and relationships:

#### depends-on.jar bundle

depends-on       - exists today, already provides various services
                 - Has depends-on-resolver as its parent
                 - Additionally adds a --depends-on-resolve switch the query command
                   that will iterate over all the DeliverableResolutionCheckers in the
                   DynamicMap and call them all to resolve "depends-on" comments. If
                   the mandatory resolvers are there, then it may delete fully resolved
                   Change.Key dependencies.

depends-on-resolver (public)
                 - Defines the DeliverableResolutionChecker interface
                 - Registers a DynamicMap<DeliverableResolutionChecker>

#### pd-plugin.jar bundle

pd-plugin        - Exists today, already provides various services

pd-plugin--resolver (private)
                 - Has depends-on-resolver as its parent
                 - Has manifest-project-revisions-cache as its parent
                 - Registers a DeliverableResolutionChecker implementation

                   bind(java...depends.on.extension.DeliverableResolutionChecker).to(java...pd.depends.on.PdDeliverableResolutionCheckerImpl);

#### manifest.jar bundle

manifest         - Exists today, already provides various services
                 - Has manifest--types as its parent
                 - binds ProjectRevisionsCacheImpl to ProjectRevisionsCache

manifest-project-revisions-cache (public)
                 - Has manifest--types as its parent
                 - registers a ProjectRevisionsCache that can then be injected into other plugins

manifest--types (private)
                 - Defines types which are used in both the main and public plugins
                 - Defines ProjectRevisionsCache, ProjectRevision, and FileNameKey


### Use the following interface and class definitions:

#### depends-on.jar bundle

##### In the depends-on main plugin:

  package com...depends.on;

  public class Modules {
    public static final String NAME = "depends-on";

    @ParentPlugin(com...depends.on.public.resolver.Modules.NAME)
    public static class Sys extends AbstractModule {
      bind(ChangePluginDefinedInfoFactory.class)
          .annotatedWith(Exports.named(NAME))
          .to(AttributeFactory.class);
    }

    @ParentPlugin(com...depends.on.public.resolver.Modules.NAME)
    public static class Ssh extends SshModule {
      bind(DynamicBean.class).annotatedWith(Exports.named(Query.class)).to(QueryOptions.class);
    }

    public static class QueryOptions implements DynamicBean {
      @Option(
          name = "--resolve-depends-on",
          usage =
              "Resolve dependencies for the change and post resolutions as"
                  + " a new comment on the change")
      public boolean resolveDependsOn = false;
    }
  }

  public class AttributeFactory implements ChangePluginDefinedInfoFactory {
    @Inject DynamicMap<DeliverableResolutionChecker> map;

    @Override
    public Map<Change.Id, PluginDefinedInfo> createPluginDefinedInfos(
      Collection<ChangeData> cds, ChangeQueryProcessor qp, String plugin) {
      QueryOption options = (Modules.QueryOptions) qp.getDynamicBean(plugin);
      if (options.resolveDependsOn) {
        ... // Lookup comments on changes, parse them and determine dependent` and
            // `dependencies` as used below for the change
        for (DeliverableResolutionChecker checker : map.iterator()) {
           DeliverableResolutionChecker.Result r = checker.confirmResolutions(dependent, dependencies);
          ...
        }
      }
    }
  }

##### In the depends-on-resolver public plugin:

  package com...depends.on.public.resolver;

  public class Modules {
    public static final String NAME = com...depends.on.Modules.NAME + "-" + POSTFIX;
    public static final String POSTFIX = "resolver";

    @PublicPlugin(POSTFIX)
    public static class Sys extends AbstractModule {
      @Override
      public void configure() {
        DynamicMap.of(DeliverableResolutionChecker.class);
      }
    }
  }

  public interface DeliverableResolutionChecker {
    public interface class Result {
       boolean isFullyResolved();
       Set<BranchNameKey> getResolvedBranches();
    }

    /**
     * dependent - is the branch of the dependent change from which the applicable deliverables
     *             can be looked up.
     *
     * dependcies - are the branches of the currently resolved dependency changes from which the
     *              applicable deliverables can be looked up. This only includes the branches
     *              which have a change on them for every Change.Key in the depends-on list.
     **/
    Result confirmResolutions(BranchNameKey dependent, Set<BranchNameKey> dependencies);
  }


#### pd-plugin.jar bundle

##### In the pd-plugin--resolver private plugin:

  package com...pd.private.resolver;

  public class Modules {
    public static final String NAME = com...pd.Modules.NAME + "-" + POSTFIX;
    public static final String POSTFIX = "resolver";

    @DynamicPlugin
    @ParentPlugin(com...pd.Modules.NAME) // Needed for getAllPdManifests() DB Lookup
    @ParentPlugin(com...manifest.public.project.revisions.cache.Modules.NAME)
    @ParentPlugin(com...depends.on.public.resolver.Modules.NAME)
    @PrivatePlugin(POSTFIX)
    public static class Sys extends AbstractModule {
      @Override
      public void configure() {
        bind(DeliverableResolutionChecker.class).to(PdDeliverableResolutionCheckerImpl.class);
      }
    }
  }

  public class PdDeliverableResolutionCheckerImpl implements DeliverableResolutionChecker {
    static class ResultImpl implements Result { ... }

    @Inject DynamicItem<ProjectRevisionsCache> prCache; // provided by manifest plugin

    Result confirmResolutions(BranchNameKey dependent, Set<BranchNameKey> dependencies) {
      Result result = new ResultImpl(dependencies);
      for (FileNameKey manifest : getDeliverableManifests(dependent)) {
        ProjectNameKey project = dependent.getParentKey();
        SetMultimap<String, ProjectRevision> prByProject =
          prCache.get().getProjectRevisionsByProject(manifest);
        for (BranchNameKey> dependency : dependencies) {
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

    private Iterable<FileNameKey> getDeliverableManifests(BranchNameKey dependent) {
      List<FileNameKey> manifests = new ArrayList<>();
      for (FileNameKey manifest : getAllPdManifests()) { // Custom Pd DB Lookup
        ProjectNameKey project = dependent.getParentKey();
        for (ProjectRevision pr : prCache.get().getProjectRevisionsByProject(manifest).get(project)) {
          if (pr.isUpload(dependent)) { // May need to do a git repo lookup
            manifests.add(manifest);
          }
        }
      }
      return manifests;
    }
  }


#### manifest.jar bundle

##### In the manifest main plugin:

  package com...manifest;

  public class Modules {
    public static final String NAME = "manifest";

    @ParentPlugin(com...manifest.private.types.Modules.NAME)
    public static class Sys extends AbstractModule {
      @Override
      public void configure() {
        // bind to a restricted DynamicItem which may only be implemented in the manifest bundle
        bind(ProjectRevisionsCache.class).to(ProjectRevisionsCacheImpl.class);
      }
    }
  }

##### In the manifest-project-revisions-cache public plugin:

  package com...manifest.public.project.revisions.cache;

  public class Modules {
    public static final String NAME = com...manifest.Modules.NAME + "-" + POSTFIX;
    public static final String POSTFIX = "project-revisions-cache";

    @ParentPlugin(com...manifest.private.types.Modules.NAME)
    @PublicPlugin(POSTFIX)
    public static class Sys extends AbstractModule {
      @Override
      public void configure() {
        DynamicItem.restrictedItemOf(ProjectRevisionsCache.class);
      }
    }
  }

##### In the manifest--types private plugin:

  package com...manifest.private.types;

  public class Modules {
    public static final String NAME = com...manifest.Modules.NAME + "--" + POSTFIX;
    public static final String POSTFIX = "types";

    @PublicPlugin(POSTFIX)
    public static class Sys extends AbstractModule {
      @Override public void configure() {}; // Just here to define its name
    }
  }

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
     * Returns whether BranchNameKey matches any uploadable branch (a mutable branch that 'repo
     * upload' would try to upload to).
     *
     * @param branch
     * @return true if BranchNameKey matches the uploadable destBranch, revision, or upstream.
     */
    public boolean isUpload(BranchNameKey branch) throws IOException {
      ... // Potentially accesses git repos to look for sha1s
    }
    ...
  }

## <a id="pros-and-cons"> Pros and Cons
## <a id="alternatives-considered"> Alternatives Considered
## <a id="implementation-plan"> Implementation Plan

### Add a @RequiresPlugin() annotation for plugin Modules

Prevent a plugin from being loaded unless all of its dependencies are
already loaded. Prevent a plugin from being unloaded if any other loaded
plugins depends on it. Support uninterrupted service reloads when
reloading a plugin by first loading the new plugin followed by all of
its dependencies (as declared by the new plugin), and then unloading all
the old plugin's dependencies followed by unloading the original plugin.

### Provide isolation via bundled private plugins

Introduce a bundling mechanism that allows multiple plugins to be
(re/un)loaded together as a unit via a single jar file. Introduce
private plugins to make use of this bundling feature.

### Add a @ParentPlugin annotation for plugin Modules

Enabling plugins to use one or more of the plugins in the same bundle as
a parent to their classloader.

### Add a @PublicPlugin annotation for plugin Modules

Introducing public plugins. Enable any plugin in any bundle to specifcy
any public plugin, even in another plugin bundle, as a dependency or as
a parent.

### Make child plugins inherit Guice injectors

Make child plugin Modules inherit injectors from their corresponding
Module type in their parent plugins.

### Add a @DynamicPlugin annotation for plugin Modules

Do not prevent the loading of a plugin bundle if the dependencies of a
dynamic plugin in the bundle are not met, instead automatically load a
dynamic plugin after its last dependency is met. Do not block unloading
of a plugin if a dynamic plugin depends on it, instead first unload the
dynamic plugin.

### Enable plugin defined DynamicItem provider restricting

When a DynamicItem is defined from a plugin, allow it to force its
provider to be implemented by a plugin from the current bundle.

## <a id="time-estimation"> Time Estimation

