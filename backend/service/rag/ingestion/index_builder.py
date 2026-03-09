from pypdf import PdfReader
from backend.service.rag.components.embedding.embedder import Embedder
from backend.service.rag.ingestion.chunker import Chunker
from backend.service.rag.components.vectorstore.faiss.vector_store import VectorStore

#ingestion = 데이터를 시스템에 넣는 과정
class IndexBuilder:

    def __init__(self):
        
        self.embedder = Embedder()          
        self.chunker = Chunker()            # 2. load 된 데이터를 청킹할 청커를 준비한다.
        self.vector_store = VectorStore()   # 3. 처리된 문서 데이터를 저장할 벡터DB 준비한다.

    # main에서 호출된 메서드가 호출되어 실제로 처리되는 곳
    def build(self):

        documents = self.load_documents()                   # 1. 처리할 문서를 임베딩 처리하기 위해 로딩한다.
        chunks = self.chunk_documents(documents)
        vectors = self.embed_chunks(chunks)
        self.vector_store.add_documents(vectors, chunks)
        return self.embedder, self.vector_store
    
    # 추후 Loader를 따로 파일 만들어야 겠다.
    def load_documents(self):

        reader = PdfReader("backend/data/raw/pdf/북브리프_돈의심리학.pdf")
        docs = []

        for page in reader.pages:
            text = page.extract_text()

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
    

    