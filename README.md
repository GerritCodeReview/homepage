Homepage for [Gerrit Code Review][home].

[home]: https://www.gerritcodereview.com/

Instructions how to publish the Gerrit documentation can be found at:
https://www.gerritcodereview.com/publishing.html

## Regression checks

The Python checks require Python 3.9+ and no additional packages. Always
validate a fresh build; `_site/` is generated and must not be edited by hand.

```sh
python3 -m unittest discover -s tests -p test_check_site.py -v
python3 tools/prepare_test_site.py
bundle exec jekyll build
export BUNDLE_GEMFILE="$PWD/Gemfile"
(cd _test/source && bundle exec jekyll build --destination ../site)
python3 tools/check_site.py
TEST_SITE=_test/site python3 -m unittest discover -s tests -p test_rendering.py -v
```

When Bundler is unavailable on the host, replace the two build commands with:

```sh
docker compose run --rm server sh -c \
  'bundle exec jekyll build && cd _test/source && bundle exec jekyll build --destination ../site'
```

The validator checks required outputs, internal links and fragments, local
assets, and the search index without contacting external services. Firebase
redirects are resolved using `firebase.json`. Historical broken links are
listed as exact source/URL pairs with reasons in `tests/link-exceptions.json`;
unused exceptions fail validation. Do not add broad patterns or exceptions
for newly introduced bugs.

Rendering tests use the real templates with controlled content staged under
`_test/`. Tests, tools, and dependencies are excluded from production output.
The Python checks run before deployment in Jenkins.

### Browser checks

Browser tests require Node 22+ and the Chromium build matching the pinned
Playwright package. First build the production site and controlled fixtures
as above, then run:

```sh
npm ci
npm run test:install-browser
npm test
```

On a fresh Linux machine, a system administrator may also need to run
`npx playwright install-deps chromium`. Jenkins agents provision these system
packages in their image; jobs install browsers as the unprivileged `jenkins`
user. `TEST_PORT` overrides the default local port (4173).

The server exposes only generated output. Tests cover real TOC nesting and
labels, keyboard and mouse navigation, direct fragments, heading anchors,
optional TOCs, search, and long content at desktop/mobile widths and around
the current 768px breakpoint. Documentation currently has a static header;
visibility assertions also support a future sticky/fixed header. Scrolling
must settle before assertions pass. Floating-sidebar behavior is intentionally
not required until that redesign exists.

The harness replaces CDN downloads with local packages matching the versions
in `_includes/head.html`, disables analytics, and uses system fonts. The old
Bootstrap/jQuery/Popper versions are deliberate test-only mirrors of existing
production dependencies, not new shipped assets; upgrading those libraries
is separate work. Update the harness pins when production CDN versions change.

JUnit results go to `test-results/browser.xml`; HTML reports go to
`playwright-report/`, with screenshots and traces for failures. These artifacts
are ignored and excluded from deployment. Browser checks can run locally
independently of agent image rollout.
