from pypdf import PdfReader
from backend.service.rag.components.embedding.embedder import Embedder
from backend.service.rag.ingestion.chunker import Chunker
from backend.service.rag.components.vectorstore.faiss.vector_store import VectorStore

# RAG ingestion 파이프라인을 하나의 객체로 캡슐화
# 외부에서는 build()만 호출하지만 실제로 내부에서는
# 문서 로딩 → 청킹 → 임베딩 → 벡터DB 저장 여러 단계가 실행됨.
# 복잡한 내부 과정을 숨기고 하나의 메서드로 제공한다 → 캡슐화
# ingestion = 데이터를 시스템에 넣는 과정
# 여기서는 문서를 벡터화하여 DB에 저장하는 작업이 됨.
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
    
    # 추후 Loader를 따로 파일 만들어야 겠다.
    def load_documents(self):

        # 왜 PdfReader를 썼는지 찾아내야 한다..
        reader = PdfReader("backend/data/raw/pdf/북브리프_돈의심리학.pdf")
        docs = []

        for page in reader.pages:
            # 페이지 개수만큼 for문을 돌면서 한페이지의 텍스트를 추출
            text = page.extract_text("plain")

            #print("text : ", text)
            if text:
                docs.append(text)
        return docs
    
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
    

    