#!/usr/bin/env python3
# Simple test to run FastAPI application

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Linkify Test")

@app.get("/")
async def root():
    return {"message": "Hello World from Linkify!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "test_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
