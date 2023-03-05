import requests
from bs4 import BeautifulSoup
import re


def FetchPackages(config):
    req = requests.post('https://www.apkmirror.com/wp-json/apkm/v1/app_exists/',
                        json={'pnames': config.GetPatches()['packages']},
                        headers={
                            'User-Agent': None,
                            'Accept-Encoding': None,
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Authorization':
                            'Basic YXBpLXRvb2xib3gtZm9yLWdvb2dsZS1wbGF5OkNiVVcgQVVMZyBNRVJXIHU4M3IgS0s0SCBEbmJL'
                        })

    apps = []
    if req.status_code == 200:
        res = req.json()
        for app in res['data']:
            if app['exists']:
                apps.append({
                    'appName': app['app']['name'].replace(' (Wear OS)', ''),
                    'appPackage': app['pname'],
                    'link': app['app']['link'].replace('-wear-os', '')
                })
        return apps
    else:
        print(req.content)
        print(
            f"Could not request to APKMirror.\n{'You have been ratelimited' if req.status_code == 429 else f'Status code: {req.status_code}'}")
        return False


def FetchVersions(app, config):
    versionList = []
    req = requests.get(f'https://www.apkmirror.com/uploads/?appcategory={app["link"].split("/")[3]}',
                       headers={
                           'User-Agent': None,
                           'Accept-Encoding': None
                       })
    if req.status_code == 200:
        page = BeautifulSoup(req.content, "html.parser")
        primary = page.find(id="primary")
        versions = primary.find_all('h5')
        for version in versions:
            if 'widgetHeader' in version['class']:
                continue
            versionTitle = version['title'].lower()
            for child in version.contents:
                if child == '\n' or child == ' ':
                    continue
                versionName = re.split(
                    f"(?<={app['link']}{app['link'].split('/')[3]}-)(.*)(?=-release/)", child['href'])[1]
            if (
                app["appPackage"] == "com.twitter.android"
                and not versionTitle.contains("release")
            ) or '(Wear OS)' in versionTitle or '-car_release' in versionTitle:
                continue
            versionList.append({
                'versionName': versionName,
                'recommended': versionName in config.GetPatches()['recommendedVersions'],
                'beta': 'beta' in versionTitle
            })

        return versionList
    else:
        print(
            f"Could not request to APKMirror.\n{'You have been ratelimited' if req.status_code == 429 else f'Status code: {req.status_code}'}")
        return False
