from service.rag.ingestion.loader.pdf_loader import PDFLoader # PdfLoader 임포트
import gradio as gr

# 2. 인덱싱 시작 버튼 클릭 시 작동할 기능.
def index_pdf(pdf_file):

    if pdf_file is None:
        return "PDF를 먼저 업로드하세요."

    try:

        # 1. FastAPI app 인스턴스에서 미리 생성된 builder를 가져온다.
        # 2. (Gradio가 FastAPI에 마운트되어 있으므로 접근이 가능하다)
        from main import app 
        builder = app.state.index_builder

        # 3. 클래스(IndexBuilder)가 아니라 '인스턴스(builder)'의 메서드를 호출한다.
        # 4. 메서드 이름도 빌더 안에 정의하신 'build_index'로 호출해야 한다.
        return builder.build_index(pdf_file.name)
    except Exception as e:

        return f"❌ 오류: {e}"

# 1. Gradio로 생성할 화면 코드
def create_indexing_tab():

    with gr.Tab("PDF 인덱싱"):
        
        gr.Markdown("PDF를 업로드하면 텍스트를 추출해 벡터 DB에 저장합니다.")
        pdf_input = gr.File(label="PDF 업로드", file_types=[".pdf"])
        index_btn = gr.Button("인덱싱 시작", variant="primary")
        index_out = gr.Textbox(label="결과", lines=3)
        index_btn.click(
              fn=index_pdf
            , inputs=[pdf_input]
            , outputs=[index_out]
        )