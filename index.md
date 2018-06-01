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
                    <b><a href="https://www.gerritcodereview.com/releases/2.15.md">2.15.1</a></b>
                    </p>
                    <a href="https://gerrit-releases.storage.googleapis.com/gerrit-2.15.1.war" class="btn btn-primary">Download</a>
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

Schedule [git gc] over all managed repositories and [replicate] to
geographical mirrors for latency reduction and backup servers for hot
spare redundancy.

## Extensible through plugins

Gerrit Code Review can be extended and further customized by installing
[server-side plugins][plugins]. Source code for additional plugins
can be found through the [project listing](https://gerrit.googlesource.com/plugins/).

## Get in touch

<table>
<tr>
<td>
<h3>Mailing list</h3>
</td>
<td>
<h3>Social media</h3>
</td>
<td>
<h3>IRC</h3>
</td>
</tr>
<tr>
<td>
<a href="https://groups.google.com/group/repo-discuss">Repo Discuss</a>
</td>
<td>
<a href="https://plus.google.com/communities/111271594706618791655">Google+</a>
<br>
<a href="https://twitter.com/gerritreview">Twitter</a>
</td>
<td>
<a href="https://freenode.net">freenode</a> #gerrit
<br>
<a href="https://echelog.com/logs/browse/gerrit/">Channel log</a>
</td>
</tr>
</table>

