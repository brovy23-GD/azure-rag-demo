"""Small deterministic lexical retrieval index for reproducible local testing."""
from __future__ import annotations
import json
import math
import re
from collections import Counter
from pathlib import Path

TOKEN = re.compile(r"[a-z0-9]+")
def tokens(s: str) -> list[str]:
    return TOKEN.findall(s.lower())

def chunks(text: str, size: int = 900, overlap: int = 120) -> list[str]:
    if not 0 <= overlap < size: raise ValueError("overlap must be less than size")
    clean = " ".join(text.split())
    if not clean: return []
    result=[]
    for start in range(0,len(clean),size-overlap):
        part=clean[start:start+size].strip()
        if part: result.append(part)
        if start+size >= len(clean): break
    return result

class Store:
    def __init__(self, path: Path):
        self.path=path
        self.items=json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []

    def add(self, source: str, text: str):
        if not source.strip(): raise ValueError("source required")
        self.items=[x for x in self.items if x["source"]!=source]
        self.items.extend({"source": source, "chunk": i, "text": c} for i,c in enumerate(chunks(text)))

    def save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        temp=self.path.with_suffix(".tmp")
        temp.write_text(json.dumps(self.items,indent=2),encoding="utf-8")
        temp.replace(self.path)

    def search(self, question: str, top_k: int = 3) -> list[dict]:
        query=set(tokens(question))
        if not query or not self.items:return []
        docs=[Counter(tokens(x["text"])) for x in self.items]
        df=Counter(t for d in docs for t in d)
        scored=[]
        for item,doc in zip(self.items,docs):
            score=sum((1+math.log(doc[t])) * math.log(1+(len(docs)+1)/(df[t]+1)) for t in query if doc[t])
            if score>0:scored.append({**item,"score":score})
        return sorted(scored,key=lambda x:(-x["score"],x["source"],x["chunk"]))[:top_k]
