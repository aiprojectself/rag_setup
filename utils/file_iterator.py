# utils/file_iterator.py

import os
from typing import Generator

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx"}


def iterate_files(folder_path: str) -> Generator[str, None, None]:
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file():
                ext = os.path.splitext(entry.name.lower())[1]
                if ext in SUPPORTED_EXTENSIONS:
                    yield entry.path

