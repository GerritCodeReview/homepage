---
title: ""
permalink: design-docs/inter-plugin-communication-solution.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Proposed solution

By implementing the `com.google.gerrit.extensions.registration.PluginProvidedApi` interface,
a plugin can provide an API which can be consumed by another plugin. The API thus provided
will only be accessible to other plugins and will not be exposed to Gerrit users directly.
To provide an API for other plugins, bind a PluginProvidedApi interface. For example:

[source,java]
----
// Suppose the below binding is provided by a plugin named 'my-api-plugin'.
bind(com.google.gerrit.extensions.registration.PluginProvidedApi.class)
    .annotatedWith(Exports.named("MyApi"))
    .to(MyApi.class);

public class MyApi implements PluginProvidedApi {
  public BranchNameKey getBranch(Project.NameKey project) {
     [...]
     return branch;
  }

  public void startMyCommand(Set<Project.NameKey> projects) {
     [...]
  }
}
----

To consume the API provided by a plugin from another plugin, inject the PluginProvidedApi
DynamicMap and fetch the respective API by name. The required API must be available/registered
when trying to request the API from PluginProvidedApi DynamicMap. The registered API is
implemented by a class that is loaded in the implementing plugin's classloader which is
different from the classloader of the consuming plugin. This means the consuming plugin cannot
access the MyAPI class at compile-time since there will be a class miss-match when the same
compile-time class is accessed via two different classloaders, i.e., if an attempt is made
to assign the implementation from the providing plugin's classloader to a class variable,
argument, or return value loaded by the consuming plugin's classloader. Due to this reason,
reflection is used to invoke the required method. For example:

[source,java]
----
public class MyClass {
  protected DynamicMap<PluginProvidedApi> pluginProvidedApis;

  @Inject
  public MyClass(DynamicMap<PluginProvidedApi> pluginProvidedApis) {
    this.pluginProvidedApis = pluginProvidedApis;
  }

  public Optional<BranchNameKey> getBranch(Project.NameKey project) {
    // Casting to original compile time class like below will fail:
    // MyApi api = (MyApi) pluginProvidedApis.get("my-api-plugin", "MyApi");
    PluginProvidedApi pluginProvidedApi = pluginProvidedApis.get("my-api-plugin", "MyApi");
    if (pluginProvidedApi == null) {
      return Optional.empty();
    }
    return getBranchFromApi(pluginProvidedApi, project);
  }

  protected Optional<BranchNameKey> getBranchFromApi(PluginProvidedApi pluginProvidedApi,
      Project.NameKey project) {
    try {
      return Optional.of(
          (BranchNameKey)
              pluginProvidedApi
                  .getClass()
                  .getMethod("getBranch")
                  .invoke(pluginProvidedApi, project));
    } catch (ClassCastException | IllegalAccessException | InvocationTargetException
        | NoSuchMethodException e) {
      return Optional.empty();
    }
  }
}



* Should plugins be testable?

    As we can’t resolve APIs in compile time, we can only write integration tests to test the
    end-to-end functionality in which the API is used and make sure that the functionality works
    as expected.

* What happens to a caller if a dependency provider is unloaded?

    The DynamicMap will null (I.e., when called pluginProvidedApis.get("my-api-plugin", "MyApi")),
    the consumer plugin must gracefully handle these scenarios.

* Does verification (eg. type checking) happen compile time or runtime?

    Runtime.

* Which parts of a plugin are available to callers?

    Only the API which will be exposed by the providing plugin through binding as below,

    bind(com.google.gerrit.extensions.registration.PluginProvidedApi.class)
        .annotatedWith(Exports.named("MyApi"))
        .to(MyApi.class);
