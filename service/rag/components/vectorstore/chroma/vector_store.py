import chromadb
import logging
from typing import List, Dict, Any

class VectorStore:

    def __init__(self):
        
        # 유사도가 음수 
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(  name="documents"
                                                               , metadata={"hnsw:space": "cosine"}  # 추가
                                                               )
        self.current_id = self.collection.count()

    def add_documents(self, vectors, docs):
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for i, doc in enumerate(docs):
            ids.append(str(self.current_id))
            embeddings.append(vectors[i])
            documents.append(doc["text"])
            metadatas.append({
                "page": doc["page"],
                "chunk": doc["chunk"]
            })
            self.current_id += 1

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def save(self):
        pass

    def print_documents(self):
        data = self.collection.get()

        print("\n===== VECTOR COUNT =====")
        print(self.collection.count())

        print("\n===== DOCUMENTS =====\n")

        for i in range(len(data["ids"])):
            print(f"ID: {data['ids'][i]}")
            print(f"PAGE: {data['metadatas'][i]['page']} | CHUNK: {data['metadatas'][i]['chunk']}")
            print(data["documents"][i])
            print("-" * 60)

    # 검색
    # : 유사도 임계값(threshold)를 설정함.
    """
        검색 로직 - 결과가 없을 경우의 처리와 데이터 구조 최적화
    """
    def search(self, query_vector : List[float], k : int = 3, threshold: float = 0.4) -> List[Dict[str, Any]]: # threshold 추가
        
        try:
            results = self.collection.query(
                  query_embeddings=[query_vector]
                , n_results = k
            )

            # 결과가 아예 없는 경우 방어 코드를 통해 [](빈 리스트)를 넘긴다.
            if not results or not results["documents"] or not results["documents"][0]:
                return []
            
            output = []
            # results["distances"][0] 등의 리스트를 zip으로 묶으면 훨씬 '파이썬'스럽고 깔끔합니다.
            for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
                
                similarity = 1 - dist
                if similarity >= threshold:
                    output.append({
                          "text": doc
                        , "page": meta.get("page")
                        , "chunk": meta.get("chunk")
                        , "similarity": round(similarity, 4)
                    })
            
            # 유사도 높은 순으로 정렬 (이미 되어있겠지만 명시적 확인)
            return sorted(output, key=lambda x: x['similarity'], reverse=True)

        except Exception as e:
            logging.error(f"검색 중 오류 발생: {e}")
            return []