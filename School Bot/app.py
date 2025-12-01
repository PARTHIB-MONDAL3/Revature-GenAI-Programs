# --------------------------------------------------------------
# app.py – Streamlit chatbot (Ollama + ChromaDB – HYBRID RAG)
# --------------------------------------------------------------
import os
import shutil
from pathlib import Path
from typing import List, Tuple

import httpx
import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb

# --------------------------------------------------------------
# 1️⃣ Streamlit Config
# --------------------------------------------------------------
st.set_page_config(
    page_title="Course-Info Chatbot",
    page_icon="📚",
    layout="centered",
)

# --------------------------------------------------------------
# 2️⃣ Chroma Setup
# --------------------------------------------------------------

LEGACY_DB_PATH = Path("./chroma_db")

if LEGACY_DB_PATH.is_dir():
    try:
        shutil.rmtree(LEGACY_DB_PATH)
        st.info("🗑️ Old legacy `chroma_db` removed.")
    except PermissionError:
        st.warning("⚠️ Could not delete old `chroma_db` (locked). Reusing.")
    except Exception as e:
        st.error(f"❗️ Unexpected error: {e}")

client = chromadb.PersistentClient(path=str(LEGACY_DB_PATH))
COLLECTION_NAME = "courses"
collection = client.get_or_create_collection(name=COLLECTION_NAME)

embedder = SentenceTransformer("all-MiniLM-L6-v2")


def _embed(texts: List[str]) -> List[List[float]]:
    return embedder.encode(texts, show_progress_bar=False).tolist()


def add_documents(docs: List[str], metadatas: List[dict]) -> None:
    ids = [f"doc_{i}_{meta['source']}" for i, meta in enumerate(metadatas)]
    embeddings = _embed(docs)
    collection.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
    )


# --------------------------------------------------------------
# 2️⃣-B: HYBRID SEARCH UTILITIES
# --------------------------------------------------------------

def semantic_search(query_text: str, top_k: int = 5):
    q_emb = _embed([query_text])[0]
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents", "metadatas"],
    )
    return results["documents"][0], results["metadatas"][0]


def keyword_search(keyword: str, top_k: int = 50):
    """Return up to top_k docs that contain the keyword."""
    results = collection.query(
        query_texts=[keyword],   # lexical filter
        n_results=top_k,
        include=["documents", "metadatas"],
    )
    return results["documents"][0], results["metadatas"][0]


def hybrid_search(query: str) -> Tuple[List[str], List[dict]]:
    """
    HYBRID MODE:
    - semantic search (top 5)
    - keyword fallback for guaranteed recall
    - merge + dedupe
    """
    sem_docs, sem_meta = semantic_search(query, top_k=5)

    # If the question indicates listing/counting known entities
    needs_full_recall = any(
        key in query.lower()
        for key in ["batches", "batch", "list batches", "how many", "count"]
    )

    if needs_full_recall:
        key_docs, key_meta = keyword_search("Batch", top_k=50)
    else:
        key_docs, key_meta = [], []

    # Merge + dedupe
    merged_docs = []
    merged_meta = []

    for d, m in zip(sem_docs, sem_meta):
        if d not in merged_docs:
            merged_docs.append(d)
            merged_meta.append(m)

    for d, m in zip(key_docs, key_meta):
        if d not in merged_docs:
            merged_docs.append(d)
            merged_meta.append(m)

    return merged_docs, merged_meta


# --------------------------------------------------------------
# 3️⃣ Ollama
# --------------------------------------------------------------
def call_ollama(messages: List[dict]) -> str:
    resp = httpx.post(
        "http://127.0.0.1:11434/api/chat",
        json={
            "model": "mistral",
            "messages": messages,
            "temperature": 0.2,
            "stream": False,
        },
        timeout=60.0,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


# --------------------------------------------------------------
# 4️⃣ Auto-Load Multiple Static Files
# --------------------------------------------------------------
def load_static_file(filename: str):
    data_path = Path(__file__).parent / "data" / filename
    if not data_path.is_file():
        return

    raw = data_path.read_text(encoding="utf-8")
    chunks = [c.strip() for c in raw.split("\n\n") if c.strip()]
    metas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
    add_documents(chunks, metas)
    st.success(f"Loaded `{filename}`")


# Load ANY number of static files
static_files = ["courses.txt", "courses2.txt", "batches.txt"]  # you can add more

for f in static_files:
    load_static_file(f)


# --------------------------------------------------------------
# 5️⃣ UI
# --------------------------------------------------------------
st.title("📚 Course-Info Chatbot (Hybrid RAG – Ollama + ChromaDB)")

with st.expander("📁 Upload more course/batch files (.txt)"):
    uploaded = st.file_uploader(
        "Upload .txt files", type=["txt"], accept_multiple_files=True
    )
    if st.button("Process & Index"):
        if not uploaded:
            st.warning("Upload at least one .txt")
        else:
            for f in uploaded:
                raw = f.read().decode("utf-8")
                chunks = [c.strip() for c in raw.split("\n\n") if c.strip()]
                metas = [{"source": f.name, "chunk_index": i} for i in range(len(chunks))]
                add_documents(chunks, metas)
            st.success("Indexed successfully.")


# --------------------------------------------------------------
# 6️⃣ Chat History
# --------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


def render_chat():
    for role, content in st.session_state.messages:
        st.chat_message(role).write(content)


render_chat()


# --------------------------------------------------------------
# 7️⃣ Chat Input + HYBRID RAG
# --------------------------------------------------------------
if prompt := st.chat_input("Ask about a course, batch, fees, duration…"):
    st.session_state.messages.append(("user", prompt))
    st.chat_message("user").write(prompt)

    # Hybrid RAG
    docs, _ = hybrid_search(prompt)
    context = "\n\n".join(docs)

    system_msg = {
        "role": "system",
        "content": (
            "You are a course/batch assistant. Use ONLY the provided context. "
            "If info is missing, say so. If the query involves listing or counting, "
            "use all relevant context chunks."
        ),
    }
    user_msg = {
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {prompt}",
    }

    try:
        answer = call_ollama([system_msg, user_msg])
    except Exception as exc:
        answer = f"❗️ Ollama error: {exc}"

    st.session_state.messages.append(("assistant", answer))
    st.chat_message("assistant").write(answer)
