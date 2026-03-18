import fitz
from service.rag.ingestion.loader.base_loader import BaseLoader
 
 
class FitzLoader(BaseLoader):
 
    def load(self, pdf_path: str) -> list[str]:
        docs = []
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text = page.get_text("text")
                if text and text.strip():
                    docs.append(text.strip())
        return docs
 