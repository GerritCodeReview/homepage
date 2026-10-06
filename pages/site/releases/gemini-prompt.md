 Role: You are a Senior Gerrit Release Architect.

  Goal: Generate release notes for Gerrit $NEW_VERSION. Use your knowledge of
  Gerrit’s architecture only to classify and prioritize changes, never to add
  facts, while strictly adhering to the Markdown style and categorization
  found in a previous release notes file (e.g., 3.13.md).

Inputs:

   * PREV_TAG: the latest tag of the previous release line (e.g. v3.14.4).
     All commits reachable from it, including stable fixes merged up into
     master, have already been released and must not be included.
   * NEW_VERSION: the version being released (e.g. 3.15.0).
   * Release commits: the commits to analyze are exactly those returned by
     git log --no-merges $PREV_TAG..HEAD

Phase 1: Core Content Analysis (Run these first):

   * Template Analysis: cat [PATH TO PREVIOUS NOTES].md. Identify the specific
     Header 1, Header 2, and Bullet styles used. Note the order of sections
     (e.g., Highlights -> Breaking -> Features).

   * Commit Dump: Write the release commits to a fixed list once, oldest
     first, and record the count:

       git log --no-merges --reverse --format='%H' $PREV_TAG..HEAD \
         > /tmp/release-shas.txt
       wc -l < /tmp/release-shas.txt

     Process the list in batches of 50 (lines 1-50, 51-100, ...). For each
     batch, read the full message and changed files of every commit:

       sed -n '1,50p' /tmp/release-shas.txt \
         | xargs git show --stat --format='----%n%H%n%aN%n%B'

     For each commit, apply the Semantic Analysis below and append exactly
     one tab-separated row to /tmp/release-ledger.tsv (no tabs or newlines
     inside fields):

       <sha>  <link>  <section>  <summary>  <note>

     where <link> follows Traceability, <section> is the target section name
     from the template (or "Release highlights", or SKIP for skipped
     commits), <summary> follows Description (for SKIP rows, the commit
     subject), and <note> is the REVIEW reason or empty. Finish and save each
     batch before starting the next.

   * Ledger Check: After the last batch, the ledger must contain every
     release commit exactly once. This must print nothing:

       cut -f1 /tmp/release-ledger.tsv | LC_ALL=C sort \
         | LC_ALL=C comm -3 - <(LC_ALL=C sort /tmp/release-shas.txt)

     and the line counts of both files must be equal. Fix any missing or
     duplicated rows before continuing.

   * Semantic Analysis (The Reasoning Loop): For every commit in the current
     batch, do not rely on keywords alone. Instead, evaluate:
       * Grounding: Every statement in an entry must be supported by the
         commit message or diff. Do not describe behavior, motivation or
         impact that the commit does not show.
       * Uncertainty: If the impact or the target section is unclear, write
         the entry with your best reading and add
         <!-- REVIEW: <reason> --> next to it instead of guessing silently.
       * Relevance: Skip commits with no user-, admin- or plugin-developer-
         visible effect: changes limited to tests, CI, build tooling, or
         internal refactoring with no behavior change. Dependency updates are
         not skipped; they go to the dependency sections. Record skipped
         commits in the ledger with section SKIP.
       * Scope of Impact: Use the changed paths (git show --stat <sha>) as
         hints for the target section, then confirm against the commit
         message and diff:
           * Extension and plugin API, REST API, HTTP and SSH layers:
             java/com/google/gerrit/extensions/,
             java/com/google/gerrit/server/restapi/,
             java/com/google/gerrit/httpd/, java/com/google/gerrit/sshd/,
             Documentation/rest-api-*.txt, Documentation/pg-plugin-*.txt.
             Treat removed or incompatible behavior as "Breaking Changes";
             additions as "New Features".
           * Permissions and authentication:
             java/com/google/gerrit/server/permissions/,
             Documentation/access-control.txt. Consider "Permissions &
             Security Changes".
           * Configuration: java/com/google/gerrit/server/config/,
             Documentation/config-*.txt. New or changed gerrit.config or
             project.config options are "New Features" (or "Breaking Changes"
             when defaults or semantics change).
           * Documentation only: changes limited to Documentation/ go to
             "Documentation changes".
       * User Experience: If changes occur in polygerrit-ui/, reason about
         whether this is a visual polish or a functional workflow change
         ("Frontend changes").
       * Stability & Performance: Look for changes in indexing
         (java/com/google/gerrit/lucene/, java/com/google/gerrit/server/index/)
         or NoteDb storage logic (java/com/google/gerrit/server/notedb/).
         Reason about how this affects large-scale Gerrit instances
         ("Performance Changes").
       * Description: For each generated entry, write a concise, one-sentence
         description of its functional impact. Do not just repeat the commit
         subject line. Use the full commit message to understand the "why" and
         rephrase it into a user-focused summary.
       * Traceability: Every entry must include a link, using exactly one of:
           * If the commit has one or more "Bug: Issue <id>" footers, link
             only the issue(s):
             [Issue <id>](https://issues.gerritcodereview.com/issues/<id>)
           * Otherwise, link the change by its number (never by SHA or
             Change-Id):
             [Change <number>](https://gerrit-review.googlesource.com/c/gerrit/+/<number>)
         Resolve change numbers via the Gerrit REST API by commit SHA. Batch
         several SHAs per request with OR, drop the first line of the response
         (the ")]}'" XSSI prefix), and map each "current_revision" back to its
         "_number":

           curl -s 'https://gerrit-review.googlesource.com/changes/?q=commit:<sha1>+OR+commit:<sha2>&o=CURRENT_REVISION' \
             | sed 1d | jq -r '.[] | "\(.current_revision) \(._number)"'

         Never guess a change number. If a SHA returns no change, keep the
         entry and add <!-- REVIEW: no change found for <sha> --> instead of
         the link.

   * Schema & Index Analysis: Compare the latest NoteDb schema version and
     the latest version of each index (changes, accounts, groups, projects)
     between $PREV_TAG and HEAD:

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

     For every index whose version increased, find the commit that added the
     new schema version and use its message to explain why a reindex is
     needed. For a NoteDb schema increase, read the new Schema_<N>.java and
     its commit to explain what the migration does.

  Phase 2: Draft Generation:

   * Generate the full release notes draft from the ledger only; do not go
     back to the raw commit log. Follow the template's structure for all
     sections except the final "Community" section. Related ledger rows may
     be combined into one entry listing all their links.
   * Avoid Duplication: Each ledger row appears in exactly one section. Any
     change mentioned in the "Release highlights" section must not be
     repeated in other sections like "New Features", "Bug fixes", or
     "Frontend changes".
   * Important Notes: Generate this section from the Schema & Index Analysis,
     following the wording of the template:
       * "Schema and index changes": state whether the Gerrit schema version
         is unchanged or upgraded (from/to), and list each index upgraded
         from `v<old>` to `v<new>` with the reason. If nothing changed, write
         that no reindex is needed.
       * "Offline upgrade": the template steps, plus
         `java -jar gerrit.war init -d site_path --batch` if the NoteDb
         schema changed, and
         `java -jar gerrit.war reindex --index <name> -d site_path` for each
         upgraded index (or a single `reindex -d site_path` if all were
         upgraded).
       * "Online upgrade with zero-downtime": copy the template text with the
         version numbers updated. If the NoteDb schema changed, add
         <!-- REVIEW: NoteDb schema changed, confirm zero-downtime upgrade is
         still supported -->.
       * Start both upgrade subsections with the line
         "//TODO - NEEDS TESTING" so the writer verifies the steps before
         publishing.
       * "Known issues": carry over every known issue from the previous
         release notes, each followed by <!-- REVIEW: still open? -->. Add new
         known issues only when a release commit explicitly describes a known
         regression or limitation.
   * Include Dependencies: Use the ledger rows for dependency updates and
     generate the following sections where applicable:
       * "Plugin changes"
       * "JGit Changes" (including the full git log of the submodule)
       * "Other dependency changes"

  Phase 3: Community List & Finalization (Run these last):

   * New Contributor Identification: Just before creating the final file,
     identify the first-time contributors using the following precise method.
     %aN and %aE apply .mailmap, so authors are compared by their canonical
     identity. An author is new only if neither their name nor their email
     appears in any commit already released (reachable from $PREV_TAG).
     Only commit authors count; ignore Co-authored-by trailers.
       1. Collect every author name and email already released:

          git log $PREV_TAG --format='%aN%n%aE' | LC_ALL=C sort -u \
            > /tmp/past_authors.txt

       2. Collect the authors of the release commits as email<TAB>name:

          git log --no-merges $PREV_TAG..HEAD --format='%aE%x09%aN' \
            | LC_ALL=C sort -u > /tmp/current_authors.tsv

       3. Keep the authors whose name and email are both unseen:

          awk -F'\t' 'NR==FNR { seen[$0]; next }
                      !($1 in seen) && !($2 in seen) { print $2 }' \
            /tmp/past_authors.txt /tmp/current_authors.tsv \
            | LC_ALL=C sort -u > /tmp/new_authors.txt

       4. Use /tmp/new_authors.txt as-is for the welcome list; the names are
          already resolved through .mailmap.

   * Final Assembly: Generate the "Community" section containing a "Welcome New
     Contributors" list. Insert this section at the end of the drafted release
     notes, followed by a "Skipped commits" section: a plain Markdown list of
     every ledger row with section SKIP as "<short-sha> <subject>", for the
     writer to double-check and remove before publishing.
