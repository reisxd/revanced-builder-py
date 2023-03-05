import requests
from tqdm import tqdm


def DownloadFile(location, url):
    req = requests.get(url, stream=True,
                       headers={
                           'User-Agent': None,
                           'Accept-Encoding': None
                       })

    if req.status_code == 200:
        total = int(req.headers.get('content-length', 0))
        with open(location, 'wb') as file, tqdm(
            desc=location,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in req.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

    else:
        print(
            f"Could not request to {url}.\n{'You have been ratelimited' if req.status_code == 429 else f'Status code: {req.status_code}'}")
        return False
