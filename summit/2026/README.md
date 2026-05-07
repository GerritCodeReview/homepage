# Gerrit User Summit 2026 — Site

Static site for the Gerrit User Summit 2026 (November 9-10, Sunnyvale CA).

This is a standalone Jekyll sub-site. It builds independently from the main
`gerritcodereview.com` site and is served at `/summit26/`.

## Prerequisites

Ruby and Bundler are required. Install dependencies once from this directory:

```sh
cd summit/2026
gem install bundler
bundle install
```

## Build

```sh
bundle exec jekyll build
```

Output is written to `_site/`. When the main site is built, its Jekyll config
preserves this output via `keep_files: [summit26]`.

## Local preview

```sh
bundle exec jekyll serve
```

Then open `http://localhost:4000/summit26/` in a browser.
