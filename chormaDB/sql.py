import sqlite3
import numpy as np

# ------------------------------
# SETUP: sample table + vectors
# ------------------------------
conn = sqlite3.connect(":memory:")

# If you are using a custom SQLite vector extension,
# you may need something like:
# conn.enable_load_extension(True)
# conn.load_extension("your_vector_extension.so")

conn.execute("""
CREATE TABLE books_vectors (
    id        INTEGER PRIMARY KEY,
    title     TEXT NOT NULL,
    embedding BLOB NOT NULL
);
""")

# Helper to create a fake 384-dim embedding
def make_vec(value: float) -> bytes:
    return np.array([value] * 384, dtype=np.float32).tobytes()

# Sample book vectors (fake data)
book1_emb = make_vec(0.10)   # Book 1
book2_emb = make_vec(0.80)   # Book 2 (far away)
book3_emb = make_vec(0.14)   # Book 3 (close to Book 1)

conn.executemany(
    "INSERT INTO books_vectors (id, title, embedding) VALUES (?, ?, ?)",
    [
        (1, "Book 1: Intro to AI",       book1_emb),
        (2, "Book 2: Cooking with Artificial Intelligence", book2_emb),
        (3, "Book 3: Machine Learning",  book3_emb),
    ],
)
conn.commit()

# ------------------------------
# SEARCH: ask user for query text
# ------------------------------
def fake_text_embedding(text: str) -> bytes:
    """
    Demo: ignore text and just make a vector
    that is 'close' to Book 1 and Book 3.
    In real life, you would call your model here.
    """
    return np.array([0.15] * 384, dtype=np.float32).tobytes()

query_text = input("Enter your search text: ")
query_emb = fake_text_embedding(query_text)

# ------------------------------
# VECTOR SEARCH (top-2, cosine)
# ------------------------------
# NOTE: The exact SQL depends on your extension.
# This matches your original style:

import struct

def bytes_to_vec(b):
    return np.frombuffer(b, dtype=np.float32)

# Fetch all rows
rows = conn.execute("SELECT id, title, embedding FROM books_vectors").fetchall()

# Compute cosine similarity
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query_vec = np.frombuffer(query_emb, dtype=np.float32)
sims = [(row[0], row[1], cosine_sim(query_vec, bytes_to_vec(row[2]))) for row in rows]

# Sort by similarity descending
top2 = sorted(sims, key=lambda x: x[2], reverse=True)[:2]



# Use the computed top2 similarities and print id and title
print("Top-2 similar books:")
for id_, title, score in top2:
    print((id_, title))
# (fake sample output):
# Top-2 similar books:
# (1, 'Book 1: Intro to AI')
# (3, 'Book 3: Machine Learning')