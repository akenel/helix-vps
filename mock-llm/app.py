# mock-llm/app.py
# Tiny FastAPI service that simulates a real LLM endpoint.
# It responds quickly and accepts a JSON body with "prompt" and returns a faux "generation".
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time, hashlib

app = FastAPI(title="Mock LLM - lightweight simulator")

class Prompt(BaseModel):
    prompt: str
    max_tokens: int = 64

@app.post("/v1/generate")
async def generate(p: Prompt):
    # simulate a tiny processing delay depending on prompt length
    delay = min(2.0, max(0.1, len(p.prompt) * 0.01))
    time.sleep(delay)
    # produce deterministic fake 'text' based on prompt hash
    digest = hashlib.sha1(p.prompt.encode("utf-8")).hexdigest()
    fake_text = f"SIMULATED_RESPONSE for: {p.prompt[:120]} ... (id={digest[:8]})"
    return {
        "id": digest,
        "object": "text_completion",
        "choices": [
            {"text": fake_text, "index": 0, "finish_reason": "length"}
        ],
        "usage": {"prompt_tokens": len(p.prompt.split()), "completion_tokens": p.max_tokens}
    }
@app.get("/health")
async def health():
    return {"status": "healthy"}