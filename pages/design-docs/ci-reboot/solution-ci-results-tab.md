---
title: "Design Doc - CI Reboot: CI Results Tab - Solution"
permalink: design-docs/ci-reboot-solution-ci-results-tab.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# Solution - CI Results Tab


## <a id="objective"> Objective

The [use cases doc](/design-docs/ci-reboot-use-cases.html) describes the
[the problems that we are trying to solve](/design-docs/ci-reboot-use-cases.html#ps-details) and
[the use cases that we are trying to address](/design-docs/ci-reboot-use-cases.html#uc-details)
with this solution.


## <a id="overview"> Overview

For the Change Page we will build a "Runs" tab next to the "Files" and "Comments" tabs for
displaying CI status and results.

The data for the Runs tab is exclusively provided by plugins. We will add a new frontend plugin
API for this purpose. Multiple plugins can contribute data at the same time. If no plugin
provides any data, then the tab is not shown.

The Gerrit backend will not be changed at all. Beyond label votes and robot comments CI results
are not stored in Gerrit, but loaded directly from other sources. That implies that such CI
results are not indexed and can only block submission indirectly via a label vote.

We will also add 1-3 lines of summary information below the commit message about the data on the
Runs tab.


## <a id="overview"> Wireframes

To get a better understanding of the proposed design we have drafted wireframes for the new tab
and the new summary. They are drafts and not finalized designs.

![CI Results Tab](/images/ci-reboot-ci-results-tab.png)

![CI Results Summary](/images/ci-reboot-ci-results-summary.png)


## <a id="api"> Plugin API

Plugins will be able to register themselves as CI data providers using the frontend plugin
API. When they have done that they will be notified during Change Page load about the change number
and the latest patchset number, and are requested to return an array of Runs, see
[data model](#data-model) section below.

The data provider will be polled for updates, if a polling interval was set during registration.
Updates can also be pushed.

The API will also include methods for managing the login workflow, if the data provider needs to
establish authentication and authorization. If APIs prove to be insufficient, then we will consider
other means such as iframes and external links. Note that it is also possible to avoid making
direct HTTP calls to other systems from the data provider plugin. Instead the data provider could
make calls to its backend plugin code and make calls to the CI system from the backend. Even
storing the CI data withing Gerrit by a plugin would be an option.  


## <a id="ext"> Extensibility

The goal of the "CI Results Tab" is to create a consistent user experience for a deeper integration
of CI systems into Gerrit's UI, but there is such a variety of CI systems being used by Gerrit
hosts that we cannot expect to meet all the special needs of each system with one unified UI. We
are therefore planning to add extension points to the tab and the summary such that individual
plugins can easily customize the UI with their own labels, buttons and widgets.

The CI Results Tab will be developed as a core feature and not as a plugin itself, because

* We would like to avoid plugins being dependent on plugins.
* We would like to avoid plugins offering plugin extension points for other plugins.
* We would like to use complex widgets and infrastructure of core that are not available to plugins.
* We believe that CI integration is a must-have feature for Gerrit hosts and we want to establish
  one consistent, smooth and well tested solution.


## <a id="data-model"> Data Model for Runs

The "Run" is the central entity that is passed in from data providers and shows up as rows in the
table on the proposed "Runs" tab. While this design doc intentionally glosses over some details, we
believe that it is vitally important to get an agreement on the data model for a Run, so this is
modeled here at a very detailed level, so that it is possible to check whether existing integrations
can be converted to the new model.

The UI will respect the order of the returned list of runs, so plugins can control which runs
appear first and thus make up for the absence of a priority field in the data model. If multiple
plugins provide data, then the results from earlier installed plugins are shown first. 

```
interface Run {
  change: number;
  // Typically only runs for the latest patchset are requested and presented. Older runs
  // are only available on request, e.g. by switching to another patchset in a dropdown.
  patchset: number;
  // The UI will focus on just the latest attempt per run. Former attempts are accessible,
  // but initially collapsed/hidden. Lower number means older run.
  attempt: number;

  // An optional opaque identifier not used by Gerrit directly, but might be used by plugin
  // extensions and callbacks.
  externalId?: string;

  // These categories are not chosen for being semantically cohesive, but for providing
  // one and only one top-level grouping mechanism. It allows the user to focus on exactly
  // the group of runs that are currently relevant to them.
  //
  // (3 more "run" related categories)
  // RUNNABLE:  Not run (yet). Mostly useful for runs that the user can trigger (see action).
  // RUNNING:   Subsumes "scheduled".
  // COMPLETED: If your run has completed without any interesting results (e.g. all tests passed),
  //            then this category is for you. It will be mostly hidden (i.e. collapsed) from the
  //            user and can cotain hundreds of completed runs.
  //
  // (3 more "result" related categories)
  // INFO:    The user will typically not bother to look into this category, only for looking up
  //          something that they are searching for. Can be used for reporting secondary metrics
  //          and analysis, or a wider range of artifacts produced by the CI system.
  // WARNING: A warning is something that should be read before submitting the change. The user
  //          should not ignore it, but it is also not blocking submit. It has a similar level of
  //          importance as an unresolved comment.
  // ERROR:   An error indicates that the change must not or cannot be submitted without fixing the
  //          problem. Errors will be visualized very prominently to the user. 
  //
  // The ‘tags’ field below can be used for further categorization, e.g. for distinguishing
  // SCHEDULED vs RUNNING, or FAILED vs TIMED_OUT. 
  category: Category;

  // Description of the run that is not specific to this change or attempt.
  // The name must be unique. There can’t be two runs with the same change/ps/attempt/name
  // combination.
  // Multiple attempts of the same run must have the same name, if the UI should group
  // these attempts.
  //
  // It should be expected that this string might be cut off at ~30 chars in the UI. The
  // full name will then be shown in a tooltip.
  // This is a plain string without styling or formatting options.
  // May optionally include the name of a CI system or platform as a prefix.
  // The name of a WARNING or ERROR result might be finer grained than a RUNNING or
  // RUNNABLE name, e.g. a test suite could be reported as 1 RUNNING run, but then later
  // be broken down into multiple WARNINGs when the run is completed.
  //
  // Examples:
  // Presubmit: Python Linter
  // End to end tests on x86/linux platform
  name: string;

  // Short description of the run status or result.
  //
  // It should be expected that this string might be cut off at ~80 chars in the UI. The
  // full description will then be shown in a tooltip.
  // This is plain string without styling or formatting options.
  //
  // Examples:
  // MessageConverterTest failed with: 'kermit' expected, but got 'ernie'.
  // 40 tests running, 30 completed: 0 failing so far.
  // Binary size of javascript bundle has increased by 27%.
  summary: string;

  // Exhaustive optional message describing the run status or result.
  // Will be initially collapsed. Might potentially be very long, e.g. a log of MB size.
  // The UI is not limiting this. CI data providers are responsible for not killing the
  // browser. :-)
  // TBD: Decide on a technology for text formatting. Markdown flavor?
  message?: string;

  // Optional reference to a label that this run influences. Allows the user to understand
  // and navigate the relationship between CI results and submit requirements.
  label?: string;

  // Tags allow a CI System to further categorize a Run, e.g. making a list of runs
  // filterable by the end-user.
  // The name is free-form, but there will be a predefined set of colors to choose from.
  // There will also be a list of common names and recommended colors, such that the most
  // common tags are consistent across Gerrit hosts.
  //
  // Examples (please provide more, if you can think of any):
  // PASS, FAIL, SCHEDULED, OBSOLETE, SKIPPED, TIMED_OUT, INFRA_ERROR, FLAKY
  // WIN, MAC, LINUX
  // BUILD, TEST, LINT
  // INTEGRATION, E2E, SCREENSHOT
  tags: Tag[]; // name + tooltip + color

  // Links provide an opportunity for the end-user to easily access details and build
  // artifacts. Links are different from Actions in that clicking a link should not change
  // the state of a Run.
  // Links are displayed by an icon+tooltip only. They don’t have a name, making them
  // clearly distinguishable from tags and actions.
  // There will be a fixed set of icons to choose from.
  // TBD: It might be worthwhile adding these icons even in the summary such that the user
  // only needs one click to get to the details. Might warrant a 'showInSummary' field.
  //
  // Examples (please provide more, if you can think of any):
  // Link to test log.
  // Link to result artifacts such as images and screenshots.
  // Link to downloadable artifacts such as ZIP or APK files.
  links: Link[]; // url + tooltip + icon

  // Callbacks to the CI plugin. Must be implemented individually by each plugin.
  // Actions are rendered as buttons. If there are more than two actions per run, then
  // further actions are put into an overflow menu. Sort order is defined by the data
  // provider.
  // TBD: Define the details of how callbacks are called. Passing an ID to a predefined
  // API method? Or are actual javascript functions being passed and called?
  //
  // Examples (please provide more, if you can think of any):
  // Run, Re-run, Cancel, Acknowledge/Dismiss, Delete,
  // Report a bug, Report as not useful, Make blocking, Downgrade severity.
  actions: Action[]; // name + callbackId + tooltip

  scheduledTimestamp?: Date;
  startedTimestamp?: Date;
  finishedTimestamp?: Date;
}
```