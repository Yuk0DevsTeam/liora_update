import os
import pymongo
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np

# MongoDB setup
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://root:example@localhost:27018/")
DB_NAME = "vector_db"
COLLECTION_NAME = "pdf_contexts"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def pdf_to_chunks(pdf_path, chunk_size=500):
    reader = PdfReader(pdf_path)
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    # Split text into chunks
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def store_pdf_contexts(pdf_path):
    chunks = pdf_to_chunks(pdf_path)
    print(f"Storing {len(chunks)} chunks from {pdf_path} into MongoDB...")
    for idx, chunk in enumerate(chunks):
        print(f"Processing chunk {idx + 1}/{len(chunks)}")
        embedding = model.encode(chunk).tolist()
        collection.insert_one({
            "text": chunk,
            "embedding": embedding
        })

def get_related_context(user_message, top_k=1):
    user_embedding = model.encode(user_message)
    docs = list(collection.find({}, {"text": 1, "embedding": 1}))
    if not docs:
        return ""

    def cosine_sim(a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    scored = [
        (doc["text"], cosine_sim(user_embedding, doc["embedding"]))
        for doc in docs
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return "\n".join([s[0] for s in scored[:top_k]])


if __name__ == "__main__":
    # Example usage
    pdf_path = "example_book.pdf"
    store_pdf_contexts(pdf_path)