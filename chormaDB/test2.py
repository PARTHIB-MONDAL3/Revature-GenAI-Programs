import chromadb
from chromadb.utils import embedding_functions

# Step 1: Create a client connection (local by default)
client = chromadb.Client()

# Step 2: Set up an embedding function (turns text into vectors)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # A small, fast model
)

# Step 3: Create a collection (where data is stored)
collection = client.create_collection(
    name="my_first_collection",
    embedding_function=embedding_function
)

print("Connected to Chroma and created collection 'my_first_collection'!")