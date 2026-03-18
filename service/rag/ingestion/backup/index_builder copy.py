import pdfplumber
import fitz
from typing import Literal
from service.rag.components.embedding.embedder import Embedder
from service.rag.ingestion.chunker import Chunker
from service.rag.components.vectorstore.chroma.vector_store import VectorStore
from service.rag.ingestion.loader.base_loader import BaseLoader

class IndexBuilder:

    # 생성자, IndexBuilder 인스턴스가 생성되면 하위의 코드를 실행한다.
    # 작업 준비를 하는 것, 준비물 사놓기.
    def __init__(self):
        
        self.embedder = Embedder()                                      # 1. 임베딩을 처리할 모델을 준비한다.        
        self.chunker  = Chunker()                                       # 2. load 된 데이터를 청킹할 청커를 준비한다.
        self.vector_store = VectorStore()                               # 3. 처리된 문서 데이터를 저장할 벡터DB 준비한다.

    # build_index.py 파일에서 호출된 메서드가 호출되어 실제로 처리되는 곳
    # PDF 로딩 → 청킹 → 임베딩 → 벡터DB 저장 과정이 한 번에 실행되도록 만듦.
    def build_index(self):

        documents = self.load_documents()                               # 1. 처리할 문서를 임베딩 처리하기 위해 로딩한다.
        print("------------------ ", documents)
        chunks = self.chunk_documents(documents)                        #.2. 청킹
        vectors = self.embed_chunks(chunks)                             #.3. 벡터 DB 저장
        self.vector_store.add_documents(vectors, chunks)
        return self.embedder, self.vector_store
    
 
    # ──────────────────────────────────────────────────────────────
    # loader_type : "fitz" | "pdfplumber" (기본값 "pdfplumber")
    # pdf_path    : PDF 파일 경로 (기본값 유지)
    # ──────────────────────────────────────────────────────────────
    def load_documents(
        self,
        loader_type: Literal["fitz", "pdfplumber"] = "pdfplumber",
        pdf_path: str = "data/raw/pdf/북브리프_돈의심리학.pdf",
    ) -> list[str]:
 
        if loader_type == "fitz":
            return self._load_with_fitz(pdf_path)
        elif loader_type == "pdfplumber":
            return self._load_with_pdfplumber(pdf_path)
        else:
            raise ValueError(f"지원하지 않는 loader_type: '{loader_type}' — 'fitz' 또는 'pdfplumber' 중 선택하세요.")
    
    def load_documents(self, pdf_path: str = "data/raw/pdf/북브리프_돈의심리학.pdf") -> list[str]:
        return self.loader.load(pdf_path)
    
    def chunk_documents(self, documents):

        chunks = []
        for page, doc in enumerate(documents):

            print(f"\n========= PAGE {page+1} =========")
            doc_chunks = self.chunker.split(doc, page+1)
            chunks.extend(doc_chunks)
        return chunks
    
    # 임베딩 모델은 문자열 리스트를 받아야 한다.
    def embed_chunks(self, chunks):
        
        # 문자열 리스트로 변환하는 코드 추가.
        texts = [c["text"] for c in chunks]
        return self.embedder.embed(texts)
    
    def clean_text(self, text):
        return (
            text.replace("\u00a0", " ")
                .replace("\r", "\n")
                .strip()
        )

    