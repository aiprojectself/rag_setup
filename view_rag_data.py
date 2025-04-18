from chromadb import PersistentClient
import yaml

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

chromadb_path = config["chromadb_path"]
client = PersistentClient(path=chromadb_path)

# List available collections
collections = client.list_collections()
print("Collections:", [col.name for col in collections])

# Load the collection (update with your actual collection name)
collection = client.get_collection(name="client1")  # replace with your collection name

# Fetch all documents
results = collection.get(include=["documents", "metadatas"])
for i in range(len(results["documents"])):
    print(f"\n--- Document {i+1} ---")
    print("ID:", results["ids"][i])
    # print("Text:", results["documents"][i])
    print("Metadata:", results["metadatas"][i])
