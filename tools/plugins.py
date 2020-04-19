from __future__ import print_function
import argparse
import getpass
import os
import re
import requests
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import List

from jinja2 import Template
from pygerrit2 import Anonymous, GerritRestAPI, HTTPBasicAuth, HTTPBasicAuthFromNetrc
from tqdm import tqdm


BRANCHES = ["master"] + [f"stable-{version}" for version in ["3.1", "3.0", "2.16"]]
CI = "https://gerrit-ci.gerritforge.com"
GERRIT = "https://gerrit-review.googlesource.com"
GITILES = "https://gerrit.googlesource.com"


class BuildResult(Enum):
    UNAVAILABLE = "unavailable"
    SUCCESSFUL = "successful"
    FAILED = "failed"


class PluginState(Enum):
    ACTIVE = "active"
    READ_ONLY = "read-only"


@dataclass
class Branch:
    """Branch of a plugin repository"""

    name: str
    build: BuildResult


@dataclass
class Plugin:
    """Gerrit plugin"""

    name: str
    parent: str
    state: PluginState
    owner_group_ids: List[str]
    owner_names: List[str]
    empty: bool
    description: str
    all_changes_count: int
    recent_changes_count: int
    branches: List[Branch]


class Plugins:
    """Data about Gerrit plugins"""

    def __init__(self, options):
        """Get data about all Gerrit plugins.

        :param options: command line options
        """
        auth = self._authenticate(options)
        self.api = GerritRestAPI(url=GERRIT, auth=auth)
        self.plugins = list()
        self._fetch_plugin_data()

    def __iter__(self):
        return iter(self.plugins)

    def _fetch_plugin_data(self):
        """Fetch plugin data from Gerrit"""
        plugin_list = self.api.get("/projects/?p=plugins%2f&d")
        builds = requests.get(
            f"{CI}/api/json?pretty=true&tree=jobs[name,lastBuild[result]]"
        ).json()
        for p in tqdm(plugin_list):
            name = p[len("plugins/") :]
            plugin = plugin_list[p]
            parent, owner_group_ids = self._get_meta_data(name)
            if plugin["state"] == "ACTIVE":
                state = PluginState.ACTIVE
                changes = self._get_recent_changes_count(p)
                branches = self._get_branch_results(plugin["id"], name, builds)
            else:
                state = PluginState.READ_ONLY
                changes = 0
                branches = None
            if "description" in plugin:
                description = plugin["description"].split("\n")[0].rstrip(r"\.")
            else:
                description = ""
            self.plugins.append(
                Plugin(
                    name=name,
                    parent=parent,
                    state=state,
                    owner_group_ids=owner_group_ids,
                    owner_names=self._get_owner_names(name, parent, owner_group_ids),
                    empty=self._is_project_empty(p),
                    description=description,
                    all_changes_count=self._get_all_changes_count(p),
                    recent_changes_count=changes,
                    branches=branches,
                )
            )

    def _authenticate(self, options):
        if options.netrc:
            return HTTPBasicAuthFromNetrc(url=GERRIT)
        elif options.anonymous:
            return Anonymous()
        else:
            return self._authenticate_interactive()

    def _authenticate_interactive(self):
        username = os.environ.get("username")
        password = os.environ.get("password")
        while not username:
            username = input("user: ")
        while not password:
            password = getpass.getpass("password: ")
        auth = HTTPBasicAuth(username, password)
        return auth

    def _get_branches(self, pluginId):
        branchList = self.api.get(f"/projects/{pluginId}/branches/")
        pluginBranches = []
        for b in branchList:
            if b["ref"].startswith("refs/heads/"):
                ref = b["ref"]
                pluginBranches += [ref[len("refs/heads/") :]]
        return pluginBranches

    def _get_branch_results(self, pluginId, pluginName, builds):
        pluginBranches = self._get_branches(pluginId)
        branches = list()
        for branch in BRANCHES:
            if branch in pluginBranches:
                string = fr"^plugin-{pluginName}[\w|-]*-{branch}$"
                pattern = re.compile(string)
                result = BuildResult.UNAVAILABLE
                for job in builds["jobs"]:
                    if pattern.match(job["name"]):
                        result = job["lastBuild"]["result"]
                        result = (
                            BuildResult.SUCCESSFUL
                            if result == "SUCCESS"
                            else BuildResult.FAILED
                        )
                        break
                branches.append(Branch(branch, result))
        return branches

    def _get_all_changes_count(self, pluginName):
        changes = self.api.get(f"/changes/?q=project:{pluginName}")
        return len(changes)

    def _get_recent_changes_count(self, pluginName):
        changes = self.api.get(f"/changes/?q=project:{pluginName}+-age:3months")
        return len(changes)

    def _get_meta_data(self, pluginName):
        path = requests.utils.quote(f"plugins/{pluginName}", safe="")
        permissions = self.api.get(f"projects/{path}/access")
        parent = permissions["inherits_from"]["name"]
        try:
            owner_group_ids = permissions["local"]["refs/*"]["permissions"]["owner"][
                "rules"
            ].keys()
        except KeyError:
            # no owner group defined
            owner_group_ids = list()
        return parent, owner_group_ids

    def _get_owner_names(self, pluginName, parent, owner_group_ids):
        names = set()
        for id in owner_group_ids:
            try:
                owners = self.api.get(f"/groups/{id}/members/")
                names = names | {o.get("name") for o in owners}
            except requests.HTTPError:
                # can't read group
                pass
        names = sorted(list(names))
        if parent == "Public-Plugins":
            names.insert(0, "Core maintainers")
        names = ", ".join(names)
        return names

    def _is_project_empty(self, pluginName):
        gitiles_uri = f"{GITILES}/{pluginName}"
        try:
            response = requests.get(gitiles_uri)
            if response.status_code == 200:
                if response.text.find("Empty Repository") > -1:
                    return True
        except requests.HTTPError as e:
            print(f"Failed to browse {pluginName} in gitiles:\n{e}", file=sys.stderr)
        return False


