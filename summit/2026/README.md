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

Output is written to `_site/`. This is a standalone build, independent of the
main `gerritcodereview.com` site's build.

## Local preview

Build with relative paths so you can open the HTML files directly:

```sh
cd summit/2026
bundle exec jekyll build --config _config.yml,_config_local.yml
```

Then open `_site/index.html` directly in a browser.
