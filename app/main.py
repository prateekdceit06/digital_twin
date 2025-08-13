import gradio as gr
from me.me import Me

def launch():
    me = Me()
    gr.ChatInterface(
        fn=me.chat,
        type="messages",
        fill_height=True,
        chatbot=gr.Chatbot(
            type="messages",
            value=[{
                "role": "assistant",
                "content": "👋 Welcome! I am Prateek Jain. Ask me anything about my work and research. "
                           "If you want me to connect with you, please provide your email address and name (optional)."
            }],
            height="85vh"
        )
    ).launch()
