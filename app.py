import sys
import uvicorn

# 🚀 THE MONKEY PATCH: HF Anti-Crash Bypass
# Gradio ko ullu banane ke liye hum ek fake HfFolder create kar rahe hain
import huggingface_hub
if not hasattr(huggingface_hub, "HfFolder"):
    # Agar HfFolder delete ho chuka hai, toh ek dummy class inject kar do
    huggingface_hub.HfFolder = type("HfFolder", (), {"get_token": lambda: None})

import spaces
from main import app

# 🚀 HF ZeroGPU Bypass: Dummy function taaki startup crash na ho
@spaces.GPU
def gpu_bypass():
    pass

if __name__ == "__main__":
    # Hugging Face hamesha port 7860 par traffic bhejta hai
    uvicorn.run("main:app", host="0.0.0.0", port=7860)
