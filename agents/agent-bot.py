import gradio as gr
from agent import agent              # the function you just wrote

def chat(message, history): 
    # Gradio fills in message(newest) and history (past turns) for you
    # Homework hint : pass the history into your agent to give it memory
    return agent(message)

gr.ChatInterface(fn=chat, title="🛍️ Smart Shop Assistant").launch(share=True)  # ②