---
title: "Gerrit Code Review"
sidebar: gerritdoc_sidebar
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
                    <a href="intro-gerrit-walkthrough.html" class="btn btn-primary">Learn More</a>
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
                    <a href="user-dashboards.html" class="btn btn-primary">Learn More</a>
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
                    <p>with deeply integrated and delagatable access controls.
                    </p>
                    <a href="project-configuration.html" class="btn btn-primary">Learn More</a>
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
                    <b><a href="3.0.html">3.0.1</a></b>
                    </p>
                    <a href="https://gerrit-releases.storage.googleapis.com/gerrit-3.0.1.war" class="btn btn-primary">Download</a>
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

Schedule [git gc](https://gerrit-documentation.storage.googleapis.com/Documentation/3.0.1/config-gerrit.html#gc)
over all managed repositories and
[replicate](https://gerrit.googlesource.com/plugins/replication/+doc/v3.0.1/src/main/resources/Documentation/config.md)
to geographical mirrors for latency reduction and backup servers for hot
spare redundancy.

## Extensible through plugins

Gerrit Code Review can be extended and further customized by installing
[server-side plugins](https://gerrit-documentation.storage.googleapis.com/Documentation/3.0.1/config-plugins.html).
Source code for additional plugins can be found through the
[project listing](https://gerrit.googlesource.com/plugins/).

## Support

The Gerrit open source community actively supports the last 2 releases
on a best effort basis. Older releases are not actively maintained but
may still receive important fixes (e.g. security fixes), but there is
no guarantee for this. Which fixes are backported to these old
releases is decided on a case by case basis.

End of life for old releases happens implicitly when a new Gerrit version
is released, and is not necessarily announced.

For questions write to the mailing list (<a href="https://groups.google.com/group/repo-discuss">repo-discuss on Google Groups</a>),
or check the questions tagged with <a href="https://stackoverflow.com/questions/tagged/gerrit">[gerrit]</a>
on Stack Overflow.

The repo-discuss mailing list is managed to prevent spam posts. This
means posts from new participants must be approved manually before they
appear on the mailing list. Approvals normally happen within 1 work
day. Posts of people that participate in mailing list discussions
frequently are approved automatically.

## Events

Events (e.g. user summits, hackathons) are announced on the
<a href="https://groups.google.com/group/repo-discuss">repo-discuss</a>
mailing list and can be found in the
<a href="https://calendar.google.com/calendar?cid=Z29vZ2xlLmNvbV91YmIxcGxhNmlqNzg1b3FianI2MWg0dmRpc0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t">community calendar</a>.

## Social Media

Follow us on Twitter (<a href="https://twitter.com/gerritreview">@gerritreview</a>).

## Training Slides

The following slides explain Git and Gerrit concepts and workflows and are meant
for self-studying how Git and Gerrit work:

* <a href="https://docs.google.com/presentation/d/1IQCRPHEIX-qKo7QFxsD3V62yhyGA9_5YsYXFOiBpgkk/edit?usp=sharing">Git explained: Git Concepts and Workflows</a>
* <a href="https://docs.google.com/presentation/d/1C73UgQdzZDw0gzpaEqIC6SPujZJhqamyqO1XOHjH-uk/edit?usp=sharing">Gerrit explained: Gerrit Concepts and Workflows</a>

