---
title: "Publishing Gerrit Documentation"
sidebar: gerritdoc_sidebar
permalink: publishing.html
hide_sidebar: true
hide_navtoggle: true
toc: true
---

This topic describes how to publish updates to the Gerrit website.

## Prerequisites

1.  [Install Docker](https://docs.docker.com/install/)
1.  [Install Docker Compose](https://docs.docker.com/compose/install/)
1.  [Prepare your system](https://firebase.google.com/docs/hosting/deploying#section-hosting-setup)
    to host content on Firebase.
1.  Have the appropriate permissions to the Gerrit Code Review project on the
    Google Cloud Platform.

## Cloning the repository

The repository that contains the Gerrit website is called
[homepage](https://gerrit-review.googlesource.com/q/project:homepage).

To clone the repository, run the following command.

```
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

1.  Navigate to the root of the homepage repository.
1.  Type the following command:
    
    ```
    docker-compose up
    ```

The docker file is configured to build the site and serve it on a local staging
server. To access the staging server, navigate to the following URL in your
browser:

```
http://localhost:4000
```

To build the site without staging it, type the following command:

```
docker run -v $(pwd):/site bretfisher/jekyll-serve jekyll build
```

## Deploying the site

**Note:** If this is your first time running Firebase on this machine, you need
to provide authentication credentials. For more information, see
[Appendix: Logging in to Firebase](#appendix-logging-in-to-firebase).

**To deploy the site:**

1.  Make sure you have proper ownership of the output files.

    ```
    sudo chown -R $( id -u $USER ):$( id -g $USER ) _site/
    ```

1.  Type the following command from the root of the repository:

    ```
    firebase deploy
    ```

In a few moments, the site is updated. You can view the deployment in the
Firebase console.

## Rolling back to another deployment

1.  Open the Firebase console.

1.  From the left navigation pane, click **Hosting**.

1.  In Deployment History, select the deployment you'd like to return to.

1.  Click the More button (three vertical dots).

1.  Select **Rollback**.

## Writing content

This section describes how to add new content to the documentation.

**Note:** For complete documentation on the site template and how to create
content, see [Getting started with the Documentation Theme for Jekyll](http://idratherbewriting.com/documentation-theme-jekyll/index.html).

1.  Using the text editor of your choice, create an empty document.

1.  At the top of the document, add the following text block:

    ```
    ---
    title: [TITLE_NAME]
    sidebar: [SIDEBAR_NAME]
    permalink: [FILENAME]
    ---
    ```

    Where:

    *  TITLE_NAME is the title of the topic.
    *  SIDEBAR_NAME is one of the following values:
       *  gerritsidebar: This sidebar is used for most topics.
       *  errors_sidebar: This sidebar is used for error messages.
       *  cmd_sidebar: This sidebar is used for the command reference topics.
       *  restapi_sidebar: This sidebar is used for the REST API reference.
       *  userguide_sidebar: This sidebar is used for the Gerrit User Guide (currently in alpha
    *  FILENAME is the output name of the file. This name MUST be unique.

1.  Author your topic using the Kramdown Markdown.

1.  Save the file in the following directory:

    ```
    path/to/repository/jekyll-source/pages/gerrit
    ```

This template supports a few additional extensions for authoring content. Some
that you might find useful include:

*  [Notes and warnings](http://idratherbewriting.com/documentation-theme-jekyll/mydoc_alerts.html)
*  [Navtabs](http://idratherbewriting.com/documentation-theme-jekyll/mydoc_navtabs.html)

For more information on how the documentation is structured and the syntax it
supports, see the [template documentation](http://idratherbewriting.com/documentation-theme-jekyll/).

## Appendix: Logging in to Firebase

If you have never used Firebase before, you need to perform these steps:

1.  [Install the Firebase CLI](https://firebase.google.com/docs/hosting/quickstart#install-the-firebase-cli).

1.  [Log in to Firebase](https://firebase.google.com/docs/hosting/quickstart#access-your-firebase-projects).

    **Note:** After you provide your credentials, you are returned to http://localhost
    to confirm your authentication. If you cannot access localhost for some reason,
    you can run this command instead: `firebase login --no-localhost`.

1.  [Initialize Firebase](https://firebase.google.com/docs/hosting/quickstart#initialize-your-site).

    **Note:** When you initialize Firebase, specify `_site` as the root
    directory. Accept the defaults for all other options.

## Appendix: Jekyll Template

Jekyll sites use a variety of templates. For Gerrit, we have selected
[this template](http://idratherbewriting.com/documentation-theme-jekyll/). We
chose this template because it has robust support for documentation. For
example, this template supports:

*  A left navigation system that includes sections that can expand and collapse

*  Support for tabs within content, which makes it easier to display multiple
   options for users (for instance, displaying GWT or PolyGerrit instructions)

*  A simple, but extensible Search box

As the theme is already included in the repository for the Gerrit site, you
should not need to install it when making changes to your content. However, to
learn about the template and its features, use the following link:

[http://idratherbewriting.com/documentation-theme-jekyll/](http://idratherbewriting.com/documentation-theme-jekyll/)

