!pip install sentence-transformers faiss-cpu
!git clone https://github.com/xdevplatform/postman-twitter-api.git twitter_docs/postman-twitter-api-master
!ls twitter_docs/postman-twitter-api-master
import os, re

def chunk_document(text, source, max_tokens=250):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current, length = [], [], 0
    for sent in sentences:
        tokens = sent.split()
        if length + len(tokens) > max_tokens and current:
            chunks.append({"source": source, "text": " ".join(current)})
            current, length = [], 0
        current.append(sent)
        length += len(tokens)
    if current:
        chunks.append({"source": source, "text": " ".join(current)})
    return chunks

def load_docs(path):
    chunks = []
    file_count = 0
    for root, _, files in os.walk(path):
        if "/." in root:  # skip hidden folders
            continue
        for fname in files:
            if fname.endswith(".md"):  # only markdown files
                full = os.path.join(root, fname)
                try:
                    with open(full, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                    chunks.extend(chunk_document(text, full))
                    file_count += 1
                    print(f"Processed {file_count} files...", end="\r")
                except:
                    pass
    return chunks

chunks = load_docs("twitter_docs/postman-twitter-api-master")
print(f"\nTotal chunks created: {len(chunks)}")

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Prepare texts
texts = [c["text"] for c in chunks]

# Compute embeddings
embeddings = model.encode(texts, batch_size=16, show_progress_bar=True)
embeddings = embeddings.astype("float32")

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

print("FAISS index built successfully!")

def semantic_search(query, k=5):
    qvec = model.encode([query]).astype("float32")
    D, I = index.search(qvec, k)
    results = []
    for rank, (idx, dist) in enumerate(zip(I[0], D[0])):
        results.append({
            "rank": rank + 1,
            "score": float(dist),
            "source": chunks[idx]["source"],
            "text": chunks[idx]["text"]
        })
    return results

query = "How do I fetch tweets with expansions?"
results = semantic_search(query, k=5)

import json
print(json.dumps(results, indent=2))

import os, shutil

project_folder = "semantic_search_task1"
os.makedirs(project_folder, exist_ok=True)

shutil.copy("semantic_search.py", project_folder)
shutil.make_archive(project_folder, 'zip', project_folder)

from google.colab import files
files.download("semantic_search_task1.zip")







