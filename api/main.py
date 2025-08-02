from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Linkify API funcionando!",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "linkify",
        "timestamp": "2025-08-02"
    }
