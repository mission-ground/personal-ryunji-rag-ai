# query → embedding → vector search
import numpy as np

# RAG(검색 증강 생성) 시스템에서 질문과 관련된 정보를 
# 데이터베이스에서 찾아는 검색 기술 또는 엔진을 의미한다.
# 사람으로 치면 자료 찾는 사람
class Retriever:

    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str):

        query_vector = self.embedder.embed(query)

        query_vector = np.array([query_vector])

        documents = self.vector_store.search(query_vector)

        return documents