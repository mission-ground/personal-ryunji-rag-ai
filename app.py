# app.py의 역할: 각 클래스를 조립해서 전체 RAG 파이프라인을 실행한다.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service.rag.ingestion.index_builder import IndexBuilder
#from service.rag.components.vectorstore.faiss.vector_store import VectorStore
from service.rag.components.vectorstore.chroma.vector_store import VectorStore  # faiss → chroma
from service.rag.components.embedding.embedder import Embedder
from service.rag.rag_pipeline import RAGPipeline

print("----------------------------------------------------------------------")
print("******************** 5주차 개발 : RAG 파이프라인 시작 ********************")
print("----------------------------------------------------------------------")

# 1. 초기화 (Spring의 ApplicationContext 로드 시점과 유사), 이 녀석은 알고보니 디스패처 서블릿이었다!
app = FastAPI()

# 2. 전역 변수로 관리(실제로는 DI 컨테이너를 쓰는 게 좋음, 추후 수정하도록 하고 우선은 이렇게 시작한다.)
store = VectorStore()
embedder = Embedder()

# 3. DTO 정의(Request Body 데이터 구조)
class QuestionRequest(BaseModel):
    query: str

# 4. API 엔드포인트(Controller 역할)
@app.post("/ask")
async def ask_question(request : QuestionRequest) : 
    
    # strip()은 trim()과 같다.
    query = request.query.strip();
    if not query:
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")
    
    try:
        
        # 5. 비즈니스 로직(현재는 검색 단계까지 구현됨)
        # 5.1. 질문을 벡터로 변환
        query_vector = embedder.embed([query])[0]
        
        # 5.2. 벡터 DB 검색
        results = store.search(query_vector, k=3)
        
        # 6. 결과 반환(JSON 형태로 자동 변환됨)
        return {
              "status"  : "success"
            , "results" : [
                {
                     "page"       : r['page']
                   , "chunk"      : r['chunk']
                   , "similarity" : 1 - r['distance']
                   , "content"    : r['text']
                } for r in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
# 서버 실행 가이드: 터미널에서 `uvicorn app:app --reload` 실행












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
