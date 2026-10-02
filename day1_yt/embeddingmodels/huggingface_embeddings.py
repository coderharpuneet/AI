from langchain_huggingface import HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    raise RuntimeError(
        "Hugging Face token not found. Set HF_TOKEN in the day1_yt/.env file."
    )

embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=hf_token,
)

texts = [
    "The quick brown fox jumps over the lazy dog.",
    "I love programming in Python.",
    "Artificial intelligence is transforming the world.",
]

vectors = embeddings.embed_documents(texts)

print(vectors)


