import torch
import json
from scipy.io.wavfile import write

# รับพารามิเตอร์
import sys
text = sys.argv[1]
output_path = sys.argv[2]

# โหลด config
config_file = "vits/config.json"
with open(config_file, "r") as f:
    hps = json.load(f)

# ตัวอย่างโค้ดโหลดโมเดลจริง
# (ต้องแก้ให้ตรงกับโมเดลที่คุณใช้จริง)
from models import VITS

model = VITS(hps["model"])
checkpoint = torch.load("vits/model.pth", map_location="cpu")
model.load_state_dict(checkpoint["model"])
model.eval()

# แปลงข้อความเป็นเสียงจริง
with torch.no_grad():
    audio = model.infer(text)

# บันทึกไฟล์เสียง
write(output_path, hps["data"]["sampling_rate"], audio.numpy())
