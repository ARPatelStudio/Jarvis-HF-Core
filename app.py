import logging
import sys
import gradio as gr
import uvicorn
import spaces

# ==============================
# 🔧 Logging Setup
# ==============================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("JarvisApp")

# ==============================
# 🚀 HF Anti-Crash Monkey Patch
# ==============================
import huggingface_hub
if not hasattr(huggingface_hub, "HfFolder"):
    logger.warning("⚠️ Patching missing HfFolder in huggingface_hub...")
    huggingface_hub.HfFolder = type("HfFolder", (), {"get_token": lambda: None})

# ==============================
# 📦 Core Imports
# ==============================
# Ensure your FastAPI app is imported correctly
from main import app as fastapi_app

# ==============================
# 🚀 ZeroGPU Decorated Function
# ==============================
# The AST scanner will detect this. When the button is clicked, 
# ZeroGPU will dynamically allocate a GPU for this specific execution.
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
    logger.info("🚀 Starting J.A.R.V.I.S. Omni-Core server on port 7860...")
    
    # Start the unified FastAPI + Gradio application
    uvicorn.run(app, host="0.0.0.0", port=7860)
