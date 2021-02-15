---
title: ""
permalink: design-docs/inter-plugin-communication-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---
# Problem Statement

We want to leverage information from a proprietary data source to look in
manifest XML files for projects and branches so that we can accurately determine
which changes non-git ("Depends-on") dependencies for a change resolve to.

# Background

At Qualcomm we track non-git dependencies using change comments prefixed with
"Depends-on:" and a list of changes. We have a plugin (called "depends-on") that
can read these comments during change queries and output a list of changes for
CI systems and other users to consume. CI systems want to ensure they include
all of a change's dependencies when validating the change.

When propagating changes across branches, we do not want to lose dependency
information. To ensure it is retained with the change, the depends-on plugin
listens for cherry-pick events and copies the change comment from the source to
the destination change. Because the comments can refer to a specific change
number and that change number is unlikely to satisfy the dependency on the
destination branch (due to which branches are included in manifests, etc), the
depends-on plugin converts the change numbers into Change-Ids (`Iabc...`). When
a change with a Change-Id dependency is returned in query results, CI systems
consider the change to have unresolved dependencies; i.e. a dependency on a
logical change that has yet to be propagated to the appropriate destination(s).

To unblock those changes with unresolved dependencies, we want to find the
equivalent propagated change for each logical change. When each change is found,
we want the "Depends-on:" comment updated with the change number (potentially
replacing the Change-Id). We only want to remove the Change-Id once a change has
been found for each appropriate destination, thus unblocking the propagated
change and its propagated dependencies for CI.

Since non-git dependencies are not restricted to changes on the same branch or
project, they only make sense in the context of some grouping at a higher level
than a single git repo. A repo manifest file or git submodule superproject are
examples of ways to define a set of projects and branches that go together. That
set definition can be considered a deliverable. When considering the concept of
an appropriate destination, we think about sets of deliverables.

Today this functionality described in the last two paragraphs above is provided
by code hardcoded into our fork that tightly couples to a proprietary system.

# Use-case
We want to port/move the code from our Gerrit core fork to plugins and use a
plugin design that has clean layering.

## What are the responsibilities of each plugin?

The overarching goal is to provide as open source as much functionality as
possible (separated into different plugins by logical boundaries). We've
identified 3 specific functional areas for plugins:

* depends-on plugin:<br>
    Has the ability to read & parse a change comment and output it to users as
    dependency information. Has the ability to write change comments with
    dependency information. Listens for cherry-pick events and propagates
    dependency information from source to destination changes.

    Includes the ability to resolve (by reading/parsing and adding change
    comments) logical change dependencies into concrete change dependencies
    based on sets of deliverables.

* "proprietary deliverables" ("PDs") plugin:<br>
    Should be the only plugin that knows what the sets of deliverables are based
    on proprietary data sources.

    Deliverables are both pointers to manifest files and other project/branch
    sets defined in proprietary systems.

* manifest plugin:<br>
    Reads/writes git-repo style manifest XML files.

    Can convert a manifest reference (specified as project+branch+file) into the
    specific Gerrit projects and branches listed as projects in that manifest.

## How do the plugins work when others are not present?

All plugins continue providing functionality when others are not there.
Specifically:

* depends-on plugin:<br>
    Without either the manifest or PDs plugins, depends-on continues to parse
    comments and can output dependency info as query attributes; continues to
    copy dependencies (add comments) on propagated changes.

    Refuses to remove logical dependencies when resolving propagated
    dependencies when given an incomplete deliverables set (i.e. if the PDs
    plugin isn't present to provide the full deliverables set).

* PDs plugin:<br>
    Continues to output query attributes, provide search operators, etc if the
    depends-on plugin isn't available. A subset of those attributes and
    operators are available if the manifest plugin isn't available.

* manifest plugin:<br>
    Continues to provide search operators when depends-on and/or PDs plugins
    aren't available.

## How does it work when one of the plugins providing functionality changes its API, and is reloaded?

A well developed plugin would treat a situation where the API it needs is no
longer compatible the same way it would if the other plugin wasn't loaded. It
should have the same behavior as if the consuming plugin got a 404 from a REST
API call to another plugin.

# Acceptance Criteria

* Can share generic plugins (manifest and depends-on) with the community without
  sharing confidential business logic (PDs plugin).

* Works with vanilla Gerrit

* If we fix a bug in one plugin, we need to only deploy a new version of that
  plugin (unless the fix requires an interface change). This also means in the
  case of a bug, we would not need to rebuild the non-buggy plugins (they are
  potentially plugins we never build but only consume from gerritforge ci, etc).

* Load order between plugins does not matter.
    * Reloading any plugin in the stack (say for a bug fix) should continue to
      work. All new operations after the reload, even from other plugins, will
      exercise the newly reloaded plugin code (with the bug fix).

* Keeping a gerrit server process running 24x7 is not a primary objective, but
  would be nice to have.

* Provides ways for a Gerrit admin to detect that the system isn't fully working.

* No need for admins or plugin devs to perform any steps beyond [regular plugin
  development](#regular-plugin-development).

## Nice to haves
* Leverage a cache from another plugin
    * manifest plugin caches manifest file content and the PDs plugin can expose
      search attributes that leverage it

    * PDs plugin caches pointers to manifests and other deliverables used during
      resolving Depends-on dependencies

    * manifest plugin caches manifest file content, provides switches to the
      'propagator' plugin (which is a layer on top of cherry-pick), and those
      switches are called from a propagator command using the manifest caches

## Regular Plugin Development
This mostly means doing things that are outlined in the [plugin dev
doc](https://gerrit-review.googlesource.com/Documentation/dev-plugins.html).

Specific to inter-plugin APIs, regular plugin development includes a plugin
having access to a subset of another plugin's signatures during
development/compilation.

For Java, that's commonly accomplished by having access to: 1) at least a subset
of the source or 2) a subset of the classfiles (probably in a jar). This is
similar to the plugin having access to these same things from Gerrit itself.
Just as Gerrit's build produces a WAR today and plugin devs can develop against
the `gerrit-*-api.jar`(s), it would be reasonable for plugins to produce JARs
for install and potentially a subset jar for other plugins to develop against.

* Does it mean that my IDE can resolve all classes needed?<br>
    Yes. Your IDE would have access to the other plugin's signatures.
* Does hot plugin swapping without a restart work?<br>
    Yes.
