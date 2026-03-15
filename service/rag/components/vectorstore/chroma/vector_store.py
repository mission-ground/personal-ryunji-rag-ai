import chromadb


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(name="documents")
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

    def search(self, query_vector, k=3):
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=k
        )

        output = []

        for i in range(len(results["documents"][0])):
            output.append({
                "text": results["documents"][0][i],
                "page": results["metadatas"][0][i]["page"],
                "chunk": results["metadatas"][0][i]["chunk"]
            })

        return output