#!/usr/bin/env python3
"""Stage a controlled Jekyll source at _test/source, never in production pages."""

from pathlib import Path
import shutil


def main():
    root = Path(__file__).resolve().parent.parent
    source = root / "_test" / "source"
    # Remove only our generated fixture source; no repository content is cleaned.
    if source.exists():
        shutil.rmtree(source)
    source.mkdir(parents=True)
    for name in ("_layouts", "_includes", "_data", "assets", "js", "images"):
        shutil.copytree(root / name, source / name)
    shutil.copy2(root / "_config.yml", source / "_config.yml")
    shutil.copy2(root / "search.json", source / "search.json")
    shutil.copy2(root / "404.md", source / "404.md")
    for fixture in (root / "tests" / "fixtures").glob("*.md"):
        if fixture.name == "post.md":
            posts = source / "_posts"
            posts.mkdir()
            shutil.copy2(fixture, posts / "2020-01-01-excluded.md")
        else:
            shutil.copy2(fixture, source / fixture.name)
    print("Prepared _test/source; build with destination _test/site")


if __name__ == "__main__":
    main()
