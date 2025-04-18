from chromadb import PersistentClient
from langchain_ollama import OllamaEmbeddings
import yaml

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

chromadb_path = config["chromadb_path"]
embedding_model = config["embedding_model"]

client = PersistentClient(path=chromadb_path)
embedding_fn = OllamaEmbeddings(model=embedding_model)
collection = client.get_or_create_collection(name="client1")


def store_chunks(chunks, file_id, metadata):
    # Step 1: Delete existing chunks for the file_id
    existing = collection.get(where={"file_id": file_id})
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # Step 2: Embed new chunks
    embeddings = embedding_fn.embed_documents(chunks)

    # Step 3: Prepare and insert new chunk data
    ids = []
    metadatas = []
    for idx, chunk in enumerate(chunks):
        ids.append(f"{file_id}_chunk_{idx}")
        chunk_metadata = metadata.copy()
        chunk_metadata.update({
            "file_id": file_id,
            "chunk_index": idx
        })
        metadatas.append(chunk_metadata)

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


