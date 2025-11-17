# kautilya_task1
Semantic Search on Twitter API Documentation

This project implements a semantic search engine over the Postman Twitter API documentation using Sentence Transformers and FAISS.

✅ Features

Extracts and chunks Markdown documentation

Generates embeddings using all-MiniLM-L6-v2

Builds a FAISS vector index for fast similarity search

Allows command-line querying:

python semantic_search.py --query "How do I fetch tweets with expansions?"

📂 Project Workflow

Clone the Postman Twitter API documentation

Load and chunk .md files

Compute embeddings

Store and search using FAISS

Return top-k most relevant documentation snippets

🧪 Example Query
Query: "How do I fetch tweets with expansions?"


Returns the most relevant chunks from the documentation.

📦 Requirements

Python 3.8+

sentence-transformers

faiss-cpu

numpy

Install using:

pip install -r requirements.txt

▶ Usage

Run semantic search:

python semantic_search.py --query "your search text here"

📁 Repository Structure
├── semantic_search.py
├── README.md
├── twitter_docs/
├── embeddings/
└── index.faiss

✨ Purpose

This project lets you search technical documentation semantically, not just by keywords — making it easier to find relevant API explanations.
