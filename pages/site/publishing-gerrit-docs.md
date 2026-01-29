---
title: "Publishing Gerrit Documentation"
permalink: publishing.html
hide_sidebar: true
hide_navtoggle: true
toc: true
---

There is a build job `homepage` which automatically updates the plugin page,
generates the homepage and deploys the new version.

The remainder of this topic describes how to manually publish updates to the Gerrit website.

## Prerequisites

1. [Install Docker](https://docs.docker.com/install/)
1. [Install Docker Compose](https://docs.docker.com/compose/install/)
1. [Prepare your system](https://firebase.google.com/docs/hosting/deploying#section-hosting-setup)
   to host content on Firebase.
1. Have the appropriate permissions to the Gerrit Code Review project on the
   Google Cloud Platform.

## Cloning the repository

The repository that contains the Gerrit website is called
[homepage](https://gerrit-review.googlesource.com/q/project:homepage).

To clone the repository, run the following command.

```bash
git clone https://gerrit.googlesource.com/homepage && \
(cd homepage && curl -Lo `git rev-parse --git-dir`/hooks/commit-msg \
https://gerrit-review.googlesource.com/tools/hooks/commit-msg ; \
chmod +x `git rev-parse --git-dir`/hooks/commit-msg)
```

## Building the site

In these steps, you build the site on your local machine.

The output files for the site are stored in the `_site` directory. This
directory is not stored in the repository.

**To build the site:**

1. Navigate to the root of the homepage repository.
1. Type the following command:

    ```bash
    docker compose up
    ```

1. If that command fails, try these, with caution:

    ```bash
    docker compose down && \
    git clean -fdx && \
    docker compose up
    ```

The docker file is configured to build the site and serve it on a local staging
server. To access the staging server, navigate to the following URL in your
browser:

```bash
http://localhost:4000
```

To build the site without staging it, type the following command:

```bash
docker run -v $(pwd):/site bretfisher/jekyll-serve jekyll build
```

## Updating the plugins page

Updating the `plugins.md` file requires to run the `plugins.py`
script. The script depends on the `pygerrit2` library, which can
be installed using the provided `pipenv` environment:

```bash
cd homepage
pipenv install --dev
```

Running `plugins.py` may require using either one of its `-a` or `-n`
options, depending on CI authentication:

```bash
cd homepage
pipenv run python tools/plugins.py
docker compose up
(browse to) http://localhost:4000/plugins.html
```

The resulting `plugins.md` file lends the browsed `plugins.html` page.

If changes are made to the `plugins.py` script, check for coding errors and
style violations with `flake8`, and format the code with `black`:

```bash
pipenv run flake8 tools/plugins.py
pipenv run black tools/plugins.py
```

Both of these tools are also provided in the pipenv environment.

## Deploying the site

**Note:** If this is your first time running Firebase on this machine, you need
to provide authentication credentials. For more information, see
[Appendix: Logging in to Firebase](#appendix-logging-in-to-firebase).

**To deploy the site:**

1. Make sure you have proper ownership of the output files.

    ```bash
    sudo chown -R $( id -u $USER ):$( id -g $USER ) _site/
    ```

1. Type the following command from the root of the repository:

    ```bash
    firebase deploy
    ```

In a few moments, the site is updated. You can view the deployment in the
Firebase console.

## Rolling back to another deployment

1. Open the Firebase console.

1. From the left navigation pane, click **Hosting**.

1. In Deployment History, select the deployment you'd like to return to.

1. Click the More button (three vertical dots).

1. Select **Rollback**.

## Writing content

This section describes how to add new content to the documentation.

**Note:** For complete documentation on the site template and how to create
content, see [Getting started with the Documentation Theme for Jekyll](http://idratherbewriting.com/documentation-theme-jekyll/index.html).

1. Using the text editor of your choice, create an empty document.

1. At the top of the document, add the following text block:

    ```markdown
    ---
    title: [TITLE_NAME]
    permalink: [FILENAME]
    ---
    ```

    Where:

    * TITLE_NAME is the title of the topic.
    * FILENAME is the output name of the file. This name MUST be unique.

1. Author your topic using the Kramdown Markdown.

1. Save the file in the following directory:

    ```bash
    path/to/repository/jekyll-source/pages/gerrit
    ```

This template supports a few additional extensions for authoring content. Some
that you might find useful include:

* [Notes and warnings](http://idratherbewriting.com/documentation-theme-jekyll/mydoc_alerts.html)
* [Navtabs](http://idratherbewriting.com/documentation-theme-jekyll/mydoc_navtabs.html)

For more information on how the documentation is structured and the syntax it
supports, see the [template documentation](http://idratherbewriting.com/documentation-theme-jekyll/).

### Writing blog posts

The Gerrit website supports adding blog posts. Users can view a list of
current blogposts by click the **News** link in the navigation bar.

To create a blog post:

1. Create a new markdown file. The name of the file must use this format:

    ```bash
    YYYY-MM-DD-[permalink].md
    ```

    Where `[permalink]` is a descriptive name of the file and `YYYY-MM-DD` is
    the date that will be shown on the post. Posts will be listed on the index
    in chronological order; posts with a date in the future will not be rendered
    or appear in the index until that date.

1. Add the following to the top of the blog post:

    ```markdown
        ---
        title: [TITLE]
        tags: [TAGS]
        keywords: [KEYWORDS]
        permalink: [FILENAME].html
        summary: [SUMMARY]
        hide_sidebar: true
        hide_navtoggle: true
        toc: true
        ---
    ```

    Where:

    * `[TITLE]` is the title of the blog post
    * `[TAGS]` is an optional space-delimited list of tags
    * `[KEYWORDS]` is an optional space-delimited list of keywords
    * `[FILENAME]` is the name of the file
    * `[SUMMARY]` is a one- to two- sentence description of the post

1. Save the post in the `_posts` directory or the `_drafts` directory.

    For posts to be published immediately, save the new file in the `_posts` directory.

    For posts that are still work in progress, or to be written iteratively by
    multiple authors across several commits, save the new file in the `_drafts`
    directory. When the post is complete, move the file into the `_posts` directory.

1. Save any images in the top-level `images` directory.

## Appendix: Logging in to Firebase

If you have never used Firebase before, you need to perform these steps:

1. [Install the Firebase CLI](https://firebase.google.com/docs/hosting/quickstart#install-the-firebase-cli).

1. [Log in to Firebase](https://firebase.google.com/docs/hosting/quickstart#access-your-firebase-projects).

    **Note:** After you provide your credentials, you are returned to <http://localhost>
    to confirm your authentication. If you cannot access localhost for some reason,
    you can run this command instead: `firebase login --no-localhost`.

1. [Initialize Firebase](https://firebase.google.com/docs/hosting/quickstart#initialize-your-site).

    **Note:** When you initialize Firebase, specify `_site` as the root
    directory. Accept the defaults for all other options.

## Appendix: Jekyll Template

Jekyll sites use a variety of templates. For Gerrit, we have selected
[this template](http://idratherbewriting.com/documentation-theme-jekyll/). We
chose this template because it has robust support for documentation. For
example, this template supports:

* A left navigation system that includes sections that can expand and collapse

* Support for tabs within content, which makes it easier to display multiple
  options for users (for instance, displaying GWT or PolyGerrit instructions)

* A simple, but extensible Search box

As the theme is already included in the repository for the Gerrit site, you
should not need to install it when making changes to your content. However, to
learn about the template and its features, use the following link:

[http://idratherbewriting.com/documentation-theme-jekyll/](http://idratherbewriting.com/documentation-theme-jekyll/)
