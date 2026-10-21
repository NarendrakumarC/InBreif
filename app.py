import gradio as gr
from summarizer import summarize
from summarise_langchain import summarizeSite

gr.Interface(
    fn=summarizeSite,
    inputs=gr.Textbox(label="Website URL", placeholder="https://example.com"),
   # outputs=gr.Markdown(label="Summary"),
    outputs=[
        gr.Markdown(label="Summary"),
        gr.Markdown(label="Hindi Summary"),
        gr.Markdown(label="Kannada Summary"),
        gr.Markdown(label="Beginner Summary"),
        ],
    title="🔎 AI Website Summarizer",
).launch(share=True)