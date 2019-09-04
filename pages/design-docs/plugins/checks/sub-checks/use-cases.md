# Use-cases

Some checkers may run multiple units of work (some call these "jobs",
we will call them "sub-checks" in this document) as part of a single
check.  Users may wish to be able to see the individual results and
log links for these units of work as conveniently as they do now with
checks themselves.

## <a id="acceptance-criteria"> Acceptance Criteria

The checks plugin supports checkers returning additional data about
the sub-checks that they ran, and the Polygerrit UI renders this in a
manner that provides similar information about sub-checks as checks.

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

  Such grouping allows users to easily confirm that all of the
  expected sub-checks run by a checker are present, as well as help
  identify which checker system ran a sub-check.

* A checker may have its own facilities for determining which checks
  to run on a change in Gerrit, and they may be more dynamic than the
  checks API facilitates.

The project gating system Zuul provides an example of both situations.
Zuul supports in-repository configuration of jobs (that is, changes to
Zuul's configuration are made as changes to files in git repositories
and go through code-review and testing as well) -- to the extent that
a single change to a tested repo can define a new job, configure that
job to run on changes to that repo, and the new job will be run on the
very change that defined it, even before that change is merged.
Further, Zuul supports additional criteria for deciding which jobs to
run that would be difficult or impossible to encode in Gerrit queries;
for example, Zuul supports establishing relationships between jobs in
a full directed acyclic graph, so that one job can determine whether
others run based on its result.

Other examples of dynamic job configuration in Zuul include:

* Jobs which only run on certain branches, or if certain files are
  changed (or if certain files are *not* changed).  These are all
  supported by the current checks API, but some users may find it
  convenient to manage that within the external system.

* Jobs which only run if other checks are run (e.g., if a job builds
  an image, 1 or more subsequent jobs may run which then use that
  image in testing).

* Jobs which only run if other checks succeed (e.g., to save
  resources, run a style test first and then run integration test if
  that passes)

* Jobs which decide what other checks to run (e.g., a job runs a
  script to perform analysis on the contents of the change's repo to
  decide which tests should run).

* Jobs which are configured within the change under test (as described
  above).

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

## <a id="ux"> UX Considerations

While some of this could be accomodated in the current API by
reporting a URL hosted by the checker which enumerates the results of
individual jobs, we would like to reduce the number of times a user
has to leave Gerrit to find information about a change.  In the same
way that displaying results, timing information, and a re-run button
helps keep the most relevant information and actions related to a
change in Gerrit, displaying subchecks will as well.

Many times it is important to see and understand which jobs ran for a
change; for example, in a repo with many jobs configured, only a few
of which may run for a given change depending on what files are
updated, the user may want to confirm that the expected jobs ran, and
they should be able to do so easily without leaving the change screen
in Gerrit.

In some cases (for example, when there is only one check) the
relationship between sub-checks and checks is unimportant to the user.
However, in other cases (for example, in a system with many checkers
operated by different parties), it is important for users to be able
to see the relationship between sub-checks and their parent checks.

An example of such a case is the third-party testing employed by the
OpenStack project.  In this system, a single project may have many
third-party systems each reporting the results of several sub-checks.
In this case, knowing that, for example, the "nova-database" sub-check
is run by the "IBM DB2" third-party check provides important context
to the user.
