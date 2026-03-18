import pdfplumber
from service.rag.ingestion.loader.base_loader import BaseLoader
 
 
class PdfplumberLoader(BaseLoader):
 
    def load(self, pdf_path: str) -> list[str]:
        docs = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    docs.append(text.strip())
        return docs
 