from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import yaml

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

chunk_size = config["chunk_size"]
chunk_overlap = config["chunk_overlap"]


def chunk_file(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)


def get_file_id(file_path: str) -> str:
    directory = os.path.basename(os.path.dirname(file_path))
    filename = os.path.basename(file_path)
    return f"{directory}/{filename}"
