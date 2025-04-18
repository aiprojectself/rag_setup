# parsers/doc_parser.py

import os
import subprocess
import tempfile
import platform
from docx import Document


def extract_text_from_doc(doc_path: str) -> str:
    """
    Platform-independent function to extract text from .doc or .docx files

    Args:
        doc_path: Path to the document file

    Returns:
        Extracted text content as string
    """
    ext = os.path.splitext(doc_path.lower())[1]

    # Step 1: Try python-docx for .docx files (works on all platforms)
    if ext == ".docx":
        try:
            doc = Document(doc_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            print(f"Error parsing .docx with python-docx: {e}")

    # Step 2: Try methods with external dependencies (platform-specific)
    current_os = platform.system()

    # macOS specific methods
    if current_os == "Darwin":
        # Try textutil (built-in to macOS)
        try:
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
                temp_txt_path = temp_file.name

            result = subprocess.run([
                'textutil', '-convert', 'txt', '-output', temp_txt_path, doc_path
            ], capture_output=True)

            if result.returncode == 0:
                with open(temp_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                os.remove(temp_txt_path)
                return content
        except Exception as e:
            print(f"macOS textutil error: {e}")

    # Windows specific methods
    elif current_os == "Windows":
        # Try using pywin32 if available
        try:
            import win32com.client

            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False

            # Get absolute path (required for Word)
            abs_path = os.path.abspath(doc_path)

            # Open the document
            doc = word.Documents.Open(abs_path)

            # Extract text
            text = doc.Content.Text

            # Close and quit Word
            doc.Close(SaveChanges=False)
            word.Quit()

            return text
        except Exception as e:
            print(f"Windows COM error: {e}")

    # Step 3: Cross-platform methods - try tools that might be installed

    # Try antiword
    try:
        result = subprocess.run(['antiword', doc_path], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"Antiword error: {e}")

    # Try catdoc
    try:
        result = subprocess.run(['catdoc', doc_path], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"Catdoc error: {e}")

    # Try LibreOffice/OpenOffice (available on all platforms)
    try:
        # Create a temp directory for output
        temp_dir = tempfile.mkdtemp()

        # Command name differs between systems
        soffice_commands = ['soffice', 'libreoffice', 'localc']
        success = False

        for cmd in soffice_commands:
            try:
                # Convert to txt using LibreOffice/OpenOffice
                result = subprocess.run([
                    cmd, '--headless', '--convert-to', 'txt:Text',
                    '--outdir', temp_dir, doc_path
                ], capture_output=True, timeout=30)

                if result.returncode == 0:
                    success = True
                    break
            except (subprocess.SubprocessError, FileNotFoundError):
                continue

        if success:
            # Read the converted text file
            txt_filename = os.path.basename(os.path.splitext(doc_path)[0] + ".txt")
            txt_path = os.path.join(temp_dir, txt_filename)

            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Clean up
                os.remove(txt_path)
                os.rmdir(temp_dir)

                return content
    except Exception as e:
        print(f"LibreOffice conversion error: {e}")
        # Clean up temp dir if it exists
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)

    # Step 4: Try conversion using a pure Python approach - docx2txt
    try:
        import docx2txt
        return docx2txt.process(doc_path)
    except Exception as e:
        print(f"docx2txt error: {e}")

    # Step 5: Try to identify what the file actually is
    try:
        if current_os != "Windows":  # 'file' command not available on Windows by default
            result = subprocess.run(['file', doc_path], capture_output=True, text=True)
            file_type = result.stdout
            print(f"File type detection: {file_type}")
    except Exception:
        pass

    return f"[ERROR] Could not extract text from {doc_path}. The file may be corrupted, password-protected, or not a valid Word document."