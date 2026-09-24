"""Local-first RAG API. Optional Azure generation is enabled only by explicit configuration."""
from __future__ import annotations
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .retrieval import Store

app = FastAPI(title="Azure RAG Demo", version="0.1.0")
store = Store(Path(os.getenv("RAG_INDEX_PATH", "data/index.json")))

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)

@app.get("/health")
def health():
    return {"status": "ok", "documents": len(store.items)}

@app.post("/ask")
def ask(payload: AskRequest):
    matches = store.search(payload.question, payload.top_k)
    if not matches:
        return {"answer": "No relevant indexed passages found.", "mode": "local-extractive", "sources": []}
    sources = [{"source": m["source"], "chunk": m["chunk"], "score": round(m["score"], 4), "text": m["text"]} for m in matches]
    if os.getenv("RAG_GENERATION_MODE", "local") == "azure":
        try:
            from .azure_generation import generate
            answer = generate(payload.question, sources)
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        return {"answer": answer, "mode": "azure-generated", "sources": sources}
    # Extractive local mode makes no fabricated model claims and requires no cloud credentials.
    return {"answer": "\n\n".join(f'[{i}] {item["text"]}' for i,item in enumerate(sources,1)),
            "mode": "local-extractive", "sources": sources}
