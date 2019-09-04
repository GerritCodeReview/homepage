# Solution

## <a id="overview"> Overview

This solution proposes that sub-checks be implemented as structured
data similar to checks themselves, and stored in NoteDB along with the
check result.

## <a id="detailed-design"> Detailed Design

Define a SubCheckInput entity as follows:

| Field Name      |          | Description |
| --------------- | -------- | ----------- |
| `name`          | required | The name of this sub-check; must be unique within this check.
| `state`         | optional | The state as string-serialized form of [CheckState](#check-state)
| `message`       | optional | Short message explaining the sub-check state.
| `url`           | optional | A fully-qualified URL pointing to the result of the sub-check on the checker's infrastructure.
| `started`       | optional | The timestamp of when the sub-check started processing.
| `finished`      | optional | The timestamp of when the sub-check finished processing.
| `rerunnable`   | optional | A boolean indicating whether the sub-check is individually rerunnable.

This is essentially the CheckInput entity without the `checker_uuid`
field and the addition of the `name` and `rerunnable` fields.  If new
relevant fields are added to CheckInput, they should also be added to
SubCheckInput.

Modify CheckInput to add a new field, `sub_checks`, which is a list of
SubCheckInput entities.  When a checker updates a check, it may
optionally provide information about sub-checks using this field.

Similarly, modify the CheckInfo entity to include a `sub_checks` field
which returns the same data.

The GSON used to serialize a check in NoteDB would be updated to
include the `sub_checks` field as described above.

If a check has no sub-checks, the value of `sub_checks` is the empty
list.

Sub-checks may not contain further sub-checks -- that is to say that
only one level of hierarchy exists.  Systems such as Zuul which
support a deeper hierarchy of jobs must report a flat list when
sending data to Gerrit.

Sub-checks would not be separately indexed and therefore not
searchable, but this could be implemented as a future enhancement.

The `rerunnable` field indicates whether the sub-check is individually
rerunnable.  If it is true, then Gerrit may provide a "rerun" button
next to the sub-check (but only if access controls and configuration
allow it to also provide such a button for the overall check).  If a
user clicks the rerun button for an individual sub-check, Gerrit will
reset both the sub-check and the overall check status to NOT_STARTED,
and send the checkr notification event.  The checker is expected to
retrieve the information about the check, notice the change in
sub-check status and therefore rerun that sub-check.

The rerun endpoint of the REST API will be updated to accept an
optional `name` parameter to indicate that only the named subcheck
should be re-run.  E.g.:

'POST /changes/1/revisions/1/checks/test:my-checker/rerun?name=code-style'

The Polygerrit UI will be updated to render sub-checks similarly to
their parent check result (omitting the "For submit" field since that
only applies to the check), but indented to indicate their status as
sub-checks.  An option to collapse the subchecks so they are hidden
will be provided, but they will be displayed by default.
