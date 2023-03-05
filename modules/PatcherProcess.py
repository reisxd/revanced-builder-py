import shutil
import subprocess
from modules.ADB import *

# https://stackoverflow.com/a/72101287
def RunCommand(command, **kwargs):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs,
    )
    while True:
        stdOut = process.stdout.readline()
        if not stdOut and process.poll() is not None:
            break
        print(stdOut.decode(), end='')

def RunPatcher(config, app):
    files = config.GetFiles()
    patches = config.GetPatches()
    hasDevice = False
    isRooted = False

    args = [
            'java',
            '-jar',
            files['cli'],
            '-b',
            files['patches'],
            '--experimental',
            '-a',
            f'revanced/{app["appPackage"]}.apk',
            '-o',
            f'revanced/ReVanced-{app["appName"]}.apk',
            '-m',
            files["integrations"],
            '--exclusive'
        ]
    
    if CheckADBInstalled():
        deviceId = GetFirstDevice()
        if deviceId:
            args.append('-d')
            args.append(deviceId)
            hasDevice = True
    if 'microg-support' not in patches['patches'] or (app['appPackage'] == 'com.google.android.apps.youtube.music' and 'music-microg-support' not in patches['patches']):
        args.append('--mount')
        isRooted = True
    
    for patch in patches['patches']:
        args.append('-i')
        args.append(patch)

    RunCommand(args)
    shutil.rmtree('./revanced-cache')

    if hasDevice and isRooted:
        print('Successfully patched and mounted ReVanced!')
    elif hasDevice:
        if not isRooted and 'microg-patch' in patches['patches'] or 'music-microg-patch' in patches['patches']:
            InstallMicroG(config.GetFiles())
        print('Successfully patched and installed ReVanced and installed Vanced MicroG!')
    else:
        print(f"""Successfully patched ReVanced! Please transfer revanced/ReVanced-{app["appName"]}.apk
        and if you patched YT/YTM, also transfer revanced/{config.GetFiles()['microg']}.""")