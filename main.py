from contextlib import asynccontextmanager
from fastapi import FastAPI
import gradio as gr

from service.rag.ingestion.index_builder  import IndexBuilder
from service.rag.components.vectorstore.chroma.vector_store import VectorStore
from service.rag.components.embedding.embedder import Embedder
from service.rag.rag_pipeline import RAGPipeline
from api.routes import router
from ui.gradio_app import create_gradio_app

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # 1. 전역 리소스 초기화 : 여기서 한 번만 생성
    embedder     = Embedder()        
    vector_store = VectorStore()
    
    # 2. RAG 파이프라인 생성 (검색용)
    app.state.rag_service = RAGPipeline(embedder, vector_store) 
    
    # 3. IndexBuilder 생성 (인덱싱용)
    # Gradio에서 쓸 수 있도록 app.state에 담아줍니다.
    # 이때 PdfLoader 등을 주입합니다.
    from service.rag.ingestion.loader.pdf_loader import PDFLoader
    app.state.index_builder = IndexBuilder(
          loader=PDFLoader()
        , embedder=embedder
        , vector_store=vector_store
    )
    yield
    
# 1. 앱 생성(FastAPI) 객체를 app 변수에 담기.
app = FastAPI(  title="RAG API"
              , lifespan=lifespan
              , description="RAG 검색 API"
              , version="0.1.0")

# 2. 라우터 추가.
app.include_router(router)

# 3. Gradio 추가.
gradio_app = create_gradio_app()
app = gr.mount_gradio_app(app, gradio_app, path="/gradio")