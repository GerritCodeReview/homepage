# Understanding the Gerrit Workflow

Code review is an essential part of the development process. It's where you
learn the _why_ behind a code change, and where you can discuss design decisions
with other members of your team. With Gerrit, you can incorporate code review
into your workflow in a way that's easy to learn, yet robust enough to handle
even the most complex projects.

In this guide, you'll follow a change through the Gerrit workflow. You’ll follow
two developers, Max and Hannah, as they make and review a change to a
`RecipeBook` project.

>  This example uses a Gerrit server configured as follows:
>
>  -  **Hostname**: gerrithost
>  -  **HTTP interface port**: 8080
>  -  **SSH interface port**: 29418
>
> The project and commands used in this section are for demonstration purposes
> only.

## Setting up the environment

Our first developer, Max, has decided to make a change to the `RecipeBook`
project he works on. His first step is to get the source code that he wants to
modify. To get this code, he accesses the Gerrit user interface.

![Gerrit User Interface](/images/intro-gerrit-ui.png)

From here, he clicks **Projects** and then selects **List**. This opens a view
that displays all of the projects Max can access. He types the name of the
project into the **Filter** box to quickly locate it.

![Selecting a Project](/images/intro-select-project.png)

Max clicks on the project, which opens its Project page.

![Gerrit Project Page](/images/intro-clone-project.png)

Notice that this page includes the standard Git command to clone the
repository. Next to this command, however, is the **Clone with commit msg hook**
link. Max clicks this link, which displays a command similar to the following:

```
git clone https://review.gerrithub.io/aikidave/recipe-book && \
(cd recipe-book && curl -kLo `git rev-parse --git-dir`/hooks/commit-msg \
https://review.gerrithub.io/tools/hooks/commit-msg; chmod +x \
`git rev-parse --git-dir`/hooks/commit-msg)
```
&nbsp;
> **The commit msg hook**
>
> The commit msg hook configures this repository to automatically add a
> [Change-Id](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-changeid.html) to commits. This ID allows Gerrit to link
> together different versions of the same change being reviewed.
>
> To learn more about adding a change-id and the commit message hook, see the
> [commit-msg Hook](cmd-hook-commit-msg.html) topic.

Max is ready to make an update to the `recipe-book` project.

## Making the Change
Max decides to add a new recipe for pizza dough to the `recipe-book`
project. He creates a file with the recipe. When he's done, he uses the typical
`git add` and `git commit` commands to add and commit his changes.

```
git add pizza-dough.txt
git commit -m "Add new pizza dough recipe"
```

## Creating the Review

Max’s next step is to push his change to Gerrit so other contributors can review
it. He does this using the `git push origin HEAD:refs/for/master` command, as
follows:

    > git push origin HEAD:refs/for/master
    Counting objects: 3, done.
    Delta compression using up to 12 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 866 bytes | 866.00 KiB/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    remote: Processing changes: new: 1, refs: 1, done
    remote:
    remote: New Changes:
    remote:   https://review.gerrithub.io/380862 Add new pizza dough recipe
    remote:
    To https://review.gerrithub.io/aikidave/recipe-book
     * [new branch]      HEAD -> refs/for/master

Notice the reference to a `refs/for/master` branch. Gerrit uses this branch to
create reviews for the master branch. If Max opted to push to a different
branch, he would have modified his command to `git push origin
HEAD:refs/for/<branch_name>`. Gerrit accepts pushes to `refs/for/<branch_name>`
for every branch that it tracks.

The output of this command also contains a link to a web page Max can use to
review this commit. Clicking on that link takes him to a screen similar to the
following.

![Gerrit Code Review Screen](/images/intro-new-change.png)

This is the Gerrit code review screen, where other contributors can review his
change. Max can also perform tasks such as:

