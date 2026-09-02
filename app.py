import logging
import sys

# ==============================
# 🚀 HF Anti-Crash Monkey Patch (MUST BE FIRST!)
# ==============================
# Gradio tries to import HfFolder, which was removed in newer huggingface_hub versions.
# We must patch it BEFORE importing gradio.
import huggingface_hub
if not hasattr(huggingface_hub, "HfFolder"):
    class DummyHfFolder:
        @staticmethod
        def get_token():
            return None
    huggingface_hub.HfFolder = DummyHfFolder

# ==============================
# 📦 Core Imports
# ==============================
import spaces
import gradio as gr
import uvicorn
from main import app as fastapi_app

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
    
    # Link the button to the GPU-decorated function
    btn.click(fn=gpu_bypass, inputs=[], outputs=out)

# ==============================
# ⚠️ CRITICAL: Enable Gradio Queue
# ==============================
# ZeroGPU WILL NOT WORK and will crash without the queue enabled.
demo.queue()

# ==============================
# 🔗 Safely Mount Gradio UI to FastAPI
# ==============================
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")

# ==============================
# 🏁 Entry Point
# ==============================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("JarvisApp")
    logger.info("🚀 Starting J.A.R.V.I.S. Omni-Core server on port 7860...")
    
    # Start the unified FastAPI + Gradio application
    uvicorn.run(app, host="0.0.0.0", port=7860)
