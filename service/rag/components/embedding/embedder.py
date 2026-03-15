#component = 시스템을 구성하는 하나의 부품
# 텍스트를 벡터로 변경하는 클래스
from sentence_transformers import SentenceTransformer

class Embedder:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        return self.model.encode(text)