import argparse
import getpass
import os
import re
import requests

from jinja2 import Template
from pygerrit2 import GerritRestAPI, HTTPBasicAuth, HTTPBasicAuthFromNetrc


def authenticate():
    username = os.environ.get("username")
    password = os.environ.get("password")
    while not username:
        username = input("user: ")
    while not password:
        password = getpass.getpass("password: ")
    auth = HTTPBasicAuth(username, password)
    return auth


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "-n",
    "--netrc",
    dest="netrc",
    action="store_true",
    help="use credentials from .netrc",
)
options = parser.parse_args()

url = "https://gerrit-review.googlesource.com"
if options.netrc:
    auth = HTTPBasicAuthFromNetrc(url=url)
else:
    auth = authenticate()

api = GerritRestAPI(url=url, auth=auth)

plugins = api.get("/projects/?p=plugins%2f&d")

header = "|Name|State|Changes (last 3 months)|Description|Maintainers"
dashes = "|----|-----|-----------------------|-----------|---"
spacer = "|    |     |                       |           |   "

branches = ["master"] + ["stable-%s" % version for version in ["3.1", "3.0", "2.16"]]

checkMark = "&#x2714;"
unicodeSquare = "&#x20DE;"
greenCheckMark = "&#x2705;"
lock = "&#x1F512;"
redCross = "&#x274C;"


def getBranches(pluginId):
    branchList = api.get("/projects/%s/branches/" % pluginId)
    pluginBranches = []
    for b in branchList:
        if b["ref"].startswith("refs/heads/"):
            ref = b["ref"]
            pluginBranches += [ref[len("refs/heads/") :]]
    return pluginBranches


def getBranchResults(pluginId, pluginName, builds):
    pluginBranches = getBranches(pluginId)
    results = ""
    for branch in branches:
        string = r"^plugin-%s[\w|-]*-%s$" % (pluginName, branch)
        pattern = re.compile(string)
        result = unicodeSquare

        for job in builds["jobs"]:
            if pattern.match(job["name"]):
                result = job["lastBuild"]["result"]
                result = greenCheckMark if result == "SUCCESS" else redCross
                break

        if branch in pluginBranches:
            result = checkMark + "|" + result
        else:
            result = "%s|%s" % (unicodeSquare, result)
        results = result if not results else "%s|%s" % (results, result)
    return results


def getRecentChangesCount(pluginName):
    changes = api.get("/changes/?q=project:%s+-age:3months" % pluginName)
    return len(changes)


def getOwnerNames(pluginName):
    groups = api.get("/groups/?query=name:plugins-%s" % pluginName)
    if len(groups) > 0:
        ownerGroup = groups[0]
        id = ownerGroup.get("id")
        owners = api.get("/groups/%s/members/" % id)
        names = [o.get("name") for o in owners]
        names = ", ".join(names)
    else:
        names = ""
    return names


data = {"permalink": "plugins"}

template_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "plugins.md.template"
)
template = Template(open(template_path).read())
rendered_template = template.render(data=data)

with open("pages/site/plugins/plugins.md", "w") as output:
    output.writelines(rendered_template)

    output.write("\n")
    for b in branches:
        output.write(
            "[%s]: https://gerrit-ci.gerritforge.com/view/Plugins-%s/\n" % (b, b)
        )

    for branch in branches:
        header += "|Branch|CI"
        dashes += "|-----:|--"
        spacer += "|[%s]|" % branch
    output.write("\n%s|\n%s|\n%s|\n" % (header, dashes, spacer))

    url = (
        "https://gerrit-ci.gerritforge.com/api/json?pretty=true&tree=jobs"
        + "[name,lastBuild[result]]"
    )
    builds = requests.get(url).json()
    links = "\n"
    for p in plugins:
        name = p[len("plugins/") :]
        plugin = plugins[p]

        if plugin["state"] == "ACTIVE":
            state = greenCheckMark
            changes = getRecentChangesCount(p)
            availableBranches = getBranchResults(plugin["id"], name, builds)
        else:
            state = lock
            changes = 0
            availableBranches = "|".join(
                ["%s|%s" % (unicodeSquare, unicodeSquare) for b in branches]
            )

        if "description" in plugin:
            description = plugin["description"].split("\n")[0].rstrip(r"\.")
        else:
            description = unicodeSquare

        owners = getOwnerNames(name)

        line = "|[%s]|%s|%d|%s|%s|%s|\n" % (
            name,
            state,
            changes,
            description,
            owners,
            availableBranches,
        )
        output.write(line)
        links += "[%s]: https://gerrit.googlesource.com/plugins/%s\n" % (name, name)

    output.write(links)
