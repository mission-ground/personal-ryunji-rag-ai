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
    # 이미 생성된 embedder와 vector_store를 외부에서 주입받습니다.
    def __init__(self, loader: BaseLoader, embedder: Embedder, vector_store: VectorStore):
        
        self.loader   = loader
        self.embedder = embedder                                    # 1. 임베딩을 처리할 모델을 준비한다.        
        self.chunker  = Chunker(embedder=self.embedder)                 # 2. load 된 데이터를 청킹할 청커를 준비한다. 임베딩 모델 주입.
        self.vector_store = vector_store                               # 3. 처리된 문서 데이터를 저장할 벡터DB 준비한다.

    # build_index.py 파일에서 호출된 메서드가 호출되어 실제로 처리되는 곳
    # PDF 로딩 → 청킹 → 임베딩 → 벡터DB 저장 과정이 한 번에 실행되도록 만듦.
    # file_path에 기본값 None을 줍니다.
    def build_index(self, file_path: str = None):

        # 만약 인자가 들어오지 않았다면 기본 경로를 할당합니다.
        if file_path is None:
            file_path = "data/raw/pdf/북브리프_돈의심리학.pdf"
            print(f"--- 인자가 없어 기본 문서를 로드합니다: {file_path} ---")
            
        # 확장자에 따라 동적으로 로더 선택
        if file_path.endswith(".pdf"):
            print(f"--- PDF 로딩 시작: {file_path} ---")
            # PDF 전용 로더 사용 (기존에 주입된 loader가 PdfLoader라면 바로 사용)
            documents = self.loader.load(file_path)
        else:
            # 기존 텍스트 파일이나 다른 방식 처리
            print(f"--- 텍스트 로딩 시작: {file_path} ---")
            documents = self.load_documents(file_path)      # 1. 처리할 문서를 임베딩 처리하기 위해 로딩한다.
                              
        print("------------------ ", documents)
        chunks = self.chunk_documents(documents)                        #.2. 청킹
        vectors = self.embed_chunks(chunks)                             #.3. 벡터 DB 저장
        self.vector_store.add_documents(vectors, chunks)
        
        # [수정 포인트] 객체 대신 사람이 읽을 수 있는 요약 정보를 리턴합니다.
        summary = f"✅ 인덱싱 완료!\n"
        summary += f"- 총 청크 수: {len(chunks)}개\n"
        summary += f"- 저장 경로: {file_path}\n\n"
        summary += "--- 상위 3개 데이터 미리보기 ---\n"
        
        # 첫 3개 청크 내용만 살짝 보여주기
        for i, chunk in enumerate(chunks[:3]):
            content = chunk['text'][:50] + "..." if len(chunk['text']) > 50 else chunk['text']
            summary += f"[{i+1}] {content}\n"

        return summary
    
    def load_documents(self, path: str) -> list[str]:
        pages = self.loader.load(path)
        return self._remove_header(pages)

    # 검색 품질을 높이기 위해 추가된 부분
    # : 헤더 제거 후 저장한다.
    def _remove_header(self, pages: list[str], header_lines: int = 3) -> list[str]:
        if not pages:
            return pages
        header = "\n".join(pages[0].split("\n")[:header_lines])
        return [p[len(header):].strip() if p.startswith(header) else p for p in pages]
    
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
        return self.embedder.embed_documents(texts)
    
    def clean_text(self, text):
        return (
            text.replace("\u00a0", " ")
                .replace("\r", "\n")
                .strip()
        )

    