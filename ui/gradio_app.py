from ui.tabs.indexing_tab import create_indexing_tab
from ui.tabs.search_tab import create_search_tab
import gradio as gr
#
def create_gradio_app():

    with gr.Blocks(title="RAG 파이프라인") as app:
        
        gr.Markdown("## RAG 파이프라인")
        create_indexing_tab()
        create_search_tab()
    return app