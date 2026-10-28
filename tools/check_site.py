#!/usr/bin/env python3
"""Validate a fresh Jekyll output without network access or third-party packages."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit


ORIGIN = "https://www.gerritcodereview.com"
HOSTS = {"www.gerritcodereview.com", "gerritcodereview.com"}
REQUIRED = (
    "index.html",
    "404.html",
    "releases-readme.html",
    "plugins.html",
    "assets/css/style.css",
    "js/jekyll-search.js",
    "js/toc.js",
    "js/heading-anchors.js",
    "images/gerrit-logo.svg",
    "search.json",
)
FORBIDDEN = (
    "tests",
    "tools",
    "node_modules",
    "test-results",
    "playwright-report",
    "package.json",
    "package-lock.json",
    "playwright.config.js",
    "Jenkinsfile",
    "Pipfile",
    "Pipfile.lock",
    "AGENTS.md",
)


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for attribute in ("href", "src", "poster"):
            if attrs.get(attribute):
                self.links.append(attrs[attribute])
        # This site's srcsets use ordinary URLs, not data URLs containing commas.
        if attrs.get("srcset"):
            self.links.extend(
                item.strip().split()[0]
                for item in attrs["srcset"].split(",")
                if item.strip()
            )


class SiteChecker:
    def __init__(self, site, required=REQUIRED, redirects=None, exceptions=()):
        self.site = Path(site).resolve()
        self.required = required
        self.redirects = redirects or {}
        self.exceptions = {
            (item["source"], item["url"]): item["reason"] for item in exceptions
        }
        self.documents = {}

    def link_error(self, source, url):
        if not url or url == "#":
            return None
        parsed = urlsplit(urljoin(f"{ORIGIN}/{source}", url))
        if parsed.scheme not in ("http", "https") or parsed.hostname not in HOSTS:
            return None
        seen = set()
        while parsed.path in self.redirects:
            if parsed.path in seen:
                return "redirect cycle"
            seen.add(parsed.path)
            destination = self.redirects[parsed.path]
            if "#" not in destination and parsed.fragment:
                destination += "#" + parsed.fragment
            parsed = urlsplit(urljoin(ORIGIN, destination))
            if parsed.hostname not in HOSTS:
                return None
        target = self.site / unquote(parsed.path).lstrip("/")
        if not target.resolve().is_relative_to(self.site):
            return "path escapes site output"
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            return "missing target"
        if parsed.fragment and target.suffix == ".html":
            relative = target.relative_to(self.site).as_posix()
            if relative not in self.documents:
                self.documents[relative] = Document(target.read_text(encoding="utf-8"))
            if unquote(parsed.fragment) not in self.documents[relative].ids:
                return "missing fragment"
        return None

    def check(self):
        errors = []
        used_exceptions = set()
        for name in self.required:
            if (
                not (self.site / name).is_file()
                or not (self.site / name).stat().st_size
            ):
                errors.append(f"missing required output: {name}")
        for name in FORBIDDEN:
            if (self.site / name).exists():
                errors.append(f"test/tooling output must not be deployed: {name}")
        for path in sorted(self.site.rglob("*.html")):
            source = path.relative_to(self.site).as_posix()
            document = Document(path.read_text(encoding="utf-8"))
            self.documents[source] = document
            for url in sorted(set(document.links)):
                error = self.link_error(source, url)
                if error:
                    key = (source, url)
                    if key in self.exceptions:
                        used_exceptions.add(key)
                    else:
                        errors.append(f"{source}: {url}: {error}")
        for source, url in sorted(self.exceptions.keys() - used_exceptions):
            errors.append(f"unused link exception: {source}: {url}")
        search = self.site / "search.json"
        try:
            entries = json.loads(search.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            errors.append(f"invalid search JSON: {error}")
            return errors
        if not isinstance(entries, list):
            errors.append("search JSON must be an array")
            return errors
        for index, entry in enumerate(entries):
            fields = ("title", "url", "tags", "keywords", "summary")
            if not isinstance(entry, dict) or any(
                not isinstance(entry.get(f), str) for f in fields
            ):
                errors.append(f"search entry {index}: requires string fields {fields}")
                continue
            if not entry["title"] or not entry["url"]:
                errors.append(f"search entry {index}: empty title or URL")
                continue
            parsed = urlsplit(urljoin(ORIGIN + "/", entry["url"]))
            if parsed.hostname not in HOSTS or parsed.scheme not in ("http", "https"):
                errors.append(f"search entry {index}: URL must point to this site")
                continue
            error = self.link_error("index.html", entry["url"])
            if error:
                errors.append(f"search entry {index}: {entry['url']}: {error}")
        return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", default="_site")
    parser.add_argument("--firebase", default="firebase.json")
    parser.add_argument("--exceptions", default="tests/link-exceptions.json")
    options = parser.parse_args()
    try:
        hosting = json.loads(Path(options.firebase).read_text())["hosting"]
        redirects = {
            item["source"]: item["destination"] for item in hosting.get("redirects", [])
        }
        exceptions = json.loads(Path(options.exceptions).read_text())
        if any(not item.get("reason") for item in exceptions):
            raise ValueError("link exceptions require a reason")
        errors = SiteChecker(
            options.site, redirects=redirects, exceptions=exceptions
        ).check()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Cannot validate site: {error}", file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"Site validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("Site validation passed (outputs, internal links/assets, search JSON)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
