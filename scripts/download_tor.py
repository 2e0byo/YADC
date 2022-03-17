import zipfile
import io
import requests

TOR = "https://dist.torproject.org/torbrowser/11.0.7/tor-win64-0.4.6.10.zip"
r = requests.get(TOR)
with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
    zf.extractall()
