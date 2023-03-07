import subprocess
import re

# https://stackoverflow.com/a/19859308

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def CheckJDKInstalled():
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        javaLog = result.stdout or result.stderr
        buildString = re.findall('\(.+?\)', javaLog)
        if buildString == []:
            print('JDK is not installed.\nPlease install JDK from here: https://www.azul.com/downloads-new/?package=jdk')
            return False
        indx = 0
        for i in range(0, len(buildString)):
            if hasNumbers(buildString[i]):
                indx = i
                break
        version = re.sub(r'[()]', '', buildString[indx].replace('build ', ''))
        versionNumbers = version.split('.')
        if int(versionNumbers[0]) < 17 or 'openjdk' not in javaLog:
            print("JDK/Java was installed, but it's too old or not a JDK distribution.\nPlease install JDK from here: https://www.azul.com/downloads-new/?package=jdk")
            return False
        else:
            return True
    except FileNotFoundError:
        print('JDK is not installed.\nPlease install JDK from here: https://www.azul.com/downloads-new/?package=jdk')
        return False