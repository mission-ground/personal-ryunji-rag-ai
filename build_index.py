from backend.service.rag.ingestion.index_builder import IndexBuilder

builder = IndexBuilder()

embedder, store = builder.build()

store.save()

print("✅ FAISS index 저장 완료")