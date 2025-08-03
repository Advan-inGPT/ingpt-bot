from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import requests

app = FastAPI()

# === Model download config ===
#MODEL_PATH = "../../models/deepseek-coder-1.3b.gguf"
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models"))
MODEL_FILE = "deepseek-coder-1.3b.gguf"
MODEL_URL = "https://huggingface.co/TheBloke/deepseek-coder-1.3B-instruct-GGUF/resolve/main/deepseek-coder-1.3b-instruct.Q4_K_M.gguf"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
#LLAMA_BIN_DIR = "../build/bin"
LLAMA_BIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build", "bin"))



# === Run on FastAPI startup ===
@app.on_event("startup")
def download_model_if_needed():
    os.makedirs(MODEL_DIR, exist_ok=True)
    if os.path.exists(MODEL_PATH):
        print(f"✅ Model already exists at {MODEL_PATH}")
    else:
        print(f"⬇️ Downloading model to {MODEL_PATH} ...")
        with requests.get(MODEL_URL, stream=True) as r:
            r.raise_for_status()
            with open(MODEL_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ Download complete!")




class Prompt(BaseModel):
    prompt: str

@app.post("/chat")
def chat(prompt: Prompt):
    full_prompt = f"### Instruction:\n{prompt.prompt}\n### Response:\n"
    try:
        result = subprocess.run(
            ["./llama-cli", "-m", MODEL_PATH, "-p", full_prompt],
            cwd=LLAMA_BIN_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout.split("### Response:")[-1].strip()
        return {"response": output}
    except Exception as e:
        return {"error": str(e)}
