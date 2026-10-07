# Gerrit release notes prompt

## Role

You are a Senior Gerrit Release Architect.

## Goal

Generate release notes for Gerrit `$NEW_VERSION`. Use your knowledge of
Gerrit’s architecture only to classify and prioritize changes, never to add
facts, while strictly adhering to the Markdown style and categorization found
in `$PREV_NOTES`.

## Inputs

* `GERRIT_REPO`: path to a local clone of the Gerrit core repository
  (`https://gerrit.googlesource.com/gerrit`). Before starting, ask the user
  where to find it; do not clone it yourself. Check that it is a Gerrit clone
  and contains `$PREV_TAG`:

  ```shell
  git -C $GERRIT_REPO remote -v | grep gerrit.googlesource.com/gerrit
  git -C $GERRIT_REPO rev-parse --verify "$PREV_TAG^{commit}"
  git -C $GERRIT_REPO log -1 --oneline HEAD
  ```

  If a check fails, tell the user and ask again. Show the user the `HEAD`
  commit and confirm it is the one being released. Run every `git` command
  in this prompt from `$GERRIT_REPO`; the `PREV_NOTES` and `OUTPUT` paths are
  relative to this release notes repository.
* `PREV_TAG`: the latest tag of the previous release line (e.g. `v3.14.4`).
  All commits reachable from it, including stable fixes merged up into master,
  have already been released and must not be included.
* `NEW_VERSION`: the version being released (e.g. `3.15.0`).
* `PREV_NOTES`: the release notes of the immediately previous release line,
  used as the template (e.g. `pages/site/releases/3.14.md`).
* `OUTPUT`: `pages/site/releases/<major>.<minor>.md` for `NEW_VERSION` (e.g.
  `pages/site/releases/3.15.md`). If the file already exists, stop and ask
  instead of overwriting it.
* Release commits: the commits to analyze are exactly those returned by
  `git log --no-merges $PREV_TAG..HEAD`.

## Phase 1: Core Content Analysis (run these first)

### Template Analysis

`cat $PREV_NOTES`. Identify the specific Header 1, Header 2, and Bullet styles
used. Note the order of sections (e.g., Highlights -> Breaking -> Features).

### Commit Dump

Write the release commits to a fixed list once, oldest first, and record the
count:

```shell
git log --no-merges --reverse --format='%H' $PREV_TAG..HEAD \
  > /tmp/release-shas.txt
wc -l < /tmp/release-shas.txt
```

Process the list in batches of 50 (lines 1-50, 51-100, ...). For each batch,
read the full message and changed files of every commit:

```shell
sed -n '1,50p' /tmp/release-shas.txt \
  | xargs git show --stat --format='----%n%H%n%aN%n%B'
```

For each commit, apply the Semantic Analysis below and append exactly one
tab-separated row to `/tmp/release-ledger.tsv` (no tabs or newlines inside
fields):

```
<sha>  <link>  <section>  <summary>  <note>
```

where `<link>` follows Traceability, `<section>` is the target section name
from the template (or "Release highlights", or `SKIP` for skipped commits),
`<summary>` follows Description (for `SKIP` rows, the commit subject), and
`<note>` is the REVIEW reason, the skip reason (e.g. `fixes unreleased code`),
or empty. Finish and save each batch before starting the next.

### Ledger Check

After the last batch, the ledger must contain every release commit exactly
once. This must print nothing:

```shell
cut -f1 /tmp/release-ledger.tsv | LC_ALL=C sort \
  | LC_ALL=C comm -3 - <(LC_ALL=C sort /tmp/release-shas.txt)
```

and the line counts of both files must be equal. Fix any missing or duplicated
rows before continuing.

### Semantic Analysis (The Reasoning Loop)

For every commit in the current batch, do not rely on keywords alone. Instead,
evaluate:

* **Grounding**: Every statement in an entry must be supported by the commit
  message or diff. Do not describe behavior, motivation or impact that the
  commit does not show.
* **Uncertainty**: If the impact or the target section is unclear, write the
  entry with your best reading and add `<!-- REVIEW: <reason> -->` next to it
  instead of guessing silently.
* **Relevance**: Skip commits with no user-, admin- or plugin-developer-visible
  effect: changes limited to tests, CI, build tooling, or internal refactoring
  with no behavior change. Dependency updates are not skipped; they go to the
  dependency sections. Record skipped commits in the ledger with section
  `SKIP`.
