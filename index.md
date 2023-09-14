---
title: "Gerrit Code Review"
permalink: index.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---
<div class="row">
        <div class="col-md-3 col-sm-6">
            <div class="panel panel-default text-center">
                <div class="panel-heading">
                    <span class="fa-stack fa-5x">
                          <i class="fa fa-circle fa-stack-2x text-primary"></i>
                          <i class="fa fa-comments fa-stack-1x fa-inverse"></i>
                    </span>
                </div>
                <div class="panel-body">
                    <h4>Discuss code</h4>
                    <p>and boost your team's code fu by talking about
                    specifics.</p>
                    <a href="https://gerrit-review.googlesource.com/Documentation/intro-gerrit-walkthrough.html"
                       class="btn btn-primary">Learn More</a>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="panel panel-default text-center">
                <div class="panel-heading">
                    <span class="fa-stack fa-5x">
                          <i class="fa fa-circle fa-stack-2x text-primary"></i>
                          <i class="fa fa-code-fork fa-stack-1x fa-inverse"></i>
                    </span>
                </div>
                <div class="panel-body">
                    <h4>Serve Git</h4>
                    <p>As an integrated experience within the larger code
                    review flow.</p>
                    <a href="https://gerrit-review.googlesource.com/Documentation/user-dashboards.html"
                       class="btn btn-primary">Learn More</a>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="panel panel-default text-center">
                <div class="panel-heading">
                    <span class="fa-stack fa-5x">
                          <i class="fa fa-circle fa-stack-2x text-primary"></i>
                          <i class="fa fa-lock fa-stack-1x fa-inverse"></i>
                    </span>
                </div>
                <div class="panel-body">
                    <h4>Manage workflows</h4>
                    <p>with deeply integrated and delegatable access controls.
                    </p>
                    <a href="https://gerrit-review.googlesource.com/Documentation/project-configuration.html"
                       class="btn btn-primary">Learn More</a>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="panel panel-default text-center">
                <div class="panel-heading">
                    <span class="fa-stack fa-5x">
                          <i class="fa fa-circle fa-stack-2x text-primary"></i>
                          <i class="fa fa-download fa-stack-1x fa-inverse"></i>
                    </span>
                </div>
                <div class="panel-body">
                    <h4>Download</h4>
                    <p>Our latest release is:<br>
                    <b><a href="3.8.html">3.8.2</a></b>
                    </p>
                    <a href="https://gerrit-releases.storage.googleapis.com/gerrit-3.8.2.war" class="btn btn-primary">Download</a>
                </div>
            </div>
        </div>
    </div>

## Discuss code
Read old and new versions of files with syntax highlighting and colored
differences. Discuss specific sections with others to make the right changes.

<img src="images/sbs.png">

## Manage and serve Git repositories

Gerrit includes Git-enabled SSH and HTTPS servers compatible with all
Git clients.  Simplify management by hosting many Git repositories
together.

<table>
<tr>
 <td>
 <h4>Navigate projects</h4>
 </td>
 <td>
 <h4>Control access</h4>
 </td>
 <td>
 <h4>Update branches</h4>
 </td>
</tr>
<tr>
 <td>
 <img src="images/project-list.png">
 </td>
 <td>
 <img src="images/access.png">
 </td>
 <td>
 <img src="images/branches.png">
 </td>
</tr>
</table>

Schedule [git gc](https://gerrit-documentation.storage.googleapis.com/Documentation/3.6.0/config-gerrit.html#gc)
over all managed repositories and
[replicate](https://gerrit.googlesource.com/plugins/replication/+doc/v3.6.0/src/main/resources/Documentation/config.md)
to geographical mirrors for latency reduction and backup servers for hot
spare redundancy.w

## Extensible through plugins

Gerrit Code Review can be extended and further customized by installing
[server-side plugins](https://gerrit-documentation.storage.googleapis.com/Documentation/3.6.0/config-plugins.html).
Source code for additional plugins can be found through the
[project listing](https://gerrit.googlesource.com/plugins/).

## Community

[Members](https://www.gerritcodereview.com/members.html) of the Gerrit community are expected to behave within the guidelines of the community's [Code Of Conduct](https://www.gerritcodereview.com/codeofconduct.html) when representing the community.  We would like to [praise](https://www.gerritcodereview.com/kudos.html) some of the more recent accomplishements from the community.

Members of the community will discuss most Gerrit related things on the [repo-discuss](https://groups.google.com/group/repo-discuss) mailing list. For a more real-time Gerrit discussion you may also join our [Discord server](https://discord.gg/HkGbBJHYbY).

Events such as user summits and hackathons are announced on the [repo-discuss](https://groups.google.com/group/repo-discuss) mailing list. You can also see the events posted on our [Calendar](https://calendar.google.com/calendar?cid=Z29vZ2xlLmNvbV91YmIxcGxhNmlqNzg1b3FianI2MWg0dmRpc0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t), or if you prefer to follow us on [Twitter@gerritreview](https://twitter.com/gerritreview).

For face-to-face discussions there is a monthly Gerrit community meeting (monthly on the first Thursday from 5pm to 6pm CET, join the meeting [here](https://meet.google.com/kue-ysnz-yme)). Everyone is welcome to join and bring up things they like to discuss. The agenda is completely open, but topics may be added beforehand to the [agenda](https://docs.google.com/document/d/1QmrIsyBx52Sk_qWwrcci0hI_SlUWMGiwT8Kp05_ioBw/edit?usp=sharing). Please always prefix topics with your name in square brackets, so that it's clear who added which topic.

## Support

Please refer to the [support](support.html) page for more details.

## Training Slides

These have been moved to the [Presentations](https://www.gerritcodereview.com/presentations.html)
page under Community. More presentations are made available there as well.
