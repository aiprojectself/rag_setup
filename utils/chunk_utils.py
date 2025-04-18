from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


def chunk_file(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)


def get_file_id(file_path: str) -> str:
    directory = os.path.basename(os.path.dirname(file_path))
    filename = os.path.basename(file_path)
    return f"{directory}/{filename}"
