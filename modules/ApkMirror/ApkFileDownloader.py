import requests
from bs4 import BeautifulSoup
import inquirer
from modules.FileDownloader import DownloadFile

def MakeRequest(url):
    req = requests.get(url,
    headers={
        'User-Agent': None, 
        'Accept-Encoding': None
    })
    return req

def DownloadAPK(version, app):
    req = MakeRequest(f'https://www.apkmirror.com{app["link"]}{app["link"].split("/")[3]}-{version}-release/')
   
    if req.status_code == 200:
        page = BeautifulSoup(req.content, "html.parser")
        universal = page.select("span[class='apkm-badge']")[0]
        notUniversal = page.find('div', class_='table-cell rowheight addseparator expand pad dowrap', string='arm64-v8a')
        if notUniversal:
            questions = [
                inquirer.List(
                    "arch",
                    message="Please select the architecture you want to patch.\nYou can find this information on your devices settings or using CPU-Z",
                    choices=[
                        ("arm64-v8a"),
                        ("armeabi-v7a")
                    ],
                    ),
                ]

            answers = inquirer.prompt(questions)

            apk = page.find('div', class_='table-cell rowheight addseparator expand pad dowrap', string=answers['arch'])
            apkLink = apk.find_previous_sibling('div').find('a')['href']
        else:
            apk = universal
            apkLink = apk.find_previous_sibling('a')['href']
        
        if not apkLink:
            print(f'Could not find APK. Please try downgrading.')
            return False

        req = MakeRequest(f'https://apkmirror.com{apkLink}')
        page = BeautifulSoup(req.content, "html.parser")
        downloadLink = page.find('a', class_='accent_bg')['href']
        
        req = MakeRequest(f'https://apkmirror.com{downloadLink}')
        page = BeautifulSoup(req.content, "html.parser")
        apkLink = page.find('a', attrs={ 'rel': 'nofollow' })['href']

        DownloadFile(f'revanced/{app["appPackage"]}.apk', f'https://apkmirror.com{apkLink}')
    else:
        print(f"Could not request to APKMirror.\n{'You have been ratelimited' if req.status_code == 429 else f'Status code: {req.status_code}'}")
        return False