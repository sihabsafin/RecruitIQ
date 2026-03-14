"""
utils/vector_store.py
Local ChromaDB + sentence-transformers for semantic resume-JD matching.
Uses whatever chromadb version crewai installed — no version pinning.
"""

from sentence_transformers import SentenceTransformer
from typing import List, Dict

_model = None
_client = None
_collection = None

MODEL_NAME = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "recruitiq_resumes"


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def _get_collection():
    global _client, _collection
    if _collection is None:
        import chromadb
        _client = chromadb.Client()
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def embed_text(text: str) -> List[float]:
    return _get_model().encode(text, normalize_embeddings=True).tolist()


def add_resume(candidate_id: str, resume_text: str, metadata: Dict):
    try:
        col = _get_collection()
        embedding = embed_text(resume_text[:2000])
        col.upsert(
            ids=[candidate_id],
            embeddings=[embedding],
            documents=[resume_text[:2000]],
            metadatas=[metadata],
        )
    except Exception:
        pass  # Vector store is optional — screening still works without it


def match_resume_to_jd(resume_text: str, jd_text: str) -> float:
    """Returns 0-100 similarity score using cosine similarity."""
    try:
        model = _get_model()
        r_emb = model.encode(resume_text[:2000], normalize_embeddings=True)
        j_emb = model.encode(jd_text[:2000], normalize_embeddings=True)
        cosine_sim = float((r_emb * j_emb).sum())
        return round((cosine_sim + 1) / 2 * 100, 1)
    except Exception:
        return 50.0  # neutral fallback


def search_similar_resumes(jd_text: str, top_k: int = 5) -> List[Dict]:
    try:
        col = _get_collection()
        if col.count() == 0:
            return []
        jd_emb = embed_text(jd_text[:2000])
        results = col.query(
            query_embeddings=[jd_emb],
            n_results=min(top_k, col.count()),
            include=["metadatas", "distances"],
        )
        out = []
        for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
            meta["similarity_score"] = round((1 - dist) * 100, 1)
            out.append(meta)
        return out
    except Exception:
        return []
