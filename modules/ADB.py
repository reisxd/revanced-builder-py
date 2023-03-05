import subprocess
import re


def CheckADBInstalled():
    try:
        subprocess.run(['adb'], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return False
    return True


def GetFirstDevice():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    devices = re.search('\n(.*?)\t', result.stdout)
    if devices == None:
        return None
    return devices.group().replace('\n', '').replace('\t', '')


def CheckRoot():
    result = subprocess.run(['adb', 'shell', 'su -c exit'],
                            capture_output=True, text=True)
    if 'inaccessible or not found' in result.stderr:
        return False
    return True


def CheckForRoot():
    if not CheckADBInstalled():
        print('ADB is not installed. Please install it and connect your device.')
        return False
    else:
        deviceId = GetFirstDevice()
        if deviceId == None:
            print("There's no device plugged in. Please plug in a device.")
            return False
        if not CheckRoot():
            print("Your device is either not rooted or denied root access to shell.")
            return False
    return deviceId


def GetPackageVersion(app):
    result = subprocess.run(['adb', 'shell', 'dumpsys', 'package',
                            app['appPackage']], capture_output=True, text=True)
    appVersion = re.split('versionName=([^=]+)', result.stdout)
    if appVersion == None:
        return None
    return appVersion[1].replace('\n    splits', '')


def InstallMicroG(files):
    subprocess.run(['adb', 'install', files['microg']],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
