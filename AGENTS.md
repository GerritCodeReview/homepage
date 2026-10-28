# Repository Guidelines

## Project Structure & Module Organization
This repository is a Jekyll site for `gerritcodereview.com`.
- Content pages: `index.md`, `404.md`, and `pages/**` (site docs, releases, design docs, tags).
- Blog/news posts: `_posts/*.md` using `YYYY-MM-DD-title.md`.
- Layout and reusable snippets: `_layouts/**`, `_includes/**`, `_data/**`.
- Static assets: `assets/css/`, `js/`, `images/`.
- Build output: `_site/` (generated; do not hand-edit).
- Tooling scripts: `tools/plugins.py`, `createtag`.

## Build, Test, and Development Commands
- `bundle install`: install Ruby/Jekyll dependencies from `Gemfile`.
- `bundle exec jekyll build`: produce static site in `_site/` (main validation step).
- `docker compose up`: preferred local workflow; builds and serves on `http://localhost:4000`.
- `docker compose run --rm server bundle exec jekyll build`: fallback build command when `bundle` is unavailable on the host.
- For a clean rebuild if container state is broken, first run `git clean -ndx` and review every path it would delete. Obtain explicit user approval before running `docker compose down && git clean -fdx && docker compose up`; this deletes all untracked and ignored files, potentially including `AGENTS.md` and local tooling.
- `pipenv install --dev`: install Python tooling used by `tools/plugins.py`.
- `pipenv run python tools/plugins.py -a`: regenerate plugin content using anonymous access; use `-n` instead to authenticate with `.netrc` credentials.

## Known Workarounds and Notes
- In this environment, `bundle` may not be installed on the host (`bundle: command not found`). Use Docker commands for Jekyll validation.
- `docker compose config -q` is a quick sanity check that the compose file is valid before running heavier commands.
- Running `docker compose run --rm server bundle exec jekyll build` can reinstall Bundler inside the ephemeral container on each run (lockfile expects Bundler `4.0.3`). This is expected in short-lived containers.
- For faster iterative checks, keep `docker compose up` running and validate pages at `http://localhost:4000` instead of repeated one-off container runs.
- For CSS cleanup, use PurgeCSS in analysis mode first:
  - `npx purgecss --css _site/assets/css/style.css --content '_site/**/*.html' 'js/*.js' --rejected --rejected-css`
  - Review rejected selectors manually before deletion because `_includes/` templates and dynamic selectors can look unused in current output.
- If PurgeCSS tooling was installed locally, avoid committing transient Node artifacts unless intentionally adding tooling:
  - `node_modules/`, `package.json`, `package-lock.json`.

## Coding Style & Naming Conventions
- Markdown/front matter: keep keys consistent with existing pages (`title`, `permalink`, `layout`, etc.).
- Posts must follow date-based filenames: `_posts/YYYY-MM-DD-short-title.md`.
- Python (`tools/*.py`): format with `black`, lint with `flake8` (`max-line-length = 100`).
- Keep changes focused; avoid unrelated formatting churn in large content files.

## Testing Guidelines
Validate changes with fresh production and controlled-fixture builds (see README.md):
- Run `bundle exec jekyll build` before uploading a Change.
- Run `python3 -m unittest discover -s tests -p test_check_site.py -v` and
  `python3 tools/check_site.py` for offline generated-site validation.
- Prepare fixtures with `python3 tools/prepare_test_site.py`, build them as described
  in README.md, then run
  `TEST_SITE=_test/site python3 -m unittest discover -s tests -p test_rendering.py -v`.
- Browser tests require Node 22+: run `npm ci`, `npm run test:install-browser`, and
  `npm test` after building both sites. Reports and `_test/` are generated; do not commit them.
- Preserve behavior-focused TOC tests through layout redesigns; sidebar-specific
  assertions belong with the sidebar implementation.
- For Python tooling updates, run `pipenv run flake8` and `pipenv run black --check tools`.
- Manually spot-check affected pages in local `jekyll serve` output.

## Commit & Review Guidelines (Gerrit)
- Follow the observed commit style: short, imperative subject lines (e.g., `Add release notes for Gerrit v3.13.5`, `Update links to latest release`).
- Keep subject lines specific to user-visible impact.
- Install the Gerrit `commit-msg` hook once per clone so commits include `Change-Id`:
  - `curl -Lo $(git rev-parse --git-dir)/hooks/commit-msg https://gerrit-review.googlesource.com/tools/hooks/commit-msg && chmod +x $(git rev-parse --git-dir)/hooks/commit-msg`
- Push commits as Gerrit Changes for review (not pull requests), typically via:
  - `git push origin HEAD:refs/for/master`
- Change descriptions should include:
  - what changed and why,
  - issue/context links when applicable,
  - screenshots for visible UI/layout updates,
  - confirmation that `bundle exec jekyll build` passed locally.

## Security & Configuration Tips
- Do not commit credentials or tokens (Firebase and Gerrit credentials are injected in CI).
- Treat `_config.yml`, `firebase.json`, and deployment settings as high-impact files; review carefully.
