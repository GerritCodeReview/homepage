Phase 1: Core Content Analysis (Run these first):

   * Template Analysis: cat [PATH TO PREVIOUS NOTES].md. Identify the specific Header 1, Header 2, and Bullet styles used. Note the order of sections (e.g., Highlights -> Breaking -> Features).

   * Semantic Analysis (The Reasoning Loop): For every commit in git log <previous-tag>..HEAD, do not rely on keywords alone. Instead, evaluate:
       * Scope of Impact: If a change modifies gerrit-extension-api, gerrit-httpd, or gerrit-sshd, treat it as a potential Breaking Change or API Update.
       * User Experience: If changes occur in polygerrit-ui/, reason about whether this is a visual polish or a functional workflow change.
       * Stability & Performance: Look for changes in Lucene/FakeDB indexing or NoteDb storage logic. Reason about how this affects large-scale Gerrit instances.
       * Description: For each generated entry, write a concise, one-sentence description of its functional impact. Do not just repeat the commit subject line. Use the full commit message to understand the "why" and rephrase it into a
         user-focused summary.
       * Traceability: Every entry must include a link. Prioritize the Bug link (e.g., [Issue <id>](...))) if a Bug: <id> footer exists. Otherwise, use the Change link (e.g., [Change <hash>](...)).

  Phase 2: Draft Generation:

   * Using the analysis from Phase 1, generate the full release notes draft. Follow the template's structure for all sections except the final "Community" section.
   * Avoid Duplication: Ensure that any change mentioned in the "Release highlights" section is not repeated in other sections like "New Features", "Bug fixes", or "Frontend changes".
   * Include Dependencies: Scan the commit log for dependency updates and generate the following sections where applicable:
       * "Plugin changes"
       * "JGit Changes" (including the full git log of the submodule)
       * "Other dependency changes"

  Phase 3: Community List & Finalization (Run these last):

   * New Contributor Identification: Just before creating the final file, identify the first-time contributors using the following precise method:
       1. Generate a list of all unique author emails from the project's entire history up to the commit before this release's range:
          git log <previous-tag>^ --format='%ae' | sort -u > /tmp/past_authors.txt
       2. Generate a list of unique author emails from the current release's range:
          git log <previous-tag>..HEAD --format='%ae' | sort -u > /tmp/current_authors.txt
       3. Isolate the new author emails by finding those present in /tmp/current_authors.txt but not in /tmp/past_authors.txt:
          comm -23 /tmp/current_authors.txt /tmp/past_authors.txt > /tmp/new_author_emails.txt
       4. Using the list of new emails, retrieve the full names for the final list and resolve them using .mailmap.

   * Final Assembly: Generate the "Community" section containing a "Welcome New Contributors" list. Insert this section at the end of the drafted release notes to produce the final, complete file.
