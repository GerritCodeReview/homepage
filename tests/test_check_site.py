"""Behavioral tests for the generated-site validator (no third-party packages)."""

import json
from pathlib import Path
import tempfile
import unittest

from tools.check_site import SiteChecker


class SiteCheckerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.write("index.html", '<h1 id="intro">Home</h1>')
        self.write("search.json", "[]")

    def write(self, path, text):
        file = self.site / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def check(self, **kwargs):
        return SiteChecker(self.site, required=("index.html",), **kwargs).check()

    def test_missing_required_output_is_reported(self):
        (self.site / "index.html").unlink()
        self.assertIn("missing required output: index.html", self.check())

    def test_resolves_relative_directory_encoded_and_same_site_links(self):
        self.write(
            "guide/index.html",
            '<a href="../asset%20name.svg">a</a>'
            '<a href="../#intro">b</a>'
            '<a href="https://www.gerritcodereview.com/guide/#section">c</a>'
            '<h2 id="section">Section</h2>',
        )
        self.write("asset name.svg", "<svg/>")
        self.write(
            "index.html",
            '<h1 id="intro">Home</h1><a href="guide/">guide</a>'
            '<a href="//gerritcodereview.com/guide/#section">absolute</a>'
            '<a href="https://example.org/missing">external</a>'
            '<a href="mailto:x@example.org">mail</a><a href="#">toggle</a>',
        )
        self.assertEqual([], self.check())

    def test_missing_link_asset_and_fragment_are_reported(self):
        self.write(
            "index.html",
            '<a href="gone.html">gone</a><img src="gone.png">'
            '<script src="gone.js"></script><a href="#gone">fragment</a>',
        )
        errors = "\n".join(self.check())
        for target in ("gone.html", "gone.png", "gone.js", "#gone"):
            self.assertIn(target, errors)

    def test_redirects_are_resolved_and_cycles_reported(self):
        self.write(
            "index.html", '<a href="/old.md#intro">old</a><h1 id="intro">Home</h1>'
        )
        self.assertEqual([], self.check(redirects={"/old.md": "/index.html"}))
        errors = self.check(redirects={"/old.md": "/old.md"})
        self.assertIn("redirect cycle", "\n".join(errors))

    def test_legacy_named_anchors_are_valid(self):
        self.write("index.html", '<a name="legacy"></a><a href="#legacy">old</a>')
        self.assertEqual([], self.check())

    def test_search_requires_array_fields_and_valid_targets(self):
        for value in ({}, [None], [{}], [{"title": "Title", "url": "gone.html"}]):
            with self.subTest(value=value):
                self.write("search.json", json.dumps(value))
                self.assertTrue(self.check())
        self.write(
            "search.json",
            '[{"title":"Home","url":"/","tags":"",' '"keywords":"","summary":""}]',
        )
        self.assertEqual([], self.check())

    def test_malformed_search_json_is_reported(self):
        self.write("search.json", '[{"title": "bad "quote""}]')
        self.assertIn("invalid search JSON", "\n".join(self.check()))

    def test_exact_exceptions_do_not_hide_other_links(self):
        self.write("index.html", '<a href="old.html">old</a><a href="new.html">new</a>')
        exceptions = [
            {"source": "index.html", "url": "old.html", "reason": "Archived link"}
        ]
        errors = self.check(exceptions=exceptions)
        self.assertEqual(1, len(errors))
        self.assertIn("new.html", errors[0])

    def test_stale_exceptions_are_reported(self):
        exceptions = [
            {"source": "index.html", "url": "old.html", "reason": "Archived link"}
        ]
        self.assertIn(
            "unused link exception", "\n".join(self.check(exceptions=exceptions))
        )

    def test_test_tooling_must_not_be_deployed(self):
        self.write("tests/fixture.html", "test")
        self.assertIn("test/tooling output", "\n".join(self.check()))


if __name__ == "__main__":
    unittest.main()
