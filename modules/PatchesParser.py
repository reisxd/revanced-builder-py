import json

def ParsePatches(packageName, config):
    with open(config.GetFiles()['patches-json']) as f:
        patches = json.load(f)
    for patch in patches:
        isCompatible = False
        for package in patch['compatiblePackages']:
            if package['name'] not in config.GetPatches()['packages']:
                packages = config.GetPatches()['packages']
                packages.append(package['name'])
                config.SetPatches('packages', packages)
            if package['name'] != packageName:
                continue
            else:
                patches = config.GetPatches()['patches']
                latestVer = package['versions'][-1] if package['versions'] else 'NONE'
                patches.append({
                    'name': patch['name'],
                    'desc': patch['description'],
                    'latestVer': latestVer,
                    'recommended': not patch['excluded']
                })
                config.SetPatches('patches', patches)

                for version in package['versions']:
                    if version not in config.GetPatches()['recommendedVersions']:
                        versions = config.GetPatches()['recommendedVersions']
                        versions.append(version)
                        config.SetPatches('recommendedVersions', versions)
