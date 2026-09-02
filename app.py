import logging
import gradio as gr
import uvicorn
import spaces
from fastapi import FastAPI

# ==============================
# 📦 Core Imports
# ==============================
# Import your FastAPI app
from main import app as fastapi_app

# ==============================
# 🏥 HF Health Check Endpoint
# ==============================
# Hugging Face pings "/" to check if the app is alive. 
# Without this, it might kill the container.
@fastapi_app.get("/")
def health_check():
    return {"status": "J.A.R.V.I.S. Omni-Core is online"}

# ==============================
# 🚀 ZeroGPU Decorated Function
# ==============================
@spaces.GPU
def gpu_bypass():
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return f"ZeroGPU Active! Engine running on: {device.upper()}"

# ==============================
# 🎨 Minimal Gradio UI
# ==============================
with gr.Blocks(theme=gr.themes.Monochrome(), title="J.A.R.V.I.S. Omni-Core") as demo:
    gr.Markdown("# 🟢 J.A.R.V.I.S. Omni-Core is Live")
    gr.Markdown("System initialized. FastAPI backend is running in the background.")
    
    btn = gr.Button("Ping Engine Status")
    out = gr.Textbox(label="Status")
    
    btn.click(fn=gpu_bypass, inputs=[], outputs=out)

# Enable Gradio Queue (Required for ZeroGPU)
demo.queue()

# ==============================
# 🔗 Mount Gradio UI to FastAPI
# ==============================
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")

# ==============================
# 🏁 Entry Point (NO IF GUARD!)
# ==============================
# We remove the `if __name__ == "__main__":` guard so that 
# Hugging Face's supervisor is forced to start the server.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("JarvisApp")
logger.info("🚀 Starting J.A.R.V.I.S. Omni-Core server on port 7860...")

# Start the unified FastAPI + Gradio application
uvicorn.run(app, host="0.0.0.0", port=7860)
