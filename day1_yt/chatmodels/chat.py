from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq


model = ChatGroq(
     model="openai/gpt-oss-120b"
)

# print(model)
# response = model.invoke("Write a poem on tennis?",temperature=0)
# response = model.invoke("Write a poem on tennis?",temperature=0.9)
response = model.invoke("Write a poem on tennis?",temperature=0.9,max_tokens=100)

print(response.content)
