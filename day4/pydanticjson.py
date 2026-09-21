import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")


class Ticket(BaseModel):
    name: str
    email: str
    contact_number: str


schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object",
}

system_prompt = f"""
Extract the personal information from the ticket strictly based on this schema
and give me a JSON output:

{schema}
"""

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"

text = """
Hello my name is Pratyush.
I have an iphone which is not working at all.
My email is test@test.com.
My contact number is 1234567890.
"""

prompt = f"""
This is a customer ticket.

Please extract the personal information:

{text}
"""

message = {
    "role": "user",
    "content": prompt
}

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        message
    ],
    temperature=2,
    response_format=response_format
)

answer = response.choices[0].message.content
print(answer)


import json
raw_json=answer
data_file=json.loads(raw_json)
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.contact_number)