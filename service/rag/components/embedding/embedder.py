#component = 시스템을 구성하는 하나의 부품
# 텍스트를 벡터로 변경하는 클래스
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class Embedder:

   #def __init__(self, model_name="all-MiniLM-L6-v2"):
   # 성희가 물어봤던 부분이었나? 왜 이 모델을 썼냐고 했었던 것 같은데.
   # BAAI/bge-m3 모델은 현재 오픈소스 임베딩 모델 중 한국어 성능이 가장 좋은 녀석 중 하나래.
   # 1) 다국어 지원 : 한국어 처리가 매우 매끄러움.
   # 2) 멀티 기능   : 나중에 'Dense Retrieval' 외에 'Sparse Retrieval(키워드 기반)' 기능까지 확장할 수 있는 모델이다.
    def __init__(self, model_name="BAAI/bge-m3"):
        
        # 모델 로딩은 무거운 작업이라 생성자에서 하는 게 정석이라 한다.
        # 당연한건데 이해 못했었음. 메서드 호출될 때마다 생성하면 비효율적.
        # 이 클래스가 로드되는 시점 한번만 실행.
        self.model = SentenceTransformer(model_name)

    # 1. 여러 개를 한 번에 변환할 때 (Batch 처리용)
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)
    
    # 2. 질문 하나만 변환할 때 (단일 처리용)
    def embed_query(self, text: str) -> np.ndarray:
        
        # 내부적으로 리스트로 감싸서 보내고, 결과에서 0번째를 꺼내서 반환
        return self.model.encode([text])[0]