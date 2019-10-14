---
title: "Gerrit Code Review"
sidebar: gerritdoc_sidebar
permalink: index.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Gerrit Code Review

Gerrit is a Git based Code Review and Workflow server. You can see it in action [here](https://gerrit-review.googlesource.com/q/status:open+project:gerrit) where it is used to manage the Gerrit code base itself.

<div class="row">
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
                    <b><a href="3.0.html">3.0.3</a></b>
                    </p>
                    <a href="https://gerrit-releases.storage.googleapis.com/gerrit-3.0.3.war" class="btn btn-primary">Download</a>
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

Schedule [git gc](https://gerrit-documentation.storage.googleapis.com/Documentation/3.0.3/config-gerrit.html#gc)
over all managed repositories and
[replicate](https://gerrit.googlesource.com/plugins/replication/+doc/v3.0.3/src/main/resources/Documentation/config.md)
to geographical mirrors for latency reduction and backup servers for hot
spare redundancy.

## Extensible through plugins

Gerrit Code Review can be extended and further customized by installing
[server-side plugins](https://gerrit-documentation.storage.googleapis.com/Documentation/3.0.3/config-plugins.html).
Source code for additional plugins can be found through the
[project listing](https://gerrit.googlesource.com/plugins/).


## Community

[Members](https://www.gerritcodereview.com/members.html) of the Gerrit community are expected to behave within the guidelines of the community's [Code Of Conduct](https://www.gerritcodereview.com/codeofconduct.html) when representing the community.  We would like to [praise](https://www.gerritcodereview.com/kudos.html) some of the more recent accomplishements from the community.

Members of the community will discuss most Gerrit related things on the [repo-discuss](https://groups.google.com/group/repo-discuss) mailing list. Events such as user summits and hackathons are announced there. You can also see the events posted on our [Calendar](https://calendar.google.com/calendar?cid=Z29vZ2xlLmNvbV91YmIxcGxhNmlqNzg1b3FianI2MWg0dmRpc0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t">community calendar), or if you prefer to follow us on [Twitter@gerritreview](https://twitter.com/gerritreview).  For a more real-time Gerrit discussion, see our [Slack channel](https://gerritcodereview.slack.com/)

Please refer to the [support](support.html) page for more details.

## Training Slides

The following slides explain Git and Gerrit concepts and workflows and are meant
for self-studying how Git and Gerrit work:

* <a href="https://docs.google.com/presentation/d/1IQCRPHEIX-qKo7QFxsD3V62yhyGA9_5YsYXFOiBpgkk/edit?usp=sharing">Git explained: Git Concepts and Workflows</a>
* <a href="https://docs.google.com/presentation/d/1C73UgQdzZDw0gzpaEqIC6SPujZJhqamyqO1XOHjH-uk/edit?usp=sharing">Gerrit explained: Gerrit Concepts and Workflows</a>

