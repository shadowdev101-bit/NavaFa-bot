import sys

text = sys.argv[1]
output = sys.argv[2]

# --- ตัวอย่าง ---
# ตรงนี้แทนด้วย code inference ของ VITS ที่คุณใช้
# ให้มันสร้างไฟล์ wav ออกมาตาม path ที่รับมา

from scipy.io.wavfile import write
import numpy as np

sr = 22050
audio = np.zeros(sr)  # mock เสียง (ทดสอบ)
write(output, sr, audio)