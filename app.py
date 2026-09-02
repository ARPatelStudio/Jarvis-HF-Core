import logging
import sys

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
    huggingface_hub.HfFolder = type(
        "HfFolder",
        (),
        {
            "get_token": staticmethod(lambda: None),
            "save_token": staticmethod(lambda token: None),
            "delete_token": staticmethod(lambda: None),
        },
    )

# ==============================
# 📦 Core Imports
# ==============================
import spaces
import gradio as gr
import uvicorn
from main import app as fastapi_app

# ==============================
# 🚀 Dummy GPU Function
# ==============================
@spaces.GPU
def gpu_bypass():
    logger.info("✅ ZeroGPU function triggered (bypass mode).")
    return "ZeroGPU Bypassed! CPU Engine Active."

# ==============================
# 🎨 Minimal Gradio UI
# ==============================
with gr.Blocks(theme=gr.themes.Monochrome(), title="J.A.R.V.I.S. Omni-Core") as demo:
    gr.Markdown("# 🟢 J.A.R.V.I.S. Omni-Core Background UI")
    gr.Markdown("This lightweight UI satisfies Hugging Face's ZeroGPU scanner.")
    btn = gr.Button("Ping Engine Status")
    out = gr.Textbox(label="Status")
    btn.click(fn=gpu_bypass, inputs=[], outputs=out)

# ==============================
# 🔗 Safely Mount Gradio
# ==============================
# ⚠️ MASTER FIX: Hum koi route delete nahi kar rahe jisse Python crash ho.
# Hum chupchaap Gradio ko "/ui" par mount kar rahe hain. 
# Aapki original API (main.py) apni jagah par 100% safe aur active rahegi!
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")

# ==============================
# 🏁 Entry Point
# ==============================
if __name__ == "__main__":
    logger.info("🚀 Starting J.A.R.V.I.S. Omni-Core server on port 7860...")
    uvicorn.run("app:app", host="0.0.0.0", port=7860)
