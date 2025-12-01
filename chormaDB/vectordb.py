import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Sample embeddings
docs = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])  # Document vectors
query = np.array([[0.2, 0.3]])  # Query vector

# Compute similarities
similarities = cosine_similarity(query, docs)[0]
ranked_indices = np.argsort(similarities)[::-1]
print("Top matches:", ranked_indices)
'''

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in text.split() if token not in stop_words]
    return ' '.join(tokens)

raw_text = "Hello World! This is a sample."
cleaned = preprocess_text(raw_text)
print("Cleaned:", cleaned)'''