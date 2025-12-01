import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

conn = sqlite3.connect("student_info.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS info_vectors (
    id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    embedding BLOB NOT NULL
);
""")

entries = [
    ("Student Info", """
Alexandra Thompson, a 19-year-old computer science sophomore with a 3.7 GPA,
is a member of the programming and chess clubs who enjoys pizza, swimming, and hiking
in her free time in hopes of working at a tech company after graduating from the University of Washington.
"""),

    ("Club Info", """
The university chess club provides an outlet for students to come together and enjoy playing
the classic strategy game of chess. Members of all skill levels are welcome, from beginners learning
the rules to experienced tournament players. The club typically meets a few times per week to play casual games,
participate in tournaments, analyze famous chess matches, and improve members' skills.
"""),

    ("University Info", """
The University of Washington, founded in 1861 in Seattle, is a public research university
with over 45,000 students across three campuses in Seattle, Tacoma, and Bothell.
As the flagship institution of the six public universities in Washington state,
UW encompasses over 500 buildings and 20 million square feet of space,
including one of the largest library systems in the world.
"""),
]

for idx, (_, desc) in enumerate(entries, 1):
    emb = model.encode(desc).astype(np.float32)
    conn.execute(
        "INSERT OR REPLACE INTO info_vectors (id, description, embedding) VALUES (?, ?, ?)",
        (idx, desc.strip(), emb.tobytes())
    )

conn.commit()

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query = input("Enter your search text: ")
query_vec = model.encode(query).astype(np.float32)

rows = conn.execute("SELECT id, description, embedding FROM info_vectors").fetchall()

scores = []
for row in rows:
    emb = np.frombuffer(row[2], dtype=np.float32)
    sim = cosine_sim(query_vec, emb)
    scores.append((row[0], row[1][:90] + "...", sim))

top2 = sorted(scores, key=lambda x: x[2], reverse=True)[:2]

print("\nTop-2 similar entries:")
for idd, txt, s in top2:
    print(f"ID: {idd}, Sim: {s:.4f}")
    print(f"Text: {txt}\n")
