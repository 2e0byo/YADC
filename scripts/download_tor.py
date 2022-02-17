import zipfile
import io
import requests

TOR = "https://dist.torproject.org/torbrowser/11.0.6/tor-win64-0.4.6.9.zip"
r = requests.get(TOR)
with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
    zf.extractall()
