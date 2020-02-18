from shutil import copyfile
from pygerrit2 import GerritRestAPI, HTTPBasicAuthFromNetrc

url = "https://gerrit-review.googlesource.com"
auth = HTTPBasicAuthFromNetrc(url=url)
api = GerritRestAPI(url=url, auth=auth)
plugins = api.get("/projects/?p=plugins%2f&d")

header = "|Name|State|Changes|Description"
dashes = "|----|-----|-------|-----------"
spacer = "|    |     |       |           "

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
    return "|".join(["YES" if b in pluginBranches else "NO" for b in branches])


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
    header = "%s|  " % header
    dashes = "%s|--" % dashes
    for _ in branch:
        dashes = "%s-" % dashes
        header = "%s " % header
    spacer = "%s|[%s]" % (spacer, branch)
output.write("\n%s|\n%s|\n%s|\n" % (header, dashes, spacer))

links = "\n"
for p in plugins:
    name = p[len("plugins/"):]
    plugin = plugins[p]
    state = plugin['state']

    if plugin['state'] == 'ACTIVE':
        changes = getRecentChangesCount(p)
        availableBranches = getBranches(plugin['id'])
    else:
        changes = 0
        availableBranches = "|".join(["N/A" for b in branches])

    if 'description' in plugin:
        description = plugin['description'].split('\n')[0]
    else:
        description = 'NONE'

    line = "|[%s]|%s|%d|%s|%s|\n" % (
        name, state, changes, description, availableBranches)
    output.write(line)
    links = "%s[%s]: https://gerrit.googlesource.com/plugins/%s\n" % (
        links, name, name)

output.write(links)
