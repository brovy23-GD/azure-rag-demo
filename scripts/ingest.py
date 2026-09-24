"""Ingest .txt and .md documents from a directory into the local retrieval index."""
import argparse
from pathlib import Path
from app.retrieval import Store

def ingest(input_dir:Path,index:Path) -> int:
    if not input_dir.is_dir():raise ValueError(f"Input directory does not exist: {input_dir}")
    files=sorted(p for p in input_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".md",".txt"})
    store=Store(index)
    for f in files:
        if f.stat().st_size>2_000_000:raise ValueError(f"File too large: {f}")
        store.add(str(f.relative_to(input_dir)),f.read_text(encoding="utf-8"))
    store.save()
    return len(files)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,default=Path("sample_docs"))
    parser.add_argument("--index",type=Path,default=Path("data/index.json"))
    args=parser.parse_args()
    print(f"Indexed {ingest(args.input,args.index)} files at {args.index}")
