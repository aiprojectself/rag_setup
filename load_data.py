from utils.file_iterator import iterate_files
from parsers.text_extractor import extract_text

from utils.chunk_utils import chunk_file, get_file_id
from database.chroma_store import store_chunks
import yaml

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

data_directory = config["data_directory"]

for file_path in iterate_files(data_directory):
    try:
        print(f"Processing: {file_path}")
        text = extract_text(file_path)
        chunks = chunk_file(text)
        file_id = get_file_id(file_path)
        metadata = {
            "archive": False,
            "blocked": False
        }
        store_chunks(chunks, file_id, metadata)
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