* **Released Bugs Only**: "Bug fixes" lists only fixes for bugs present in a
  released version. A fix for a bug introduced by another release commit
  (i.e. the bug was never released) is skipped: record it as `SKIP` with the
  note `fixes unreleased code`. For every fix, find which commits introduced
  the lines it modifies or deletes, ignoring tests, and whether they were
  released:

  ```shell
  git diff -U0 <sha>^ <sha> -- . ':!javatests' ':!*_test.ts' \
    | awk '/^--- a\//{f=substr($0,7)} /^@@/{split($2,a,","); n=(a[2]=="")?1:a[2]; if (n>0) print f, substr(a[1],2), n}' \
    | while read -r f s n; do
        git blame --porcelain -L "$s,+$n" <sha>^ -- "$f" | awk '/^[0-9a-f]{40} /{print $1}'
      done \
    | sort -u \
    | while read -r c; do
        git merge-base --is-ancestor "$c" "$PREV_TAG" && echo released || echo unreleased
      done \
    | sort | uniq -c
  ```

  * Only `unreleased`: the bug was never released; skip the fix.
  * Any `released`: the fix addresses released code; keep it in "Bug fixes".
  * No output (the fix only adds lines): decide from the commit message. If it
    names the commit or change that introduced the bug, check whether that
    one is a release commit
    (`git log --format=%h $PREV_TAG..HEAD --grep='Change-Id: <id>'`). If the
    origin is still unclear, keep the fix in "Bug fixes" and add
    `<!-- REVIEW: could not tell whether this bug was released -->`.
* **Scope of Impact**: Use the changed paths (`git show --stat <sha>`) as hints
  for the target section, then confirm against the commit message and diff:
  * Extension and plugin API, REST API, HTTP and SSH layers:
    `java/com/google/gerrit/extensions/`,
    `java/com/google/gerrit/server/restapi/`,
    `java/com/google/gerrit/httpd/`, `java/com/google/gerrit/sshd/`,
    `Documentation/rest-api-*.txt`, `Documentation/pg-plugin-*.txt`.
    Treat removed or incompatible behavior as "Breaking Changes"; additions as
    "New Features".
  * Permissions and authentication:
    `java/com/google/gerrit/server/permissions/`,
    `Documentation/access-control.txt`. Consider "Permissions & Security
    Changes".
  * Configuration: `java/com/google/gerrit/server/config/`,
    `Documentation/config-*.txt`. New or changed `gerrit.config` or
    `project.config` options are "New Features" (or "Breaking Changes" when
    defaults or semantics change).
  * Documentation only: changes limited to `Documentation/` go to
    "Documentation changes".
