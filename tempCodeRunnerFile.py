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
prompt="I love you baby"
message_system = {
     "role": "system", 
     "content": "You are my girlfriend"
     }
message = {"role": role, "content": prompt}
response = client.chat.completions.create(
     model=model,
     messages=[message_system, message]
)
print(response)
print("###############################")