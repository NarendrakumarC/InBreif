import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key= os.getenv("GROQ_API_KEY")
)


# -- tiny "database" (a dict standing in for real one)
PRICES = {"shoes": 799, "hat": 399, "bag": 1420, "shorts": 1299, "pants": 1699}

# step 1 the tool call is just a normal python function
def get_price(item):
    print(f"🔧 tool called: get_price({item})")     # so you SEE it happen
    return f"₹{PRICES.get(item.lower(), 'unknown')}"

# print(get_price("shoes"))

# step 2 : describe the tool so the model knows it exits 

tools = [{
    "type": "function",                                      
    "function": {
        "name": "get_price",                                 
        "description": "Get the price of a shop item the user asks about.",  
        "parameters": {                                       
            "type": "object",
            "properties": {"item": {"type": "string", "description": "the item name"}},
            "required": ["item"],
        },
    },
}]

# step 3 the loop - think - maybe call tool -> answer

def agent(user_message):
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(          # ① send message + tools menu
        model="openai/gpt-oss-20b", messages=messages, tools=tools)
    msg = response.choices[0].message

    if msg.tool_calls:                                  # ② did it ask for a tool?
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)  # ③ read its request, run it
            result = get_price(args["item"])
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
        response = client.chat.completions.create(      # ④ send it all back → nice answer
            model="openai/gpt-oss-20b", messages=messages)
        msg = response.choices[0].message

    return msg.content

if __name__ == "__main__":
    print(agent("How much are the shoes?"))      # → tool fires → "₹799"
    print(agent("Hi! What can you help with?"))   # → no tool → just chats