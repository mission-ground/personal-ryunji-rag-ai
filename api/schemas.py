from pydantic import BaseModel, Field

# FastAPI에서 JSON 요청/응답을 Python 객체처럼 다루게 해주는 핵심 도구
# 요청 Body로 들어오는 JSON은 query라는 문자열 값을 가져야 한다
# DTO 정의(Request Body 데이터 구조)
# 라는 데이터 설계도 / DTO 클래스야.
class QuestionRequest(BaseModel):
    query: str = Field(..., min_length=1, description="사용자 질문")


class SearchResult(BaseModel):
    page: int
    chunk: int
    similarity: float
    content: str


class QuestionResponse(BaseModel):
    status: str
    results: list[SearchResult]