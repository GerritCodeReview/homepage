import re
import requests

from shutil import copyfile
from pygerrit2 import GerritRestAPI, HTTPBasicAuthFromNetrc

url = "https://gerrit-review.googlesource.com"
auth = HTTPBasicAuthFromNetrc(url=url)
api = GerritRestAPI(url=url, auth=auth)
plugins = api.get("/projects/?p=plugins%2f&d")

header = "|Name|State|Changes"
dashes = "|----|-----|-------"
spacer = "|    |     |       "

branches = ["master"] + ["stable-%s" % version for version in [
    "3.1",
    "3.0",
    "2.16",
]]


def getBranches(pluginId):
    branchList = api.get("/projects/%s/branches/" % pluginId)
    pluginBranches = []
    for b in branchList:
        if b['ref'].startswith('refs/heads/'):
            ref = b['ref']
            pluginBranches += [ref[len('refs/heads/'):]]
    return pluginBranches


def getBranchResults(pluginId, pluginName, builds):
    pluginBranches = getBranches(pluginId)
    results = ""
    for branch in branches:
        string = r"^plugin-%s[\w|-]*-%s$" % (pluginName, branch)
        pattern = re.compile(string)
        result = 'NONE'

        for job in builds['jobs']:
            if pattern.match(job['name']):
                result = job['lastBuild']['result'][0]
                break

        if branch in pluginBranches:
            result = "YES|" + result
        else:
            result = "NO|" + result
        results = result if not results else "%s|%s" % (results, result)
    return results


def getRecentChangesCount(pluginName):
    changes = api.get("/changes/?q=project:%s after:2019-12-31" % pluginName)
    return len(changes)


page = "plugins"
template = open("template.md", 'r')
output = open("%s.md" % page, 'w')
for line in template:
    output.write(line.replace("template", page))

output.write('\n')
for b in branches:
    output.write(
        "[%s]: https://gerrit-ci.gerritforge.com/view/Plugins-%s/\n" % (b, b))

for branch in branches:
    header += "|Branch|CI"
    dashes += "|------|--"
    spacer += "|[%s]|" % branch
output.write("\n%s|\n%s|\n%s|\n" % (header, dashes, spacer))

url = "https://gerrit-ci.gerritforge.com/api/json?pretty=true&tree=jobs[name,lastBuild[result]]"
builds = requests.get(url).json()
descriptions = ""
links = "\n"
for p in plugins:
    name = p[len("plugins/"):]
    plugin = plugins[p]
    state = plugin['state']

    if plugin['state'] == 'ACTIVE':
        changes = getRecentChangesCount(p)
        availableBranches = getBranchResults(plugin['id'], name, builds)
    else:
        changes = 0
        availableBranches = "|".join(["N/A|N/A" for b in branches])

    if 'description' in plugin:
        description = plugin['description'].split('\n')[0].rstrip(r'\.')
    else:
        description = 'NONE'

    line = "|[%s]|%s|%d|%s|\n" % (name, state, changes, availableBranches)
    output.write(line)

    descriptions += "|[%s]|%s|\n" % (name, description)
    links += "[%s]: https://gerrit.googlesource.com/plugins/%s\n" % (
        name, name)

output.write("\n## Plugin descriptions\n\n")
output.write("|Name|Description|\n")
output.write("|----|-----------|\n")
output.write(descriptions)
output.write(links)
