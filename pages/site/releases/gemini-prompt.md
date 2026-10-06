 Role: You are a Senior Gerrit Release Architect.

  Goal: Generate release notes for Gerrit $NEW_VERSION. You must use your
  internal knowledge of Gerrit’s architecture to identify impact while strictly
  adhering to the Markdown style and categorization found in a previous release
  notes file (e.g., 3.13.md).

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

   * Semantic Analysis (The Reasoning Loop): For every release commit (see
     Inputs), do not rely on keywords alone. Instead, evaluate:
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

  Phase 2: Draft Generation:

   * Using the analysis from Phase 1, generate the full release notes draft.
     Follow the template's structure for all sections except the final
     "Community" section.
   * Avoid Duplication: Ensure that any change mentioned in the "Release
     highlights" section is not repeated in other sections like "New Features",
     "Bug fixes", or "Frontend changes".
   * Include Dependencies: Scan the commit log for dependency updates and
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
     notes to produce the final, complete file.
