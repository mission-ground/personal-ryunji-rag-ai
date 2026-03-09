import faiss
import numpy as np
import pickle

# 벡터 저장과 검색을 처리하는 클래스
class VectorStore:

    def __init__(self, dimension=384):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = {}     # vector_id → metadata
        self.current_id = 0

    # 1. 벡터 저장
    def add_documents(self, vectors, docs):

        vectors = np.array(vectors).astype("float32")

        self.index.add(vectors)

        for i, doc in enumerate(docs):

            self.documents[self.current_id] = doc

            self.current_id += 1
            
    def save(self, path="faiss_index.bin"):

        faiss.write_index(self.index, path)

        with open("documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)


    def load(self, path="faiss_index.bin"):

        self.index = faiss.read_index(path)

        with open("documents.pkl", "rb") as f:
            self.documents = pickle.load(f)        
        
    # db 확인용.        
    def print_documents(self):

        print("\n========= VECTOR STORE DOCUMENTS =========\n")

        for idx, doc in self.documents.items():

            print(f"ID: {idx}")
            print(f"PAGE: {doc['page']} | CHUNK: {doc['chunk']}")
            print(doc["text"])
            print("-"*60)
                

    # 3. 벡터 검색
    def search(self, query_vector, k=3):

        query_vector = np.array([query_vector]).astype("float32")

        distances, indices = self.index.search(query_vector, k)

        results = []

        for idx in indices[0]:

            if idx in self.documents:
                results.append(self.documents[idx])

        return results