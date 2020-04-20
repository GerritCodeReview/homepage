from __future__ import print_function
import argparse
import getpass
import os
import re
import requests
import sys
import time
from dataclasses import dataclass
from enum import Enum, IntEnum
from operator import attrgetter
from typing import List

from jinja2 import Template
from pygerrit2 import Anonymous, GerritRestAPI, HTTPBasicAuth, HTTPBasicAuthFromNetrc
from tqdm import tqdm


BRANCHES = ["master"] + [f"stable-{version}" for version in ["3.1", "3.0", "2.16"]]
CI = "https://gerrit-ci.gerritforge.com"
GERRIT = "https://gerrit-review.googlesource.com"
GITILES = "https://gerrit.googlesource.com"

CHECK_MARK = "&#x2714;"
GREEN_CHECK_MARK = "&#x2705;"
LOCK = "&#x1F512;"
RED_CROSS = "&#x274C;"
SQUARE = "&#x20DE;"


class BuildResult(Enum):
    """Build result for a plugin"""

    UNAVAILABLE = "unavailable"
    SUCCESSFUL = "successful"
    FAILED = "failed"

    def render(self):
        if self == BuildResult.SUCCESSFUL:
            return GREEN_CHECK_MARK
        elif self == BuildResult.FAILED:
            return RED_CROSS
        else:
            return SQUARE


class PluginState(IntEnum):
    ACTIVE = 1
    READ_ONLY = 2

    def render(self):
        if self == PluginState.ACTIVE:
            return GREEN_CHECK_MARK
        else:
            return LOCK


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

    def _render_empty(self):
        return SQUARE if self.empty else CHECK_MARK

    def render_state(self) -> str:
        return f"{self.state.render()}|{self._render_empty()}"

    def render_branches(self) -> str:
        results = ""
        for branch_name in BRANCHES:
            branch_exists = SQUARE
            build_state = SQUARE
            if self.branches:
                for b in self.branches:
                    if b.name == branch_name:
                        branch_exists = CHECK_MARK
                        build_state = b.build.render()
                        break
            result = f"{branch_exists}|{build_state}"
            results = result if not results else f"{results}|{result}"
        return results


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
        self.plugins = sorted(self.plugins, key=attrgetter("state", "empty"))

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

            if plugin["state"] == "ACTIVE":
                state = PluginState.ACTIVE
                changes = self._get_recent_changes_count(p)
                branches = self._get_branch_results(plugin["id"], name, builds)
            else:
                state = PluginState.READ_ONLY
                changes = 0
                branches = None

            description = (
                plugin["description"].split("\n")[0].rstrip(r"\.")
                if "description" in plugin
                else ""
            )

            parent, owner_group_ids = self._get_meta_data(name)
            self.plugins.append(
                Plugin(
                    name=name,
                    parent=parent,
                    state=state,
                    owner_group_ids=owner_group_ids,
                    owner_names=self._get_owner_names(parent, owner_group_ids),
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
                        result = (
                            BuildResult.SUCCESSFUL
                            if job["lastBuild"]["result"] == "SUCCESS"
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

    def _get_owner_names(self, parent, owner_group_ids):
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

    @staticmethod
    def render_header():
        header = "|Name|State|Repo|Changes (last 3 months/all)|Description|Maintainers"
        dashes = "|----|-----|----|---------------------------|-----------|---"
        spacer = "|    |     |    |                           |           |   "
        links = "\n"
        for b in BRANCHES:
            header += "|Branch|CI"
            dashes += "|-----:|--"
            spacer += f"|[{b}]|"
            links += f"[{b}]: {CI}/view/Plugins-{b}\n"

        return (header, dashes, spacer, links)


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

    flags = (None, None)
    plugins = Plugins(options)
    (header, dashes, spacer, links) = plugins.render_header()
    for p in plugins:
        if flags != (p.state, p.empty):
            output.write(f"\n\n{header}|\n{dashes}|\n{spacer}|\n")
        output.write(
            f"|[{p.name}]"
            + f"|{p.render_state()}"
            + f"|{p.recent_changes_count}"
            + f"/[{p.all_changes_count}]({GERRIT}/q/project:plugins/{p.name})"
            + f"|{p.description}"
            + f"|{p.owner_names}"
            + f"|{p.render_branches()}"
            + "|\n"
        )
        flags = (p.state, p.empty)
        links += f"[{p.name}]: {GITILES}/plugins/{p.name}\n"

    output.write(links)
