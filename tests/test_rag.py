from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.retrieval import Store,chunks
from scripts.ingest import ingest

def test_chunks_overlap_and_empty():
    assert chunks("",size=8,overlap=2)==[]
    assert chunks("abcdefghij",size=8,overlap=2)==["abcdefgh","ghij"]

def test_ingest_and_citations(tmp_path):
    d=tmp_path/"docs";d.mkdir();(d/"guide.md").write_text("Azure search retrieves document passages.")
    index=tmp_path/"index.json"
    assert ingest(d,index)==1
    store=Store(index);matches=store.search("Azure retrieves")
    assert matches and matches[0]["source"]=="guide.md"
    assert store.search("unrelatedterm")==[]

def test_api_uses_index(tmp_path,monkeypatch):
    from app import main
    index=tmp_path/"index.json";store=Store(index);store.add("reference.txt","Docker containers package applications.");store.save()
    monkeypatch.setattr(main,"store",Store(index))
    monkeypatch.setenv("RAG_GENERATION_MODE","local")
    c=TestClient(app)
    assert c.get("/health").json()["documents"]==1
    reply=c.post("/ask",json={"question":"Docker containers?"})
    assert reply.status_code==200
    assert reply.json()["sources"][0]["source"]=="reference.txt"
    assert c.post("/ask",json={"question":""}).status_code==422

def test_azure_requires_explicit_credentials(tmp_path,monkeypatch):
    from app import main
    s=Store(tmp_path/"idx.json");s.add("a.txt","Azure deployment uses cloud resources.")
    monkeypatch.setattr(main,"store",s)
    monkeypatch.setenv("RAG_GENERATION_MODE","azure")
    for key in ("AZURE_OPENAI_ENDPOINT","AZURE_OPENAI_API_KEY","AZURE_OPENAI_DEPLOYMENT"):
        monkeypatch.delenv(key,raising=False)
    assert TestClient(app).post("/ask",json={"question":"Azure deployment"}).status_code==503
