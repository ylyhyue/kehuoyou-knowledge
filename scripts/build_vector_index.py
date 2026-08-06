#!/usr/bin/env python3
"""
Build vector index for kehuoyou knowledge base.
Reads Markdown files from policies/ and iterations/, chunks them,
and stores embeddings into a local Chroma vector DB.
"""
import os
import sys
from pathlib import Path
from hashlib import sha256

# Use HuggingFace mirror for stable model download in China
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

try:
    import chromadb
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
except ImportError:
    print("Installing chromadb and sentence-transformers...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "chromadb", "sentence-transformers"])
    import chromadb
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


BASE_DIR = Path("/Users/yuelaiyuehao/Documents/workbuddy 设计创意空间/kehuoyou-knowledge")
DB_DIR = BASE_DIR / "data" / "vector_index"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list:
    """Simple sliding-window chunker."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) > chunk_size and current:
            chunks.append(current.strip())
            current = current[-overlap:] if overlap < len(current) else ""
        current += "\n\n" + para if current else para
    if current:
        chunks.append(current.strip())
    return chunks


def main():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(DB_DIR))
    embedding_fn = SentenceTransformerEmbeddingFunction(
        model_name="BAAI/bge-small-zh-v1.5",
        device="cpu",
    )
    collection = client.get_or_create_collection(
        name="kehuoyou_knowledge",
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"},
    )

    md_files = list((BASE_DIR / "policies").glob("*.md")) + list((BASE_DIR / "iterations").glob("*.md"))
    docs, ids, metas = [], [], []
    for fp in md_files:
        text = fp.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            doc_id = sha256(f"{fp.name}:{i}".encode()).hexdigest()[:16]
            docs.append(chunk)
            ids.append(doc_id)
            metas.append({"source": fp.name, "chunk_index": i})

    if docs:
        collection.upsert(documents=docs, ids=ids, metadatas=metas)
        print(f"Indexed {len(docs)} chunks from {len(md_files)} files into {DB_DIR}")
    else:
        print("No documents found to index.")


if __name__ == "__main__":
    main()
