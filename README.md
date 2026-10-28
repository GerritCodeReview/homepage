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
