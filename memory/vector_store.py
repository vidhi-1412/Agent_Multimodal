import chromadb
from chromadb.config import Settings
import json
import os
import hashlib
from datetime import datetime

# Initialize ChromaDB client (persistent storage)
CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")

_client = None
_collection = None

def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client

def get_collection(name="supplier_memory"):
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


def store_result(query: str, result: str, metadata: dict = None):
    """Store a query-result pair in ChromaDB for future retrieval."""
    collection = get_collection()
    doc_id = hashlib.md5(f"{query}{datetime.now().isoformat()}".encode()).hexdigest()

    meta = {
        "query": query[:500],
        "timestamp": datetime.now().isoformat(),
        "result_preview": result[:300] if result else "",
    }
    if metadata:
        meta.update({k: str(v) for k, v in metadata.items()})

    collection.add(
        documents=[query],
        metadatas=[meta],
        ids=[doc_id]
    )
    return doc_id


def search_similar(query: str, n_results: int = 3):
    """Search ChromaDB for similar past queries."""
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return []

    try:
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count)
        )
        output = []
        if results and results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                distance = results["distances"][0][i] if results.get("distances") else 1.0
                similarity = round(1 - distance, 3)
                output.append({
                    "past_query": doc,
                    "result_preview": meta.get("result_preview", ""),
                    "timestamp": meta.get("timestamp", ""),
                    "similarity": similarity
                })
        return output
    except Exception as e:
        print(f"[ChromaDB Search Error]: {e}")
        return []


def get_all_history(limit: int = 20):
    """Retrieve recent conversation history from ChromaDB."""
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return []

    try:
        results = collection.get(limit=limit, include=["documents", "metadatas"])
        history = []
        for i, doc in enumerate(results["documents"]):
            meta = results["metadatas"][i]
            history.append({
                "query": doc,
                "result_preview": meta.get("result_preview", ""),
                "timestamp": meta.get("timestamp", ""),
            })
        history.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return history[:limit]
    except Exception as e:
        print(f"[ChromaDB History Error]: {e}")
        return []


def clear_memory():
    """Clear all stored memory from ChromaDB."""
    client = get_client()
    try:
        client.delete_collection("supplier_memory")
        global _collection
        _collection = None
        return True
    except Exception as e:
        print(f"[ChromaDB Clear Error]: {e}")
        return False


def get_stats():
    """Get memory statistics."""
    collection = get_collection()
    count = collection.count()
    return {
        "total_entries": count,
        "queries_stored": count,
        "db_path": CHROMA_PATH
    }