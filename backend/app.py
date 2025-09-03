import subprocess
import threading
import time
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

current_model = os.environ.get("DEFAULT_MODEL", "tinyllama")

# === FastAPI Setup ===
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Globals ===
current_model = "tinyllama"  # default
ollama_process = None
ollama_url = "http://localhost:11434"
model_check_timeout = 60  # seconds
ollama_lock = threading.Lock()


# === Start Ollama in background ===
def start_ollama():
    global ollama_process
    try:
        # Start `ollama serve` in the background
        ollama_process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("🚀 Ollama server started")
    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")


# === Wait for Ollama server to be ready ===
def wait_for_ollama_ready(timeout=60):
    print("⏳ Waiting for Ollama to be ready...")
    for _ in range(timeout):
        try:
            r = requests.get(f"{ollama_url}/api/tags")
            if r.status_code == 200:
                print("✅ Ollama is ready")
                return
        except:
            pass
        time.sleep(1)
    raise RuntimeError("Ollama did not start in time")


# === Download and preload a model ===
known_models = set()
def ensure_model(model_name):
    if model_name in known_models:
        return
    print(f"📦 Pulling model: {model_name}")
    try:
        r = requests.post(f"{ollama_url}/api/pull", json={"name": model_name}, timeout=180)
        r.raise_for_status()
        known_models.add(model_name)
        print(f"✅ Model '{model_name}' is ready.")
    except Exception as e:
        print(f"❌ Failed to pull model '{model_name}': {e}")
        raise

@app.on_event("startup")
def startup():
    start_ollama()
    wait_for_ollama_ready()
    for model in get_models()["models"]:
        ensure_model(model)


# === Request Models ===
class Prompt(BaseModel):
    prompt: str

class ModelSwitch(BaseModel):
    model: str


@app.post("/chat")
def chat(prompt: Prompt):
    with ollama_lock:
        try:
            res = requests.post(
                f"{ollama_url}/api/generate",
                json={"model": current_model, "prompt": prompt.prompt, "stream": False},
                timeout=60,
            )
            res.raise_for_status()
            response_data = res.json()
            return {"response": response_data.get("response", "No response")}
        except Exception as e:
            return {"error": str(e)}


@app.post("/switch_model")
def switch_model(req: ModelSwitch):
    global current_model
    with ollama_lock:
        current_model = req.model
        try:
            ensure_model(current_model)
            return {"message": f"✅ Switched to model: {current_model}"}
        except Exception as e:
            return {"error": str(e)}


@app.get("/current_model")
def get_current_model():
    return {"model": current_model}

@app.get("/models")
def get_models():
    return {"models": ["llama2", "gemma", "tinyllama"]}



@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("shutdown")
def shutdown_event():
    global ollama_process
    if ollama_process:
        print("🛑 Stopping Ollama...")
        ollama_process.terminate()
        ollama_process.wait()