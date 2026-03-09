# RAG 전체 흐름 : PDFLoader → Chunker → Embedder → Retriever → Generator

# main.py
# 역할: 각 클래스를 조립해서 전체 RAG 파이프라인을 실행한다.

from backend.service.rag.ingestion.index_builder import IndexBuilder
from backend.service.rag.components.vectorstore.faiss.vector_store import VectorStore
from backend.service.rag.components.embedding.embedder import Embedder
from backend.service.rag.rag_pipeline import RAGPipeline

#1. 데이터 로드 → 청킹 → 임베딩 → 벡터DB 저장 → 검색 → 답변 생성

print("=" * 100)
print("1주차 개발 : RAG 파이프라인 시작")
print("=" * 100)
# 1. 인덱스 생성
# RAG에서 인덱스 생성 = 데이터를 검색 가능하게 준비하는 과정
# 1.1 ├ PDF 읽기
# 1.2 ├ Chunk 생성
# 1.3 ├ Embedding 생성
# 1.4 └ VectorDB 저장
store = VectorStore()
store.load()

embedder = Embedder()

while True:

    query = input("질문: ")

    query_vector = embedder.embed([query])[0]

    results = store.search(query_vector)

    for r in results:

        print(r["text"])
# 1주차 내용은 위에까지. 아래는 무시할 것.

# 1️⃣ 벡터 DB 내용 확인

# 2. RAG 파이프라인 생성
# 2.1 ├ query
# 2.2 ├ embedding
# 2.3 ├ vector search
# 2.4 ├ context 생성
# 2.5 └ LLM 호출
#rag = RAGPipeline(embedder, store)

# 3. 질문 반복
#while True:

    #query = input("질문: ")

    #answer = rag.ask(query)

    #print("답변:", answer)