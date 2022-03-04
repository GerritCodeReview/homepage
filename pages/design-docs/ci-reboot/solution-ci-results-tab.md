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

For the Change Page we will build a "Checks" tab next to the "Files" and "Comments" tabs for
displaying CI status and results.

The data for the Checks tab is exclusively provided by plugins. We will add a new frontend plugin
API for this purpose. Multiple plugins can contribute data at the same time. If no plugin
provides any data, then the tab is not shown.

The Gerrit backend will not be changed at all. Beyond label votes and robot comments CI results
are not stored in Gerrit, but loaded directly from other sources. That implies that such CI
results are not indexed and can only block submission indirectly via a label vote.

We will also add 1-3 lines of summary information below the commit message about the data on the
Checks tab.


## <a id="wireframes"> Wireframes

To get a better understanding of the proposed design we have drafted wireframes for the new tab
and the new summary. They are drafts and not finalized designs.

![CI Results Tab](/images/ci-reboot-ci-results-tab.png)

![CI Results Summary](/images/ci-reboot-ci-results-summary.png)


## <a id="api"> Plugin API

Plugins will be able to register themselves as CI data providers using the frontend plugin
API. When they have done that they will be notified during Change Page load about the change number
and the latest patchset number, and are requested to return an array of CheckRuns and CheckResults,
see [data model](#data-model) section below.

The data provider will be polled for updates, if a polling interval was set during registration.
Updates can also be pushed.

The API will also include methods for managing the login workflow, if the data provider needs to
establish authentication and authorization. If APIs prove to be insufficient, then we will consider
other means such as iframes and external links. Note that it is also possible to avoid making
direct HTTP calls to other systems from the data provider plugin. Instead the data provider could
make calls to its backend plugin code and make calls to the CI system from the backend. Even
storing the CI data within Gerrit by a plugin would be an option.


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


## <a id="data-model"> Data Model for Checks

"CheckRun" and "CheckResult" are the central entities that are passed in from data providers.
While this design doc intentionally glosses over some details,
we believe that it is vitally important to get an agreement on the data model for runs and results,
so this is modeled here at a very detailed level, so that it is possible to check whether existing
integrations can be converted to the new model.

The UI will respect the order of the returned lists of runs and results, so plugins can control
which Checks appear first and thus make up for the absence of a priority field in the data model.
If multiple plugins provide data, then the results from earlier installed plugins are shown first.

```
// A CheckRun models an entity that has start/end timestamps and can be in either of the states
// RUNNABLE, RUNNING, COMPLETED. By itself it cannot model an error, neither can it be failed or
// successful by itself. A run can be associated with 0 to n results (see below). So until runs
// are completed the runs are more interesting for the user: What is going on at the moment? When
// runs are completed the users' interest shifts to results: What do I have to fix?
// The only actions that can be associated with runs are RUN and CANCEL.
interface CheckRun {
  // Gerrit requests check runs and results from the plugin by change number and patchset number.
  // So these two properties can as well be left empty when returning results to the Gerrit UI
  // and are thus optional.
  change?: number;
  // Typically only runs for the latest patchset are requested and presented. Older runs and their
  // results are only available on request, e.g. by switching to another patchset in a dropdown.
  // TBD: CI data providers may decide that runs and results are applicable to a newer patchset,
  // even if they were produced for an older, e.g. because only the commit message was changed.
  // Maybe that warrants the additional of another optional field, e.g. `original_patchset`.
  patchset?: number;
  // The UI will focus on just the latest attempt per run. Former attempts are accessible,
  // but initially collapsed/hidden. Lower number means older attempt. Every run has its own attempt
  // numbering, so attempt 3 of run A is not directly related to attempt 3 of run B.
  // RUNNABLE runs must use `undefined` as attempt.
  // COMPLETED and RUNNING runs must use an attempt number >=0.
  // TBD: Optionally providing aggregate information about former attempts will probably be a
  // useful feature, but we are deferring the exact data modeling of that to later. 
  attempt?: number;

  // An optional opaque identifier not used by Gerrit directly, but might be used by plugin
  // extensions and callbacks.
  externalId?: string;

  // RUNNABLE:  Not run (yet). Mostly useful for runs that the user can trigger (see actions).
  // RUNNING:   Subsumes "scheduled".
  // COMPLETED: The attempt of the run has finished. Does not indicate at all whether the
  //            run was successful or not. Outcomes can and should be modeled using the
  //            CheckResult entity.
  status: Status;
  // Optional short description of the run status. This is a plain string without styling or
  // formatting options. It will only be shown as a tooltip or in a hovercard. Examples: "40 tests
  // running, 30 completed: 0 failing so far", "Scheduled 5 minutes ago, not running yet".
  statusDescription?: string;
  // Optional link to an external page with more detailed information about the run status.
  statusLink?: Url;

  // The following 3 properties are independent of this run *instance*. They just describe what
  // the run is about and will be identical for other attempts or patchsets or changes.
  //
  // The unique name of the run.
  // There can’t be two runs with the same change/patchset/attempt/name combination.
  // Multiple attempts of the same run must have the same name.
  // It should be expected that this string is cut off at ~30 chars in the UI. The
  // full name will then be shown in a tooltip.
  name: string;
  // Optional description of the run. Only shown as a tooltip or in a hovercard.
  description?: string;
  // Optional link to an external page with more detailed information about this run.
  link?: Url;

  // Callbacks to the CI plugin. Must be implemented individually by each plugin.
  // The most important actions (which get special UI treatment) are:
  // "Run" for RUNNABLE and COMPLETED runs.
  // "Cancel" for RUNNING runs.
  //
  // TBD: Define the details of how callbacks are called. Passing an ID to a predefined
  // API method? Or are actual javascript functions being passed and called?
  actions: Action[]; // name ("Run" or "Cancel") + callbackId

  scheduledTimestamp?: Date;
  startedTimestamp?: Date;
  finishedTimestamp?: Date;
}

interface CheckResult {
  // Reference to the run that this result belongs to. Each run can have 0-n results. Each result
  // must be associated with exactly 1 run.
  checkRunName: string;
  checkRunAttempt: number;

  // An optional opaque identifier not used by Gerrit directly, but might be used by plugin
  // extensions and callbacks.
  externalId?: string;

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
  // FAILED vs TIMED_OUT.
  category: Category;

  // Short description of the check result.
  //
  // It should be expected that this string might be cut off at ~80 chars in the UI. The
  // full description will then be shown in a tooltip.
  // This is a plain string without styling or formatting options.
  //
  // Examples:
  // MessageConverterTest failed with: 'kermit' expected, but got 'ernie'.
  // Binary size of javascript bundle has increased by 27%.
  summary: string;

  // Exhaustive optional message describing the check result.
  // Will be initially collapsed. Might potentially be very long, e.g. a log of MB size.
  // The UI is not limiting this. CI data providers are responsible for not killing the
  // browser. :-)
  // TBD: Decide on a technology for text formatting. Markdown or HTML?
  message?: string;

  // Optional reference to a Gerrit label (e.g. "Verified") that this result influences.
  // Allows the user to understand and navigate the relationship between CI results and
  // submit requirements, see also https://gerrit-review.googlesource.com/c/homepage/+/279176.
  label?: string;

  // Tags allow a CI System to further categorize a result, e.g. making a list of results
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
  // artifacts.
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
  // Actions are rendered as buttons. If there are more than two actions per result, then
  // further actions are put into an overflow menu. Sort order is defined by the data
  // provider.
  // TBD: Define the details of how callbacks are called. Passing an ID to a predefined
  // API method? Or are actual javascript functions being passed and called?
  //
  // Examples (please provide more, if you can think of any):
  // Acknowledge/Dismiss, Delete, Report a bug, Report as not useful, Make blocking,
  // Downgrade severity.
  actions: Action[]; // name + callbackId + tooltip
}
```