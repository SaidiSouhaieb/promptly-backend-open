import docx2txt

from tika import parser
from striprtf.striprtf import rtf_to_text


class ExtractContent:
    def __init__(self):
        self.file_types = {
            ".txt": self.extract_text_content,
            ".pdf": self.extract_pdf_content,
            ".docx": self.extract_docsx_content,
            ".doc": self.extract_doc_content,
            ".rtf": self.extract_rtf_content,
        }

    def extract_text_content(self, file_path):
        """Reads text from a txt file."""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def extract_pdf_content(self, file_path):
        """Reads text from a pdf file."""
        raw = parser.from_file(file_path)
        return raw["content"] if raw else ""

    def extract_docsx_content(self, file_path):
        """Reads text from a DOCX file."""
        return docx2txt.process(file_path)

    def extract_doc_content(self, file_path):
        """Reads text from a .doc file by checking RTF or using a basic fallback."""
        try:
            with open(file_path, "r", encoding="latin-1") as file:
                content = file.read()
                if content.strip().startswith("{\\rtf"):
                    return rtf_to_text(content)
                return content  # fallback: just return plain text (might be gibberish if it's truly .doc)
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from {file_path}: {e}")

    def extract_rtf_content(self, file_path):
        """Reads text from an RTF file using striprtf."""
        with open(file_path, "r", encoding="latin-1") as file:
            rtf_content = file.read()
        return rtf_to_text(rtf_content)

    def get_text_content(self, file_path):
        ext = file_path.split(".")[-1]
        ext = f".{ext}" if ext else ""

        if ext in self.file_types:
            return self.file_types[ext](file_path)
        else:
            with open(file_path, "r", encoding="latin-1") as file:
                first_line = file.readline()
                if first_line.strip().startswith("{\\rtf"):
                    return self.extract_rtf_content(file_path)
            raise ValueError(f"Unsupported file type: {ext}")