* **User Experience**: If changes occur in `polygerrit-ui/`, reason about
  whether this is a visual polish or a functional workflow change ("Frontend
  changes").
* **Stability & Performance**: Look for changes in indexing
  (`java/com/google/gerrit/lucene/`, `java/com/google/gerrit/server/index/`) or
  NoteDb storage logic (`java/com/google/gerrit/server/notedb/`). Reason about
  how this affects large-scale Gerrit instances ("Performance Changes").
* **Description**: For each generated entry, write a one-sentence summary of
  its functional impact. Do not just repeat the commit subject line. Use the
  full commit message to understand the "why" and rephrase it into a
  user-focused summary. Only for breaking changes, highlights, or entries that
  need upgrade or configuration guidance, add an indented explanation
  paragraph below the summary, as in the template.
* **Traceability**: Every entry outside "Release highlights" must include a
  link, using exactly one of:
  * If the commit has one or more `Bug: Issue <id>` footers, link only the
    issue(s):
    `[Issue <id>](https://issues.gerritcodereview.com/issues/<id>)`
  * Otherwise, link the change by its number (never by SHA or Change-Id):
    `[Change <number>](https://gerrit-review.googlesource.com/c/gerrit/+/<number>)`

  Resolve change numbers via the Gerrit REST API by commit SHA. Batch several
  SHAs per request with `OR`, drop the first line of the response (the `)]}'`
  XSSI prefix), and map each `current_revision` back to its `_number`:

  ```shell
  curl -s 'https://gerrit-review.googlesource.com/changes/?q=commit:<sha1>+OR+commit:<sha2>&o=CURRENT_REVISION' \
    | sed 1d | jq -r '.[] | "\(.current_revision) \(._number)"'
  ```

  Never guess a change number. If a SHA returns no change, keep the entry and
  add `<!-- REVIEW: no change found for <sha> -->` instead of the link.

### Schema & Index Analysis

Compare the latest NoteDb schema version and the latest version of each index
(changes, accounts, groups, projects) between `$PREV_TAG` and `HEAD`:

```shell
for f in \
  java/com/google/gerrit/server/index/change/ChangeSchemaDefinitions.java \
  java/com/google/gerrit/server/index/account/AccountSchemaDefinitions.java \
  java/com/google/gerrit/server/index/group/GroupSchemaDefinitions.java \
  java/com/google/gerrit/index/project/ProjectSchemaDefinitions.java; do
  for ref in $PREV_TAG HEAD; do
    printf '%s %s v' "$ref" "$(basename "$f" SchemaDefinitions.java)"
    git show "$ref:$f" | grep -oE '> V[0-9]+' \
      | tr -dc '0-9\n' | sort -n | tail -n 1
  done
done
for ref in $PREV_TAG HEAD; do
  printf '%s NoteDb schema ' "$ref"
  git show "$ref:java/com/google/gerrit/server/schema/NoteDbSchemaVersions.java" \
    | grep -oE 'Schema_[0-9]+' | tr -dc '0-9\n' | sort -n | tail -n 1
done
```

For every index whose version increased, find the commit that added the new
schema version and use its message to explain why a reindex is needed. For a
NoteDb schema increase, read the new `Schema_<N>.java` and its commit to
explain what the migration does.

## Phase 2: Draft Generation

### Header

Copy the YAML front matter of `$PREV_NOTES` with the title set to
`Gerrit <major>.<minor>.x` and the permalink to `<major>.<minor>.html`. Follow
it with the Download and Documentation lines listing only `NEW_VERSION`:

```markdown
Download: **[<NEW_VERSION>](https://gerrit-releases.storage.googleapis.com/gerrit-<NEW_VERSION>.war)**

Documentation: **[<NEW_VERSION>](https://gerrit-documentation.storage.googleapis.com/Documentation/<NEW_VERSION>/index.html)**
```

Omit the "Bugfix releases" section; there are none yet.

### Body

Generate the full release notes draft from the ledger only; do not go back to
the raw commit log. Follow the template's structure for all sections except
the final "Community" section.

### Avoid Duplication

Each ledger row appears in exactly one section. Any change mentioned in the
"Release highlights" section must not be repeated in other sections like "New
Features", "Bug fixes", or "Frontend changes".

Ledger rows about the same functionality (the same REST endpoint, SSH
command, configuration option, search operator, extension point or UI
feature, or follow-ups of the same change) must be combined into a single
entry listing all their links, never described in separate entries or
sections. Place the combined entry in the most significant of their
sections, in this order: "Breaking Changes", "Permissions & Security
Changes", "New Features", "Performance Changes", "Bug fixes", then the
others. For example, a fix to the `config/server/index.changes` REST endpoint
and a later breaking change to the same endpoint form one "Breaking Changes"
entry.

No Change or Issue link may appear more than once in the draft. This must
print nothing:

```shell
grep -oE '\[(Change|Issue) [0-9]+\]' $OUTPUT | sort | uniq -d
```

### Release Highlights

Write the release highlights as prose without Change or Issue links, as in
the template; Traceability applies to all the other sections. Links to
documentation are allowed.

### Java Highlight

If the release changes the Java version Gerrit is built, distributed or
required to run with, the first release highlight must be a
`### Java <version>` section describing it, as in the 3.9, 3.11 and 3.12
release notes. Following Avoid Duplication, these changes appear only there,
not in "Breaking Changes" or any other section.

### Important Notes

Generate this section from the Schema & Index Analysis, following the wording
of the template:

* "Schema and index changes": state whether the Gerrit schema version is
  unchanged or upgraded (from/to), and list each index upgraded from
  `v<old>` to `v<new>` with the reason. If nothing changed, write that no
  reindex is needed.
* "Offline upgrade": the template steps, plus
  `java -jar gerrit.war init -d site_path --batch` if the NoteDb schema
  changed, and `java -jar gerrit.war reindex --index <name> -d site_path` for
  each upgraded index (or a single `reindex -d site_path` if all were
  upgraded).
* "Online upgrade with zero-downtime": copy the template text with the version
  numbers updated. If the NoteDb schema changed, add
  `<!-- REVIEW: NoteDb schema changed, confirm zero-downtime upgrade is still supported -->`.
* Start both upgrade subsections with the line `//TODO - NEEDS TESTING` so the
  writer verifies the steps before publishing.
* "Known issues": carry over every known issue from the previous release
  notes, each followed by `<!-- REVIEW: still open? -->`. Add new known issues
  only when a release commit explicitly describes a known regression or
  limitation.

### Include Dependencies

Use the ledger rows for dependency updates and generate the following sections
where applicable:

* "Plugin changes" and "JGit Changes": list the submodule commits at both ends
  to find which ones moved:

  ```shell
  for ref in $PREV_TAG HEAD; do
    git ls-tree $ref modules/jgit plugins/ \
      | awk -v ref=$ref '$2=="commit" {print ref, $4, $3}'
  done
  ```

  For each moved submodule, read its history (initialize it first with
  `git submodule update --init <path>` if needed):

  ```shell
  git -C <path> log --no-merges <old>..<new>
  ```

  and apply the same Grounding, Relevance and Description rules as for the
  release commits.
* "JGit Changes": follow the template:
  `Update JGit to [<new-short-sha>](https://eclipse.gerrithub.io/q/<new-short-sha>).`,
  then a shell block with
  `$ git log --oneline --no-merges <old-short-sha>..<new-short-sha>`, then
  `Notable changes are:` with one line per user-visible commit:
  `- [<short-sha>](https://eclipse.gerrithub.io/q/<short-sha>) <subject>`.
  Do not paste the full log.
* "Plugin changes": consider only the `plugins/*` submodules that moved, as
  listed above. Ignore everything else: release commits touching other files
  under `plugins/` (e.g. `BUILD`, `package.json`, `yarn.lock`), commits that
  mention plugins, and plugins that are not submodules. Never assign a release
  commit to "Plugin changes" in the ledger. Write one `### <Plugin name> plugin`
  subsection per moved submodule with user-visible changes, with entries
  linked as in Traceability (the REST lookup by commit SHA also finds plugin
  changes; use `https://gerrit-review.googlesource.com/c/<project>/+/<number>`
  with the project returned by the lookup).
* "Other dependency changes"

## Phase 3: Community List & Finalization (run these last)

### New Contributor Identification

Just before creating the final file, identify the first-time contributors
using the following precise method. `%aN` and `%aE` apply `.mailmap`, so
authors are compared by their canonical identity. An author is new only if
neither their name nor their email appears in any commit already released
(reachable from `$PREV_TAG`). Only commit authors count; ignore
`Co-authored-by` trailers.

1. Collect every author name and email already released:

   ```shell
   git log $PREV_TAG --format='%aN%n%aE' | LC_ALL=C sort -u \
     > /tmp/past_authors.txt
   ```

2. Collect the authors of the release commits as `email<TAB>name`:

   ```shell
   git log --no-merges $PREV_TAG..HEAD --format='%aE%x09%aN' \
     | LC_ALL=C sort -u > /tmp/current_authors.tsv
   ```

3. Keep the authors whose name and email are both unseen:

   ```shell
   awk -F'\t' 'NR==FNR { seen[$0]; next }
               !($1 in seen) && !($2 in seen) { print $2 }' \
     /tmp/past_authors.txt /tmp/current_authors.tsv \
     | LC_ALL=C sort -u > /tmp/new_authors.txt
   ```

4. Use `/tmp/new_authors.txt` as-is for the welcome list; the names are
   already resolved through `.mailmap`.

### Final Assembly

Generate the "Community" section using the exact heading and intro sentence of
the new contributors subsection in `$PREV_NOTES` with the version updated,
followed by the names in `/tmp/new_authors.txt`. Omit the subsection if there
are no new contributors. Insert this section at the end of the drafted release
notes, followed by a "Skipped commits" section. Start the section with the
comment `<!-- REVIEW: these skipped commits need reviewing; move any relevant
ones into the release notes, then remove this section before publishing -->`,
followed by a plain Markdown list of every ledger row with section `SKIP` as
`<short-sha> <subject>`. Write the complete draft to `$OUTPUT`.
