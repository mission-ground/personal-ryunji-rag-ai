import gradio as gr
from service.rag.rag_pipeline import RAGPipeline


def search(query):
    if not query or not query.strip():
        return "질문을 입력해주세요."

    results = RAGPipeline.search(query, k=3)

    return "\n\n".join([
        f"[{i + 1}] 유사도: {r['similarity']:.4f}\n{r['content'][:500]}"
        for i, r in enumerate(results)
    ])


def create_search_tab():
    with gr.Tab("질문 검색"):
        gr.Markdown("질문을 입력하면 벡터 DB에서 관련 문서를 검색합니다.")

        query_input = gr.Textbox(label="질문", placeholder="예: 기준금리란?")
        search_btn = gr.Button("검색", variant="primary")
        search_out = gr.Textbox(label="검색 결과", lines=15)

        search_btn.click(
            fn=search,
            inputs=[query_input],
            outputs=[search_out]
        )