import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from scraper import fetch_website_contents   # reuse Class 1's scraper
load_dotenv()

prompt = ChatPromptTemplate.from_template(            # ①
    "Give a short, friendly summary of this website:\n\n{website}")

model = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key= os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

parser = StrOutputParser()                             # ③

chain = prompt | model | parser                        # ④

def summarize(url):
    return chain.invoke({"website": fetch_website_contents(url)})   # ⑤

print(summarize("https://www.linkedin.com/"))