- Looking at the
  [diff](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-review-ui.html#diff-preferences) of his change

- Writing
  [inline](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-review-ui.html#inline-comments) or
  [summary](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-review-ui.html#reply) comments to ask reviewers for advice on
  particular aspects of the change

- [Adding a list of people](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/intro-user.html#adding-reviewers) that should
  review the change

In this case, Max opts to manually add the senior developer on his team, Hannah,
to review his change.

![Add a reviewer to Gerrit](/images/intro-add-reviewer.png)

## Reviewing the Change

Let’s now switch to Hannah, the senior developer who will review Max’s change.

As mentioned previously, Max chose to manually add Hannah as a reviewer. Gerrit
offers other ways for reviewers to find changes, including:

- Using the
  [search](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-search.html) feature that to find changes

- Selecting **Open** from the **Changes** menu

- Setting up [email notifications](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-notify.html) to stay informed of
  changes even if you are not added as a reviewer

Because Max added Hannah as a reviewer, she receives an email telling her about
his change. She opens up the Gerrit code review screen and selects Max’s change.
She notices that, below the section that displays information about the owner,
reviewer, and other elements of the change, there are two messages:

    * Verified
    * Code Review

These two lines indicate what checks the change must pass before it is
accepted. The default Gerrit workflow requires two checks:

-   **Verified**. This check means that the code actually compiles, passes any
    unit tests, and performs as expected.

-   **Code-Review**. This check requires that someone look at the code and
    ensures that it meets project guidelines, styles, and other criteria.

In general, the **Verified** check is done by an automated build server, through
a mechanism such as the
[Gerrit Trigger Jenkins Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Gerrit+Trigger),
while the **Code-Review** check requires an individual to look at the
code.

> **Important**
>
> The Code-Review and Verified checks require different permissions in Gerrit.
> This requirement allows teams to separate these tasks. For example, an
> automated process can have the rights to verify a change, but not perform a
> code review.

With the code review screen open, Hannah can begin to review Max’s change. She
can choose one of two ways to review the change: unified or side-by-side. Both
views allow her to perform tasks such as add
[inline](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-review-ui.html#inline-comments) or
[summary](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-review-ui.html#reply) comments.

Hannah reviews the change and is ready to provide her feedback. She clicks the
**Reply** button on the change screen. This allows her to vote on the change.

![Reviewing the Change](/images/intro-review-change.png)

For Hannah and Max’s team, a code review vote is a numerical score between -2
and 2. The possible options are:

-   +2 Looks good to me, approved

-   +1 Looks good to me, but someone else must approve

-   0 No score

-   -1 I would prefer that you didn't submit this

-   -2 Do not submit

In addition, a change must have at least one `+2` vote and no `-2` votes before
it can be submitted. These numerical values do not accumulate. Two `+1` votes do
not equate to a `+2`.

> **Note**
>
> These settings are enabled by default. To learn about how to customize them
> for your own workflow, see the [Project Configuration File
> Format](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/config-project-config.html) topic.

Hannah notices a possible issue with Max’s change, so she selects a `-1` vote.
She uses the text box to provide Max with some additional feedback. When she is
satisfied with her review, Hannah clicks the **Post** button. At this point, her
vote and message become visible to all users.

## Reworking the Change

Later in the day, Max decides to check on his change and notices Hannah’s
feedback.

![Comment in change](/images/intro-comment.png)

He clicks the file to open the Change view so he can see the comment inline.

![Displaying a comment](/images/intro-comment-display.png)

He opens up the source file and incorporates her feedback. Because
Max’s change includes a change-id, all he has to amend his existing commit and
push it to Gerrit:

    > git commit --amend
    > git push origin HEAD:refs/for/master
    Counting objects: 5, done.
    Delta compression using up to 8 threads.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (3/3), 546 bytes, done.
    Total 3 (delta 0), reused 0 (delta 0)
    remote: Processing changes: updated: 1, done
    remote:
    remote: Updated Changes:
    remote:   http://gerrithost:8080/68
    remote:
    To ssh://gerrithost:29418/RecipeBook.git
     * [new branch]      HEAD -> refs/for/master

Notice that the output of this command is slightly different from Max’s first
commit. This time, the output verifies that the change was updated.

Having uploaded the reworked commit, Max can go back to the Gerrit web interface
and look at his change.

This time, the Change view has a few updates. First, the **Patch Set** dropdown
list displays all of the different updates Max has made since he first started
work on this commit. Second, the **Diff against** drop down list shows multiple
patch sets, allowing anyone who views the change to compare the commit at any
stage. Max can also open the `pizza-dough.txt` file and compare different patch
sets to each other. These options allow Max, Hannah and any other developer to
track a change not just against the original file, but at any point during the
development process.

Max clicks **Reply** and thanks Hannah for her feedback. When Hannah next looks
at Max’s change, she sees that he incorporated her feedback. The change looks
good to her, so she changes her vote to a `+2`.

## Verifying the Change

Hannah’s `+2` vote means that Max’s change satisfies the **Code Review** check.
It has to pass one more check before it can be accepted: the **Verified** check.

The Verified check means that the change was confirmed to work. This type of
check typically involves tasks such as ensuring that the code compiles, unit
tests pass, and so on. You can configure a Verified check to consist of
as many or as few tasks as needed.

> **Manually verifying changes**
>
> Verification is typically an automated process using the
> [Gerrit Trigger Jenkins Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Gerrit+Trigger)
>  or a similar mechanism. However, there are still times when a change requires
> manual verification. For example a reviewer might want to check how or if a
> change works.
>
> To accommodate these and other situations, Gerrit exposes each change as a git
> branch. Click the
> [**download**](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/user-review-us.html#download)
> link in the Change screen to fetch a branch for a specific change.
>
> Manual verification requires a developer with specific access privileges. This
> allows organizations to control if a reviewer can verify a change, or if a
> different person should. See the [Verified Label](https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/config-labels.html#label_Verified)
> to learn more.

Hannah has the appropriate permissions to verify changes, so she again clicks
the **Reply** button. Unlike the code review check, Hannah can provide only
a score of either `+1` or `-1`.

> **Note**
>
> A change must have at least one `+1` and no -1`.

Hannah selects a `+1` for her verified check. Max’s change is now ready to be
submitted.

## Submitting the Change

Max is ready to submit his change. He opens up the change in the Code Review
screen and clicks the **Submit** button.

![Change Ready for Submit](/images/intro-submit.png)

At this point, Max’s change becomes an official part of the repository.

## Next Steps

This walkthrough provided a quick overview of how a change moves through the
default Gerrit workflow. At this point, you can:

- Try the [Hello, Gerrit](/hello-gerrit.md) tutorial and experience Gerrit for yourself.

- Read the [Users guide](https://https://gerrit-documentation.storage.googleapis.com/Documentation/2.15/intro-user.html)
  to get a better sense of how to make changes using Gerrit

