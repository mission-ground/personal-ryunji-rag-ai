from api.schemas import QuestionRequest, QuestionResponse
from fastapi import APIRouter, HTTPException
from service.rag.rag_pipeline  import RAGPipeline

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "ok"
    }

# API 엔드포인트(Controller 역할) : 검색기능
@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    
    try:
        results = RAGPipeline.ask(request.query, k=3)
        return {
              "status": "success"
            , "results": results
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"검색 처리 중 오류가 발생했습니다: {e}"
        )