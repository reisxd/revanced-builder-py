import json
import os


def CreateFile(value={'packages': []}):
    f = open("config.json", "w")
    f.write(json.dumps(value))


def WritePatches(pkgName, patches):
    f = open("config.json", "r+")
    configJson = json.load(f)
    found = False
    for package in configJson['packages']:
        if package['name'] == pkgName:
            package['patches'] = patches
            found = True

    if not found:
        configJson['packages'].append({
            'name': pkgName,
            'patches': patches
        })
    f.seek(0)
    json.dump(configJson, f)
    f.truncate()


def LoadPatches(pkgName):
    if not os.path.exists('./config.json'):
        CreateFile()
        return []
    f = open("config.json", "r")
    configJson = json.load(f)
    for package in configJson['packages']:
        if package['name'] == pkgName:
            return package['patches']

    return []
