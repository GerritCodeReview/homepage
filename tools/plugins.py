from __future__ import print_function
import argparse
import getpass
import os
import re
import requests
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum, IntEnum
from functools import partial
from operator import attrgetter
from typing import List

from jinja2 import Template
from pygerrit2 import Anonymous, GerritRestAPI, HTTPBasicAuth, HTTPBasicAuthFromNetrc
from tqdm import tqdm


BRANCHES = ["master"] + [
    f"stable-{version}" for version in ["3.12", "3.11", "3.10"]
]
CI = "https://gerrit-ci.gerritforge.com"
GERRIT = "https://gerrit-review.googlesource.com"
GITILES = "https://gerrit.googlesource.com"

CORE_MAINTAINERS_ID = "google:AI2Pq9rwJtXWrKQ9Q62CcHSid7ngIF2hCfJ4bSpVquX_P2z5kFM6v9s"
CORE_MAINTAINERS_NAME = "Core maintainers"

BRANCH_MARK = "&#x2325;"
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


class Branch:
    """Branch of a plugin repository"""

    name: str
    build: BuildResult
    present: bool

    def __init__(self, name, build, present=True):
        self.name = name
        self.build = build
        self.present = present

    @classmethod
    def missing(cls, name):
        return cls(name, BuildResult.UNAVAILABLE, False)

    def render(self):
        return BRANCH_MARK if self.present else SQUARE


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

    def render_empty(self):
        return SQUARE if self.empty else BRANCH_MARK


@dataclass(frozen=True)
class Account:
    """Gerrit account"""

    id: str
    name: str
    email: str


