import chromadb
from chromadb.utils import embedding_functions

# Connection (from Section 1)
client = chromadb.Client()
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(  # Use get_or_create to avoid errors if run multiple times
    name="",
    embedding_function=embedding_function
)

collection.add(
    documents=[
        "A detective solves crimes in London.",
        "A romance about two lovers in Paris.",
        "A sci-fi adventure on Mars."
    ],
    ids=["book1", "book2", "book3"]
)

# Query
results = collection.query(query_texts=["A mystery story with detectives."], n_results=1)
print(results)  # Should return book1 with low distance