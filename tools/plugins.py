from __future__ import print_function
import argparse
import getpass
import os
import re
import requests
import sys
import time

from jinja2 import Template
from pygerrit2 import GerritRestAPI, HTTPBasicAuth, HTTPBasicAuthFromNetrc, Anonymous
from tqdm import tqdm


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
group = parser.add_mutually_exclusive_group()

group.add_argument(
    "-n",
    "--netrc",
    dest="netrc",
    action="store_true",
    help="use credentials from .netrc",
)
group.add_argument(
    "-a",
    "--anonymous",
    dest="anonymous",
    action="store_true",
    help="use anonymous access, i.e. no credentials",
)
options = parser.parse_args()

url = "https://gerrit-review.googlesource.com"
if options.netrc:
    auth = HTTPBasicAuthFromNetrc(url=url)
elif options.anonymous:
    auth = Anonymous()
else:
    auth = authenticate()

api = GerritRestAPI(url=url, auth=auth)

plugins = api.get("/projects/?p=plugins%2f&d")

header = "|Name|State|Repo|Changes (last 3 months/all)|Description|Maintainers"
dashes = "|----|-----|----|---------------------------|-----------|---"
spacer = "|    |     |    |                           |           |   "

branches = ["master"] + [f"stable-{version}" for version in ["3.1", "3.0", "2.16"]]

checkMark = "&#x2714;"
greenCheckMark = "&#x2705;"
lock = "&#x1F512;"
redCross = "&#x274C;"
unicodeSquare = "&#x20DE;"


def getBranches(pluginId):
    branchList = api.get(f"/projects/{pluginId}/branches/")
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
        string = fr"^plugin-{pluginName}[\w|-]*-{branch}$"
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
            result = f"{unicodeSquare}|{result}"
        results = result if not results else f"{results}|{result}"
    return results


def getAllChangesCount(pluginName):
    changes = api.get(f"/changes/?q=project:{pluginName}")
    return len(changes)


def getRecentChangesCount(pluginName):
    changes = api.get(f"/changes/?q=project:{pluginName}+-age:3months")
    return len(changes)


def getMetaData(pluginName):
    path = requests.utils.quote(f"plugins/{pluginName}", safe="")
    permissions = api.get(f"projects/{path}/access")
    parent = permissions["inherits_from"]["name"]
    try:
        owner_group_ids = permissions["local"]["refs/*"]["permissions"]["owner"][
            "rules"
        ].keys()
    except KeyError:
        # no owner group defined
        owner_group_ids = list()
    return parent, owner_group_ids


def getOwnerNames(pluginName):
    parent, group_ids = getMetaData(pluginName)
    names = set()
    for id in group_ids:
        try:
            owners = api.get(f"/groups/{id}/members/")
            names = names | {o.get("name") for o in owners}
        except requests.HTTPError:
            # can't read group
            pass
    names = sorted(list(names))
    if parent == "Public-Plugins":
        names.insert(0, "Core maintainers")
    names = ", ".join(names)
    return names


def isProjectEmpty(pluginName):
    gitiles_uri = f"https://gerrit.googlesource.com/{pluginName}"
    try:
        response = requests.get(gitiles_uri)
        if response.status_code == 200:
            if response.text.find("Empty Repository") > -1:
                return True
    except requests.HTTPError as e:
        print(f"Failed to browse {pluginName} in gitiles:\n{e}", file=sys.stderr)
    return False


data = {
    "permalink": "plugins",
    "updated": time.strftime("%A %d %B at %H:%M:%S %Z", time.gmtime()),
}

template_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "plugins.md.template"
)
template = Template(open(template_path).read())
rendered_template = template.render(data=data)

with open("pages/site/plugins/plugins.md", "w") as output:
    output.writelines(rendered_template)

    output.write("\n")
    for b in branches:
        output.write(f"[{b}]: https://gerrit-ci.gerritforge.com/view/Plugins-{b}/\n")

    for branch in branches:
        header += "|Branch|CI"
        dashes += "|-----:|--"
        spacer += f"|[{branch}]|"
    output.write(f"\n{header}|\n{dashes}|\n{spacer}|\n")

    url = (
        "https://gerrit-ci.gerritforge.com/api/json?pretty=true&tree=jobs"
        + "[name,lastBuild[result]]"
    )
    builds = requests.get(url).json()
    links = "\n"
    for p in tqdm(plugins):
        name = p[len("plugins/") :]
        plugin = plugins[p]

        all = getAllChangesCount(p)
        if plugin["state"] == "ACTIVE":
            state = greenCheckMark
            changes = getRecentChangesCount(p)
            availableBranches = getBranchResults(plugin["id"], name, builds)
        else:
            state = lock
            changes = 0
            availableBranches = "|".join(
                [f"{unicodeSquare}|{unicodeSquare}" for b in branches]
            )
        if isProjectEmpty(p):
            state += f"|{unicodeSquare}"
        else:
            state += f"|{checkMark}"

        if "description" in plugin:
            description = plugin["description"].split("\n")[0].rstrip(r"\.")
        else:
            description = unicodeSquare

        owners = getOwnerNames(name)

        line = f"|[{name}]|{state}|{changes}/{all}|{description}|{owners}|{availableBranches}|\n"
        output.write(line)
        links += f"[{name}]: https://gerrit.googlesource.com/plugins/{name}\n"

    output.write(links)
