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
| `url`           | optional | A fully-qualified URL pointing to the status or result of the sub-check on the checker's infrastructure.
| `started`       | optional | The timestamp of when the sub-check started processing.
| `finished`      | optional | The timestamp of when the sub-check finished processing.
| `config`        | optional | A SubCheckConfigInput entity.

This is essentially the CheckInput entity without the `checker_uuid`
field and the addition of the `name` and `config` fields.  If new
relevant fields are added to CheckInput, they should also be added to
SubCheckInput or SubCheckInputConfig.  The default value for `state`
is `NOT_STARTED`.

Define a SubCheckConfigInput entity as follows:

| Field Name      |          | Description |
| --------------- | -------- | ----------- |
| `rerunnable`    | optional | A boolean indicating whether the sub-check is individually rerunnable; false by default.
| `required`      | optional | A boolean indicating whether the sub-check is required for the check to be successful; false by default.

This entity is likely to be expanded in the future to contain other
configuration values.

Modify CheckInput to add a new field, `sub_checks`, which is a list of
SubCheckInput entities.  When a checker updates a check, it may
optionally provide information about sub-checks using this field.  If
the field is omitted, no updates are performed.  If existing
sub-checks are omitted in an update, they will be left unmodified.  If
`sub_checks` is the empty list, all sub-checks will be removed.  To
remove a subset of sub-checks, the caller may provide an update with
the empty list for `sub_checks` followed by a second update to restore
sub-checks which should be present.

Modify the CheckInfo entity to include an optional `sub_checks` field
which returns a list of SubCheckInfo entities if any sub-checks have
been stored.  It will be omitted if no sub-checks are present.

SubCheckInfo is defined as follows:

| Field Name            |          | Description |
| --------------------- | -------- | ----------- |
| `state`               |          | The state as string-serialized form of [CheckState](#check-state)
| `name`                |          | The name of this sub-check.
| `message`             | optional | Short message explaining the sub-check state.
| `url`                 | optional | A fully-qualified URL pointing to the status or result of the sub-check on the checker's infrastructure.
| `started`             | optional | The [timestamp](../../../Documentation/rest-api.html#timestamp) of when the sub-check started processing.
| `finished`            | optional | The [timestamp](../../../Documentation/rest-api.html#timestamp) of when the sub-check finished processing.
| `created`             |          | The [timestamp](../../../Documentation/rest-api.html#timestamp) of when the sub-check was created.
| `updated`             |          | The [timestamp](../../../Documentation/rest-api.html#timestamp) of when the sub-check was last updated.
| `config`              | optional | A SubCheckConfigInfo entity.

Define a SubCheckConfigInfo entity as follows:

| Field Name      |          | Description |
| --------------- | -------- | ----------- |
| `rerunnable`    | optional | A boolean indicating whether the sub-check is individually rerunnable.
| `required`      | optional | A boolean indicating whether the sub-check is required for the check to be successful; false by default.

The serialization of a check in NoteDB would be updated to include the
`sub_checks` field as described above, with the empty list indicating
no sub-checks are present.

Sub-checks may not contain further sub-checks -- that is to say that
only one level of hierarchy exists.  Systems such as Zuul which
support a deeper hierarchy of jobs must report a flat list when
sending data to Gerrit.

Sub-checks would not be separately indexed and therefore not
searchable, but this could be implemented as a future enhancement.

The check state and the sub-check states are independent -- it is the
responsibility of the calling system to ensure coherence between the
two states (eg, that if all the subchecks are `SUCCESFUL` that the
check is also `SUCCESSFUL`).  However, Gerrit will block submission on
any `required` sub-checks of `required` checks.

The `rerunnable` field indicates whether the sub-check is individually
rerunnable.  If it is true, then Gerrit may provide a "rerun" button
next to the sub-check (but only if access controls and configuration
allow it to also provide such a button for the overall check).  If a
user clicks the rerun button for an individual sub-check, Gerrit will
reset both the sub-check status to NOT_STARTED, and send the checker
notification event.

The rerun endpoint of the REST API will be updated to accept an
optional `sub_checkname` parameter to indicate that only the named
subcheck should be re-run.  E.g.:

'POST /changes/1/revisions/1/checks/test:my-checker/rerun?sub_check_name=code-style'

The pending checks endpoint will be modified to return sub-checks, so
that checkers may use the same endpoint to query for sub-checks.  An
example request and response follows:

```
  GET /plugins/@PLUGIN@/checks.pending/?query=checker:test:my-checker+(state:NOT_STARTED+OR+state:SCHEDULED) HTTP/1.0

  HTTP/1.1 200 OK
  Content-Disposition: attachment
  Content-Type: application/json; charset=UTF-8
  )]}'
  [
    {
      "patch_set": {
        "repository": "test-repo",
        "change_number": 1,
        "patch_set_id": 1,
      }
      "pending_sub_checks": {
        "test:my-checker": {
          "name": "my-sub-check",
          "state": "NOT_STARTED",
        }
      }
    }
  ]
```

The Polygerrit UI will be updated to render sub-checks similarly to
their parent check result, but with a visual indication of their
status as sub-checks.  An option to collapse the subchecks so they are
hidden will be provided, but they will be displayed by default.
