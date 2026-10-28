"""Integration tests against the real templates rendered with controlled content."""

import json
import os
from pathlib import Path
import unittest

from tools.check_site import Document


@unittest.skipUnless(
    os.environ.get("TEST_SITE"), "set TEST_SITE to built fixture output"
)
class RenderingTest(unittest.TestCase):
    def setUp(self):
        self.site = Path(os.environ["TEST_SITE"])

    def test_search_preserves_escaping_and_nested_urls(self):
        entries = json.loads((self.site / "search.json").read_text())
        entry = next(e for e in entries if e["url"] == "/fixtures/nested/page.html")
        self.assertEqual('Quoted "title" and backslash \\', entry["title"])
        self.assertEqual('Summary with "quotes" and a backslash \\', entry["summary"])
        self.assertEqual('keyword "quoted"', entry["keywords"])

    def test_excluded_pages_and_posts_are_not_searchable(self):
        entries = json.loads((self.site / "search.json").read_text())
        titles = {e["title"] for e in entries}
        self.assertNotIn("Excluded fixture", titles)
        self.assertNotIn('Post "title"', titles)
        self.assertTrue(all(e["title"] for e in entries))

    def test_footer_links_work_from_nested_pages(self):
        document = Document((self.site / "fixtures/nested/page.html").read_text())
        self.assertIn("/plugins.html", document.links)
        self.assertIn("/support.html#enterprise-support", document.links)

    def test_firebase_404_output_exists(self):
        page = self.site / "404.html"
        self.assertTrue(page.is_file())
        self.assertIn("Page Not Found", page.read_text())


if __name__ == "__main__":
    unittest.main()
