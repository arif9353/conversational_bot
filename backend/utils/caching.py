import hashlib
import numpy as np
from google import genai
import time
from collections import deque
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Initialize Gemini Client
# ============================================================
client = genai.Client()

# ============================================================
# In-Memory Caches
# ============================================================
exact_cache = {}         # key: hash(query) → response
semantic_cache = {}      # key: hash(query) → {query, embedding, response}

SIM_THRESHOLD = 0.80      # semantic similarity threshold
MAX_CACHE_SIZE = 100      # prevent memory overflow


# ============================================================
# Helper: Hash key for exact cache
# ============================================================
def make_key(query: str) -> str:
    normalized = query.strip().lower()
    return hashlib.sha256(normalized.encode()).hexdigest()


# ============================================================
# Helper: Cosine Similarity
# ============================================================
def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ============================================================
# Helper: Get embedding vector (Gemini)
# ============================================================
def get_embedding(text: str) -> np.ndarray:
    """
    Returns a numpy array embedding from Gemini.
    """
    try:
        response = client.models.embed_content(
            model="gemini-embedding-2-preview",
            contents=text
        )

        embedding = response.embeddings[0].values
        return np.array(embedding, dtype=np.float32)

    except Exception as e:
        print("Embedding error:", e)
        # fallback safe vector
        return np.zeros(768, dtype=np.float32)


# ============================================================
# 1️⃣ Hybrid Cache Lookup
# ============================================================
def get_cached_response(query: str):
    """
    Returns:
        • LLM response (str) if cache hit
        • None if exact + semantic cache miss
    """

    key = make_key(query)

    # -------------------------
    # 1: Exact Cache Lookup
    # -------------------------
    if key in exact_cache:
        print("\n\nResponse returned from exact cache\n\n")
        return exact_cache[key]

    # -------------------------
    # 2: Semantic Cache Lookup
    # -------------------------
    try:
        query_emb = get_embedding(query)
    except Exception:
        return None

    best_sim = -1
    best_response = None

    for entry in semantic_cache.values():
        sim = cosine_sim(query_emb, entry["embedding"])
        print(f"\nSimilarity: {sim}\n")

        if sim > best_sim:
            best_sim = sim
            best_response = entry["response"]

    if best_sim >= SIM_THRESHOLD:
        print("\n\nResponse returned from semantic cache\n\n")
        return best_response  # semantic match hit

    # No hit
    return None


# ============================================================
# 2️⃣ Store Cache (Exact + Semantic)
# ============================================================
def store_cache(query: str, llm_response: str):
    """
    Stores the LLM response into:
      • exact cache
      • semantic cache (embedding-based)
    """

    key = make_key(query)

    # -------------------------
    # Prevent cache overflow (LRU-like)
    # -------------------------
    if len(exact_cache) >= MAX_CACHE_SIZE:
        exact_cache.pop(next(iter(exact_cache)))

    if len(semantic_cache) >= MAX_CACHE_SIZE:
        semantic_cache.pop(next(iter(semantic_cache)))

    embedding = get_embedding(query)

    # Store exact match
    exact_cache[key] = llm_response

    # Store semantic entry
    semantic_cache[key] = {
        "query": query,
        "embedding": embedding,
        "response": llm_response
    }

    print("\n\nResponse stored in the caches\n\n")

    return True