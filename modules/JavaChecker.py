import subprocess
import re

def CheckJDKInstalled():
    try:
        result = subprocess.run(['java', '--version'], capture_output=True, text=True)
        javaLog = result.stdout or result.stderr
        buildString = re.findall('\(.+?\)', javaLog)
        if buildString == None:
            print('JDK is not installed.')
            return False
        version = re.sub(r'[()]', '', buildString[0].replace('build ', ''))
        versionNumbers = version.split('.')
        if int(versionNumbers[0]) < 17 or 'openjdk' not in javaLog:
            print("JDK/Java was installed, but it's too old or not a JDK distribution.\nPlease install JDK from here: https://www.azul.com/downloads-new/?package=jdk")
            return False
        else:
            return True
    except FileNotFoundError:
        return False
