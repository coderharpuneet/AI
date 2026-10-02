import os

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    raise RuntimeError(
        "Hugging Face token not found. Add HF_TOKEN=your_hugging_face_token "
        "to the day1_yt/.env file."
    )

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1",
    huggingfacehub_api_token=hf_token,
)

model = ChatHuggingFace(
    llm=llm
)

response = model.invoke("Who is Roger Federer?")


print(response.content)