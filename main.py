# RAG 전체 흐름 : PDFLoader → Chunker → Embedder → Retriever → Generator

# main.py
# 역할: 각 클래스를 조립해서 전체 RAG 파이프라인을 실행한다.

from service.rag.ingestion.index_builder import IndexBuilder
#from service.rag.components.vectorstore.faiss.vector_store import VectorStore
from service.rag.components.vectorstore.chroma.vector_store import VectorStore  # faiss → chroma
from service.rag.components.embedding.embedder import Embedder
from service.rag.rag_pipeline import RAGPipeline

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
embedder = Embedder()

# ── 목표 1. 벡터 DB 저장 데이터 확인 ──────────────────────────
print("\n[1] 벡터 DB 저장 현황")
store.print_documents()



# ── 목표 2. Retrieval + 유사도 점수 출력 ──────────────────────
print("\n[2] 검색 시작 (종료: exit)")
while True:

    query = input("\n질문: ").strip()
    if query.lower() == "exit":
        break

    query_vector = embedder.embed([query])[0]
    results      = store.search(query_vector, k=3)

    print(f"\n{'='*60}")
    print(f"  검색 결과 top-{len(results)}")
    print(f"{'='*60}")

    for i, r in enumerate(results):
        print(f"\n[{i+1}] PAGE {r['page']} | CHUNK {r['chunk']}")
        print(f"     거리(distance) : {r['distance']:.4f}")          # 낮을수록 유사
        print(f"     유사도(1-dist)  : {1 - r['distance']:.4f}")     # 높을수록 유사
        print(f"     내용 : {r['text'][:200]}")
        print("-" * 60)
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