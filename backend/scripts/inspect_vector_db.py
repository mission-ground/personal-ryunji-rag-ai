from backend.service.rag.components.vectorstore.faiss.vector_store import VectorStore

store = VectorStore()

# 저장된 index 로드
store.load()

print("\n===== VECTOR COUNT =====")
print(store.index.ntotal)

print("\n===== DOCUMENTS =====")
store.print_documents()