import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
     raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role="user"
prompt="Suggest a name for a new product that is a new type of chocolate that is made with 100% organic ingredients and is free from any artificial flavors or preservatives. The brand name should be catchy, memorable, and convey the idea of high quality and natural ingredients."
message_system = {
     "role": "system", 
     "content": "You are a brand manager and you have tosuggest a brand name for a new product."
     }
message = {"role": role, "content": prompt}
response = client.chat.completions.create(
     model=model,
     messages=[message_system, message],
     temperature=0,
)
print(response)
print("###############################")