import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from scraper import fetch_website_contents   # reuse Class 1's scraper
load_dotenv()

prompt = ChatPromptTemplate.from_template(            # ①
    "Give a short, friendly summary of this website:\n\n{website}")

kannadaPrompt = ChatPromptTemplate.from_template("Give a short, friendly summary of this website in kannda:\n\n{website}")

hindiPrompt = ChatPromptTemplate.from_template("Give a short, friendly summary of this website in hindi:\n\n{website}")

beginnerPrompt = ChatPromptTemplate.from_template("Summarize this website as beginner friendly:\n\n{website}")

model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    base_url="https://api.groq.com/openai/v1",
    api_key= os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

parser = StrOutputParser()                             # ③

def create_chain():
    chains={
        "basic":  prompt | model | parser,
        "hindi":  hindiPrompt | model | parser, 
        "kannada": kannadaPrompt | model | parser,
        "beginner": beginnerPrompt | model | parser
    }
    return chains
                   # ④
chains = create_chain()

def summarizeSite(url):
    results ={}
    for name, chain in chains.items():
        print("chain=", repr(chains))
        print("type=", type(chains))
        results[name] = chain.invoke({"website": fetch_website_contents(url)})
    return (results["basic"], results["hindi"], results["kannada"], results["beginner"])           

print(summarizeSite("https://www.linkedin.com/"))