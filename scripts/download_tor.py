import io
import zipfile
import re
import requests

DOWNLOAD_PAGE = "https://www.torproject.org/download/tor/"
BASE = "https://www.torproject.org"

data = requests.get(DOWNLOAD_PAGE).text
url = re.search('"([a-zA-Z0-9./-]+\.zip)"', data).group(1)

r = requests.get(BASE + url)
with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
    zf.extractall()
