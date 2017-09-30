# Hello, Gerrit
Often, the best way to learn something is to try it out yourself. In this short
tutorial, you'll install Gerrit and add a repository to it. While this
installation isn't intended for a production environment, it does allow you to
explore Gerrit and test how its capabilities can benefit your development
workflow.

## Before you begin

To complete this quickstart, you need:

1.  A machine running Linux.

2.  Java SE Runtime Environment version 1.8 or later.

## Download Gerrit

From the Linux machine on which you want to install Gerrit:

1. Open a terminal window.

2. Download the Gerrit archive. See
   [Gerrit Code Review- Releases](https://gerrit-releases.storage.googleapis.com/index.html) for a
   list of available archives.

The steps in this quickstart used Gerrrit 2.15, which you can download using a
command such as:

    wget https://www.gerritcodereview.com/download/gerrit-2.15.war

## Install and initialize Gerrit

From the command line, type the following:

    java -jar gerrit-2.15.war init --batch --dev -d ~/gerrit_testsite

The preceding command uses two parameters:

- **--batch**. This parameter assigns default values to a variety of Gerrit
  configuration options. To learn more about these configuration options, see
  [Configuration](config-gerrit.html).

- **--dev**. This parameter configures the server to use the authentication
  option, `DEVELOPMENT_BECOME_ANY_ACCOUNT`. This authentication type makes it
  easy for you to switch between different users to explore how Gerrit works.
  To learn more about setting up Gerrit for development, see [Developer Setup](dev-readme.html).

This command displays a number of messages in the terminal window. The following
is an example of these messages:

    Generating SSH host key ... rsa(simple)... done
    Initialized /home/gerrit/gerrit_testsite
    Executing /home/gerrit/gerrit_testsite/bin/gerrit.sh start
    Starting Gerrit Code Review: OK

The last message you should see is `Starting Gerrit Code Review: OK`. This
message informs you that the Gerrit service is running. If any settings changes
are made, the server must be restarted before they will take effect.

      gerrit@host:~$ ~/gerrit_testsite/bin/gerrit.sh restart
      Stopping Gerrit Code Review: OK
      Starting Gerrit Code Review: OK
      gerrit@host:~$

The server can be also stopped and started by passing the `stop` and `start`
commands to gerrit.sh.

      gerrit@host:~$ ~/gerrit_testsite/bin/gerrit.sh stop
      Stopping Gerrit Code Review: OK
      gerrit@host:~$
      gerrit@host:~$ ~/gerrit_testsite/bin/gerrit.sh start
      Starting Gerrit Code Review: OK
      gerrit@host:~$

# Update the listening URL

Next, let's update the URL that Gerrit listens to from * to localhost. This
change helps prevent outside connections from contacting the instance.

```
git config --file gerrit_testsite/etc/gerrit.config httpd.listenUrl 'http://localhost:8080'
```

Restart your server for the change to take effect.

```
sh gerrit_testsite/bin/gerrit.sh restart
```

You can verify that the URL is updated by opening a browser window and
navigating to http://localhost:8080. The main Gerrit screen should appear.

# Create a user with admin privileges

With Gerrit up and running, the next step is to create a user. By default, the
first user you create for Gerrit has administrative privileges.

**To create a user**

1. Open the Gerrit user interface. To do this, open a browser and navigate to
   `http://localhost:8080`.
2. In the upper right corner, click the **Become** link.
   The login screen appears.
3. Click **New Account**.
4. Type a name in the **Full Name** box and then click **Save Changes**.
5. Type a user name in the **Username** box and click **Select Username**.
   In the dialog box that appears, click **Ok**.
6. Scroll to the bottom of the screen and click the **Continue** link.

Notice that there are several fields for configuring SSH keys. You will not use
SSH keys for this walkthrough.

Gerrit automatically signs you in as the new user. Before continuing to the next
step, retrieve the HTTP password for the account.

**To retreive the HTTP password**

1. Open the dropdown list next to the user name, located in the upper right
   corner.
2. Click **Settings**.
   The Account Settings screen appears.
3. Click **HTTP Password**.
4. Click **Generate Password**.
5. Copy the password to a file or some other location.

# Create a project

With a user account, you can now create a demo project.

**To create a demo project**

1. From the main Gerrit screen, click **Projects** and then click
   **Create New Project**.
   The Create Project screen appears.
2. Type a name for the project in the **Project Name** box.
3. Enable the **Create initial empty commit** checkbox.
4. Click **Create Project**.
   The Project Settings screen appears.
5. Type a description for the project in the **Description** box.
6. Leave the rest of the options at their default settings, and click
   **Save Changes**.

# Clone the repository and add a commit-msg hook

In this step, you clone the repository and make a change to it. You also add a
commit-msg hook. This hook configures this repository to automatically add a
[Change-Id](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-changeid.html)
to commits. This ID allows Gerrit to link together different versions of the
same change being reviewed.

To learn more about adding a change-id and the commit message hook, see the
[commit-msg Hook](cmd-hook-commit-msg.html) topic.


1. Clone the repository.
      > git clone http://[USER]@localhost:8080/[PROJECT-NAME]
2. Add the commit-msg hook. This hook adds a Change-Id to each change, which
   allows Gerrit to group multiple commits together.
      > curl -Lo ~/[PROJECT-NAME]/.git/hooks/commit-msg  http://localhost:8080/tools/hooks/commit-msg
3. Update the permissions for the commit-msg hook.
      > chmod u+x ~/demo/.git/hooks/commit-msg

# Make a change to the repository

1. Navigate to the project directory.
      > cd [PROJECT-NAME]
2. Make a change to the project.
      > echo "Hello, Gerrit" > hellogerrit.txt
3. Add the file.
      > git add hellogerrit.txt
4. Commit the change.
      > git commit -m "Add Hello Gerrit file"

# Push the change to Gerrit

A normal `git push` command pushes the commit to a specific branch. With Gerrit,
the process is slightly different. Gerrit uses a `refs/for/[BRANCH]` syntax.
This syntax directs the change to Gerrit.

```
git push origin HEAD:refs/for/master
```
## View the change in Gerrit

Return to the main Gerrit screen at `http://localhost:8080`. Under the **Your**
dropdown list, select **Changes**. You should see the change you just created.
Click on the change to open it.

# Next steps

You now have a fully-functional demo install of Gerrit. Here are some options
for your next steps:

* Review the [User's Guide]() to learn more about how to make and review
  changes.

* If you're interested in how to install a production-ready version of Gerrit,
  take a look at the [Installation Guide](). The steps are very similar to the
  ones you followed here, but cover important aspects such as SSH authentication
  in more detail.

