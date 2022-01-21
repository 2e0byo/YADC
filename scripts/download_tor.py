import zipfile
import io
import requests

TOR = "https://www.torproject.org/dist/torbrowser/11.0.4/tor-win32-0.4.6.9.zip"
r = requests.get(TOR)
with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
    zf.extractall()
