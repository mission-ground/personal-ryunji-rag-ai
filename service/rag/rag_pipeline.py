from service.rag.retrieval.retriever import Retriever
from service.rag.generation.generator import Generator
from service.rag.components.embedding.embedder import Embedder
from service.rag.components.vectorstore.chroma.vector_store import VectorStore




# 파일명은 snake_case, 클래스는 PascalCase가 맞음.
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