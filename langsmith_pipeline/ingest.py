"""
ingest.py
---------
One-time script to load all 77 KB chunks into a local Chroma vector store.

Run this ONCE before run_scenarios.py. If you ever update the KB, delete the
chroma_db/ folder and re-run this.

Embeddings: sentence-transformers/all-MiniLM-L6-v2 (free, runs locally on CPU)
Vector store: ChromaDB (file-based, no server needed)
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# Path to the 77 KB .txt files (relative to this script)
KB_DIR = Path(__file__).parent.parent / "kb"

# Where the Chroma vector store will live
CHROMA_DIR = Path(__file__).parent / "chroma_db"


def ingest():
    print(f"Loading KB files from: {KB_DIR}")

    if not KB_DIR.exists():
        raise FileNotFoundError(
            f"KB folder not found at {KB_DIR}. "
            f"Make sure you've copied the 77 .txt files into a 'kb/' folder "
            f"in the project root."
        )

    # Load every .txt file into a LangChain Document object
    documents = []
    for filepath in sorted(KB_DIR.glob("*.txt")):
        loader = TextLoader(str(filepath), encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            # Tag each chunk with its filename so traces show provenance
            doc.metadata["source"] = filepath.name
        documents.extend(docs)

    print(f"Loaded {len(documents)} documents")

    if len(documents) == 0:
        raise ValueError("No .txt files found in the kb/ folder.")

    # Embedding model: small, fast, free, runs on your laptop CPU
    # First time you run this it will download ~80MB of model weights
    print("Loading embedding model (first run downloads ~80MB)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Build the vector store and save to disk
    print(f"Building Chroma DB at: {CHROMA_DIR}")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    print(f"\n✅ Ingestion complete. {len(documents)} chunks indexed and saved.")
    print(f"   Vector store location: {CHROMA_DIR}")


if __name__ == "__main__":
    ingest()
