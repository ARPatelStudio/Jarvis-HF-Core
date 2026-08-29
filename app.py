import uvicorn
import spaces
from main import app

# 🚀 HF ZeroGPU Bypass: Dummy function taaki startup crash na ho
@spaces.GPU
def gpu_bypass():
    pass

if __name__ == "__main__":
    # Hugging Face hamesha port 7860 par traffic bhejta hai
    uvicorn.run("main:app", host="0.0.0.0", port=7860)
