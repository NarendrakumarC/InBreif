from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import gradio as gr
import os
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model="openai/gpt-oss-120b",
                   base_url="https://api.groq.com/openai/v1",
                  api_key= os.getenv("GROQ_API_KEY"),
                  temperature=0.3
                  )

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly tutor"),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])

chain = prompt | model

#Hard coded history
#history =[HumanMessage("My name is Aarav."), AIMessage("Hi Aarav!")]

history=[]
"""
#Console call
print("Chat with the bot (type 'quit' to exit).")
while True:
    question = input("You: ")
    if question.strip().lower() in {"quit","exit"} :
        break

    answer = chain.invoke({"history":history, "question": question}).content  
    print("Bot:",answer)

    history.append(HumanMessage(question))
    history.append(AIMessage(answer))
    print(f'(history now has {len(history)} messages)')
"""
#answer =chain.invoke({"history":history, "question":"what's my name one more time?"})
#print(answer.content)

#With gradio with memory

def chatAssistance(question, history):
    if question.strip().lower() in {"quit", "exit"}:
        return "Thanks for chatting! How may I help you next time?"

    # Convert Gradio history into LangChain messages
    chat_history = []

    for item in history or []:

        # Newer Gradio format: {"role": "user", "content": "..."}
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")

            if not isinstance(content, str) or not content.strip():
                continue

            if role in ("user", "human"):
                chat_history.append(HumanMessage(content=content))
            elif role in ("assistant", "ai"):
                chat_history.append(AIMessage(content=content))

        # Older Gradio format: (user_message, assistant_message)
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_message, assistant_message = item

            if isinstance(user_message, str) and user_message.strip():
                chat_history.append(HumanMessage(content=user_message))

            if isinstance(assistant_message, str) and assistant_message.strip():
                chat_history.append(AIMessage(content=assistant_message))

    answer = chain.invoke({
        "history": chat_history,
        "question": question
    }).content

    return answer

gr.ChatInterface(
    chatAssistance,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(value="You: ", placeholder="Ask me a yes or no question", container=False, scale=7),
    title="Smart Virtual Bot",
    description="Ask Yes Man any question",
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
).launch(share=True)        
