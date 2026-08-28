import uvicorn
from main import app

if __name__ == "__main__":
    # Hugging Face hamesha port 7860 par traffic bhejta hai
    uvicorn.run("main:app", host="0.0.0.0", port=7860)
