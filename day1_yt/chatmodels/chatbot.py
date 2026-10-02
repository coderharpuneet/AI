from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from langchain_groq import ChatGroq

model = ChatGroq(
     model="openai/gpt-oss-120b"
)
messages=[
     
]
print("---------------Welcome to the Chatbot! Press 0 to exit---------------")
while True:
     prompt=input("You : ")
     messages.append(prompt)
     if prompt == "0":
          print("---------------Thank you for using the Chatbot!---------------")
          break
     response = model.invoke(messages, temperature=0.9)
     messages.append(response.content)
     print("Bot : ", response.content)