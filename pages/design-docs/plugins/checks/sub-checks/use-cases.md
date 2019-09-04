# Use-cases

Allow checkers to return information about sub-checks which they have
run.  This allows for better presentation of information about related
checks in the user interface, as well as the ability for checkers to
determine on their own which checks to run in a more ad-hoc manner.

## <a id="acceptance-criteria"> Acceptance Criteria

The checks plugin supports checkers returning additional data about
the sub-checks that they ran, and the Polygerrit UI renders this in a
useful and understandable manner.

## <a id="background"> Background

The checks API currently requires that each checker be defined and
configured in advance.  This supports having a fixed set of checkers
which may be used for any given change in a repo, and that set may be
further reduced by checkers utilizing a query which may limit the set
of changes to which it would apply.

There are multiple reasons that users may want a many-to-one
relationship between check results and checkers in Gerrit:

* A checker may perform a large number of checks, and being able to
  report all of them as well as group the results together in the user
  interface may improve usability.

* A checker may have its own facilities for determining which checks
  to run on a change in Gerrit, and they may be more dynamic.

The project gating system Zuul provides an example of both situations.
Zuul supports in-repository configuration of jobs -- to the extent that
a single change can define a new job, configure that job to run on
changes to that repo, and that job will be run on the very change that
defined it, even before that change is merged.  Further, Zuul supports
additional criteria for deciding which jobs to run that would be
difficult or impossible to encode in Gerrit queries; for example, Zuul
supports establishing relationships between jobs in a full directed
acyclic graph, so that one job can determine whether others run based
on its result.

Such ad-hoc (at least from Gerrit's point of view) selections of jobs
don't map well to the prior configuration required by the checks
system.

To remedy this, checkers should be able to report not only an overall
pass/fail result for the change, but also the results of individual
sub-checks associated with that check.  The information reported with
sub-checks should be similar to that provided by checks in general
(result, duration, URL, etc.).  The set of sub-checks is not defined
in advance, and may differ even between different patchsets of the
same change.
