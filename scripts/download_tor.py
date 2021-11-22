import zipfile
import io
import requests

TOR = "https://www.torproject.org/dist/torbrowser/11.0.1/tor-win32-0.4.6.8.zip"
r = requests.get(TOR)
with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
    zf.extractall()
