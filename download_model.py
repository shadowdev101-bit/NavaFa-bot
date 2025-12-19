import os
import urllib.request

URL = "https://raw.githubusercontent.com/shadowdev101-bit/discord-bot-nf/refs/heads/main/models.py"
OUT = "vits/model.pth"

if not os.path.exists(OUT):
    print("Downloading VITS model...")
    urllib.request.urlretrieve(URL, OUT)
    print("Download complete")
else:
    print("Model already exists")