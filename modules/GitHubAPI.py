import requests
from modules.FileDownloader import DownloadFile
import pathlib
import os

def FetchReleases(repo):
    req = requests.get(f"https://api.github.com/repos/{repo['owner']}/{repo['repo']}/releases/latest")
    if req.status_code == 200:
        res = req.json()
        return { 'assets': res['assets'], 'version': res['tag_name'] }
    else:
        print(f"Could not request to GitHub.\n{'You have been ratelimited' if req.status_code == 429 else f'Status code: {req.status_code}'}")
        return False

def SetFiles(repo, fileName, config):
    if repo['repo'] == 'revanced-cli':
        config.SetFiles('cli', fileName)
        return
    elif repo['repo'] == 'revanced-integrations':
        config.SetFiles('integrations', fileName)
        return
    elif repo['repo'] == 'revanced-patches' and fileName.endswith('.json'):
        config.SetFiles('patches-json', fileName)
        return
    elif repo['repo'] == 'revanced-patches':
        config.SetFiles('patches', fileName)
        return
    elif repo['repo'] == 'VancedMicroG':
        config.SetFiles('microg', fileName)
        return


def DownloadFiles(config):
    repos = [
        {
            'owner': 'revanced',
            'repo': 'revanced-patches'
        },
        {
            'owner': 'revanced',
            'repo': 'revanced-integrations'
        },
        {
            'owner': 'revanced',
            'repo': 'revanced-cli'
        },
        {
            'owner': 'TeamVanced',
            'repo': 'VancedMicroG'
        },
    ]

    for repo in repos:
        assets = FetchReleases(repo)
        for asset in assets['assets']:
            fileExt = pathlib.Path(asset['name']).suffix
            fileName = f"revanced/{repo['repo']}-{assets['version']}{fileExt}"
            SetFiles(repo, fileName, config)
            revancedFolder = os.listdir('revanced')
            if fileName.split('/')[1] in revancedFolder:
                continue
            DownloadFile(fileName, asset['browser_download_url'])