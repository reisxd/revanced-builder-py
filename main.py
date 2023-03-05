import inquirer
from modules.GitHubAPI import DownloadFiles
from modules.PatchesParser import ParsePatches
from modules.ApkMirror.Scraper import *
from modules.ApkMirror.ApkFileDownloader import *
from modules.PatcherProcess import RunPatcher
from modules.ADB import CheckForRoot, GetPackageVersion
from modules.JavaChecker import CheckJDKInstalled
from modules.PatchRememberer import *
import os
import modules.Configuration

config = modules.Configuration.Configuration()
selectedApp = {}

def main():


    if not os.path.exists('revanced'):
        os.mkdir('./revanced')

    if not CheckJDKInstalled():
        print('aa')
        ExitApp()
    print('Welcome to ReVanced Builder PY! Please wait while Builder updates files.')


    DownloadFiles(config)
    ParsePatches(None, config)
    apps = FetchPackages(config)
    appList = []
    for app in apps:
        appList.append((app['appName'], app))

    questions = [
        inquirer.List(
            "app",
            message="Please select the app you want to patch",
            choices=appList,
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers == None:
        ExitApp()

    selectedApp = answers['app']
    ParsePatches(answers['app']['appPackage'], config)

    questions = [
        inquirer.List(
            "patches",
            message="Would you like to choose the patches yourself or choose the recommended patches",
            choices=[
                ("Select recommended patches", True),
                ("Select patches", False)
            ], 
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers == None:
        ExitApp()

    patchList = []

    if answers['patches']:
        patches = config.GetPatches()['patches']
        for patch in config.GetPatches()['patches']:
            if patch['recommended']:
                patchList.append(patch['name'])
        config.SetPatches('patches', patchList)
    else:
        selectedPatches = LoadPatches(selectedApp['appPackage'])
        for patch in config.GetPatches()['patches']:
            patchList.append(
                (f"{patch['name']}\n   {patch['desc']}\n\n", patch['name']))

        questions = [
            inquirer.Checkbox(
                "patches",
                message="Please select the patches you want",
                choices=patchList,
                default=selectedPatches
            ),
        ]

        answers = inquirer.prompt(questions)

        if answers == None:
            ExitApp()

        WritePatches(selectedApp['appPackage'], answers['patches'])
        config.SetPatches('patches', answers['patches'])
        if (selectedApp['appPackage'] == 'com.google.android.youtube'
            and 'microg-support' not in answers['patches']) or (selectedApp['appPackage'] == 'com.google.android.apps.youtube.music'
                                                            and 'music-microg-support' not in answers['patches']):
            
            deviceId = CheckForRoot()
            if not deviceId:
                ExitApp()
            else:
                DownloadAPK(
                    re.sub('\.', '-', GetPackageVersion(selectedApp), selectedApp))
                RunPatcher(config, selectedApp)

    if os.path.exists(f"revanced/{selectedApp['appPackage']}.apk"):
        questions = [
            inquirer.Confirm(
                "downloadAPK",
                message="APK File already exists, do you want to download an another version"
            )
        ]

        answers = inquirer.prompt(questions)
        if answers == None:
            ExitApp()

        if not answers['downloadAPK']:
            RunPatcher(config, selectedApp)
            ExitApp()
    versions = FetchVersions(selectedApp, config)

    versionList = []
    backslashChar = "\\"
    for version in versions:
        versionList.append(
            (f"{re.sub(f'{backslashChar}-', '.', version['versionName'])} {'(Recommended)' if version['recommended'] else ''}", version))

    questions = [
        inquirer.List(
            "version",
            message="Please select the version you want to patch",
            choices=versionList,
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers == None:
        ExitApp()

    DownloadAPK(answers['version']['versionName'], selectedApp)

    RunPatcher(config, selectedApp)

    ExitApp()


def ExitApp():
    input("Press any key to exit...")
    quit(0)