class Plugins:
    """Class to retrieve data about Gerrit plugins and render the plugins page"""

    @staticmethod
    def _parse_options():
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
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
        parser.add_argument(
            "-t",
            "--threads",
            dest="threads",
            default=1,
            type=int,
            help="number of threads to fetch data from Gerrit concurrently",
        )
        parser.add_argument(
            "-s",
            "--sleep",
            dest="sleep",
            default=0,
            type=int,
            help="amount to pause in-between fetching plugins data in order to avoid rate limiting",
        )
        return parser.parse_args()

    @staticmethod
    def _render_header():
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

    @staticmethod
    def _render_template():
        data = {
            "permalink": "plugins",
            "updated": time.strftime("%A %d %B at %H:%M:%S %Z", time.gmtime()),
        }

        template_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "plugins.md.template"
        )
        template = Template(open(template_path).read())
        return template.render(data=data)

    @staticmethod
    def _get_matrix_header(state, is_empty):
        if state == PluginState.ACTIVE:
            if is_empty:
                return "Not Started"
            else:
                return "Active"
        else:
            if is_empty:
                return "Deprecated, not started"
            else:
                return "Deprecated"

    def __init__(self):
        self.options = self._parse_options()
        auth = self._authenticate()
        self.api = GerritRestAPI(url=GERRIT, auth=auth)
        self.plugins = list()
        self.maintainers = defaultdict(list)
        self._create_plugins()
        self.plugins = sorted(self.plugins, key=attrgetter("state", "empty"))

    def __iter__(self):
        return iter(self.plugins)

    def _create_plugin(self, plugin_list: dict, builds, p):
        """Create a plugin by fetching its data from Gerrit"""
        name = p[len("plugins/") :]
        plugin = plugin_list[p]

        if plugin["state"] == "ACTIVE":
            state = PluginState.ACTIVE
            changes = self._get_recent_changes_count(p)
            branches = self._get_branch_results(plugin["id"], name, builds)
        else:
            state = PluginState.READ_ONLY
            changes = 0
            branches = [Branch.missing(branch) for branch in BRANCHES]

        description = (
            plugin["description"].split("\n")[0].rstrip(r"\.")
            if "description" in plugin
            else ""
        )

        parent, owner_group_ids = self._get_meta_data(name)
        maintainers, maintainers_csv = self._get_owner_names(
            parent, name, owner_group_ids
        )
        plugin = Plugin(
            name=name,
            parent=parent,
            state=state,
            owner_group_ids=owner_group_ids,
            owner_names=maintainers_csv,
            empty=self._is_project_empty(p),
            description=description,
            all_changes_count=self._get_all_changes_count(p),
            recent_changes_count=changes,
            branches=branches,
        )
        time.sleep(self.options.sleep)
        return plugin, maintainers

    def _create_plugins(self):
        """Create plugins by fetching plugin data from Gerrit"""
        # Set an explicit limit to get more results than the index default limit
        # which is applied if no limit is set and which is 100 for gerrit-review
        # TODO: Instead of setting a high limit paginate over the results (see
        # https://issues.gerritcodereview.com/issues/296837507)
        plugin_list = self.api.get("/projects/?p=plugins%2f&d&limit=500")
        builds = requests.get(
            f"{CI}/api/json?pretty=true&tree=jobs[name,lastBuild[result]]"
        ).json()
        creator = partial(self._create_plugin, plugin_list, builds)
        with ThreadPoolExecutor(max_workers=self.options.threads) as executor:
            results = list(
                tqdm(executor.map(creator, plugin_list), total=len(plugin_list))
            )
            for (plugin, maintainers) in results:
                self.plugins.append(plugin)
                for m in maintainers:
                    self.maintainers[m.name].append((m, plugin.name))

    def _authenticate(self):
        if self.options.netrc:
            return HTTPBasicAuthFromNetrc(url=GERRIT)
        elif self.options.anonymous:
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
            string = fr"^plugin-{pluginName}-[a-z|-]*{branch}$"
            pattern = re.compile(string)
            result = BuildResult.UNAVAILABLE
            for job in builds["jobs"]:
                if pattern.match(job["name"]):
                    result = (
                        BuildResult.SUCCESSFUL
                        if job["lastBuild"] and job["lastBuild"]["result"] == "SUCCESS"
                        else BuildResult.FAILED
                    )
                    branches.append(Branch(branch, result, branch in pluginBranches))
                    break
            if result == BuildResult.UNAVAILABLE:
                branches.append(Branch.missing(branch))
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

    def _get_owner_names(self, parent, name, owner_group_ids):
        accounts = set()
        external_groups = set()
        all_owner_group_ids = set(owner_group_ids)
        # add subgroups if any
        for id in owner_group_ids:
            if id == CORE_MAINTAINERS_ID:
                continue
            else:
                try:
                    subgroups = self.api.get(f"/groups/{id}/groups")
                    for s in subgroups:
                        all_owner_group_ids.add(s.get("id"))
                except requests.HTTPError:
                    print(
                        f"Failed to read subgroup {id} of owner group of plugin {name}",
                        file=sys.stderr,
                    )
        for id in all_owner_group_ids:
            try:
                if id == CORE_MAINTAINERS_ID:
                    external_groups.add(CORE_MAINTAINERS_NAME)
                else:
                    owners = self.api.get(f"/groups/{id}/members/")
                    a = {
                        Account(o.get("_account_id"), o.get("name"), o.get("email"))
                        for o in owners if o.get("name") is not None
                    }
                    accounts.update(a)
            except requests.HTTPError:
                print(
                    f"Failed to read owner group {id} of plugin {name}", file=sys.stderr
                )
        csv = ", ".join(sorted({a.name for a in accounts} | external_groups))
        return accounts, csv

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

    def _render_maintainers(self, output):
        header = "|Maintainer|Plugins|"
        dashes = "|----------|-------|"
        output.write("\n\n## Plugin Maintainers")
        output.write(f"\n\n{header}|\n{dashes}|\n")
        for m in sorted(self.maintainers):
            plugins = set()
            for (_, p) in self.maintainers.get(m):
                plugins.add(p)
            output.write(f"|{m}|{', '.join(sorted(plugins))}|\n")

    def render_maintainers_email(self, output):
        output.write(f"\nAll {len(self.maintainers)} plugin maintainers:\n")
        for m in sorted(self.maintainers):
            if m == CORE_MAINTAINERS_NAME:
                continue
            emails = set()
            output.write(f"{m}: ")
            for (accounts, _) in self.maintainers.get(m):
                if accounts.email:
                    emails.add(accounts.email)
            output.write(f"{', '.join(sorted(emails))}\n")

    def render_page(self, output):
        output.writelines(self._render_template())
        (header, dashes, spacer, links) = self._render_header()

        flags = (None, None)
        for p in self.plugins:
            if flags != (p.state, p.empty):
                output.write(f"\n\n### {self._get_matrix_header(p.state, p.empty)}")
                output.write(f"\n\n{header}|\n{dashes}|\n{spacer}|\n")
            branches = "|".join(
                [f"{b.render()}|{b.build.render()}" for b in p.branches]
            )
            output.write(
                f"|[{p.name}]"
                + f"|{p.state.render()}|{p.render_empty()}"
                + f"|{p.recent_changes_count}"
                + f"/[{p.all_changes_count}]({GERRIT}/q/project:plugins/{p.name})"
                + f"|{p.description}"
                + f"|{p.owner_names}"
                + f"|{branches}"
                + "|\n"
            )
            flags = (p.state, p.empty)
            links += f"[{p.name}]: {GITILES}/plugins/{p.name}\n"

        output.write(links)
        self._render_maintainers(output)


def main():
    plugins = Plugins()
    with open("pages/site/plugins/plugins.md", "w") as output:
        plugins.render_page(output)
    plugins.render_maintainers_email(sys.stdout)


if __name__ == "__main__":
    main()
