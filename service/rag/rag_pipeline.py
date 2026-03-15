from backend.service.rag.retrieval.retriever import Retriever
from backend.service.rag.generation.generator import Generator

# 사람으로 따지면 감독.
class RAGPipeline:

    def __init__(self, embedder, vector_store):

        self.retriever = Retriever(embedder, vector_store)
        self.generator = Generator()

    def ask(self, query):

        documents = self.retriever.retrieve(query)

        context = "\n".join(documents)

        answer = self.generator.generate(query, context)

        return answer