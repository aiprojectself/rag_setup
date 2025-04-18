# utils/resume_retriever.py

from langchain_ollama import OllamaEmbeddings
from chromadb import PersistentClient
from typing import Dict

client = PersistentClient(path="chroma_db")
collection = client.get_collection(name="resumes")
embedding_fn = OllamaEmbeddings(model="nomic-embed-text")


def retrieve_matching_resumes(job_description: str, top_k: int = 50) -> Dict[str, dict]:
    query_embedding = embedding_fn.embed_query(job_description)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    metadatas = results["metadatas"][0]
    documents = results["documents"][0]

    grouped_by_resume = {}

    for metadata, content in zip(metadatas, documents):
        resume_id = metadata["resume_id"]

        if resume_id not in grouped_by_resume:
            grouped_by_resume[resume_id] = {
                "chunks": [],
                "metadata": metadata  # Keep one set of metadata (can update if needed)
            }

        grouped_by_resume[resume_id]["chunks"].append(content)

    return grouped_by_resume