CHECK_MARK = "&#x2714;"
GREEN_CHECK_MARK = "&#x2705;"
LOCK = "&#x1F512;"
RED_CROSS = "&#x274C;"
SQUARE = "&#x20DE;"


def render_header(output):
    header = "|Name|State|Repo|Changes (last 3 months/all)|Description|Maintainers"
    dashes = "|----|-----|----|---------------------------|-----------|---"
    spacer = "|    |     |    |                           |           |   "

    output.write("\n")
    for b in BRANCHES:
        output.write(f"[{b}]: {CI}/view/Plugins-{b}/\n")

    for branch in BRANCHES:
        header += "|Branch|CI"
        dashes += "|-----:|--"
        spacer += f"|[{branch}]|"
    output.write(f"\n{header}|\n{dashes}|\n{spacer}|\n")


def render_state(p: Plugin) -> str:
    if p.state == PluginState.ACTIVE:
        state = GREEN_CHECK_MARK
    else:
        state = LOCK
    if p.empty:
        state += f"|{SQUARE}"
    else:
        state += f"|{CHECK_MARK}"
    return state


def render_branches(p: Plugin) -> str:
    results = ""
    for branch_name in BRANCHES:
        branch_exists = SQUARE
        build_state = SQUARE
        if p.branches:
            for b in p.branches:
                branch_exists = CHECK_MARK
                if b.name == branch_name:
                    if b.build == BuildResult.SUCCESSFUL:
                        build_state = GREEN_CHECK_MARK
                    elif b.build == BuildResult.FAILED:
                        build_state = RED_CROSS
        result = f"{branch_exists}|{build_state}"
        results = result if not results else f"{results}|{result}"
    return results


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

    render_header(output)

    links = "\n"
    for p in Plugins(options):
        output.write(
            f"|[{p.name}]"
            + f"|{render_state(p)}"
            + f"|{p.recent_changes_count}"
            + f"/[{p.all_changes_count}]({GERRIT}/q/project:plugins/{p.name})"
            + f"|{p.description}"
            + f"|{p.owner_names}"
            + f"|{render_branches(p)}"
            + "|\n"
        )
        links += f"[{p.name}]: {GITILES}/plugins/{p.name}\n"

    output.write(links)
