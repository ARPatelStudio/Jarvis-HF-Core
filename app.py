# 🚀 1. THE MONKEY PATCH MUST BE AT THE VERY TOP (Do not put anything above this)
import huggingface_hub
if not hasattr(huggingface_hub, "HfFolder"):
    huggingface_hub.HfFolder = type(
        "HfFolder",
        (),
        {
            "get_token": staticmethod(lambda: None),
            "save_token": staticmethod(lambda token: None),
            "delete_token": staticmethod(lambda: None),
        },
    )

import os

os.environ.setdefault("HF_HOME", "/tmp/hf")
os.environ.setdefault("TRANSFORMERS_CACHE", "/tmp/hf")
os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", "/tmp/hf")
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")

# 📦 2. Standard Imports
import logging
import gradio as gr
import uvicorn
from main import app as fastapi_app

# ==============================
# 🔧 Logging Setup
# ==============================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("JarvisApp")

# ==============================
# 🎨 Minimal Gradio UI
# ==============================
def ping_engine():
    return "🟢 CPU Engine Active. FastAPI is mounted. Embedder loads in background."

with gr.Blocks(theme=gr.themes.Monochrome(), title="J.A.R.V.I.S. Omni-Core") as demo:
    gr.Markdown("# 🟢 J.A.R.V.I.S. Omni-Core is Live")
    btn = gr.Button("Ping Engine Status")
    out = gr.Textbox(label="Status")
    btn.click(fn=ping_engine, inputs=[], outputs=out)

# ==============================
# 🔗 Safely Mount Gradio UI
# ==============================
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")

# ==============================
# 🏁 Entry Point
# ==============================
if __name__ == "__main__":
    logger.info("🚀 Starting J.A.R.V.I.S. Omni-Core server on port 7860...")
    uvicorn.run(app, host="0.0.0.0", port=7860, reload=False)
