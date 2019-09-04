# Solution

## <a id="overview"> Overview

This solution proposes that sub-checks be implemented as structured
data similar to checks themselves, and stored in NoteDB along with the
check result.

## <a id="detailed-design"> Detailed Design

Define a SubCheckInput entity as follows:

| Field Name      |          | Description |
| --------------- | -------- | ----------- |
| `state`         | optional | The state as string-serialized form of [CheckState](#check-state)
| `message`       | optional | Short message explaining the sub-check state.
| `url`           | optional | A fully-qualified URL pointing to the result of the sub-check on the checker's infrastructure.
| `started`       | optional | The timestamp of when the sub-check started processing.
| `finished`      | optional | The timestamp of when the sub-check finished processing.

This is essentially the CheckInput entity without the checker_uuid
field.  If new relevant fields are added to CheckInput, they should
also be added to SubCheckinput.

Modify CheckInput to add a new field, `sub_checks`, which is a list of
SubCheckInput entities.  When a checker updates a check, it may
optionally provide information about sub-checks using this field.

Similarly, modify the CheckInfo entity to include a `sub_checks` field
which returns the same data.

The GSON used to serialize a check in NoteDB would be updated to
include the sub_checks field as described above.

If a check has no sub-checks, the value of `sub_checks` is the empty
list.

Sub-checks may not contain further sub-checks -- that is to say that
only one level of hierarchy exists.  Systems such as Zuul which
support a deeper hierarchy of jobs will flatten the list when sending
data to Gerrit.

Sub-checks would not be separately indexed and therefore not
searchable, but this could be implemented as a future enhancement.

The Polygerrit UI will be updated to render sub-checks similarly to
their parent check result (omitting the "For submit" field since that
only applies to the check), but indented to indicate their status as
sub-checks.  An option to collapse the subchecks so they are hidden
will be provided, but they will be displayed by default.
