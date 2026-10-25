import os
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import (
	Docx2txtLoader,
	PyPDFLoader,
	TextLoader,
)
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def load_uploaded_documents(uploaded_files: Sequence[Any]) -> list[Document]:
	"""Save each upload temporarily, then load it with the matching LangChain loader."""
	documents: list[Document] = []
	loaders = {
		".txt": TextLoader,
		".md": TextLoader,
		".pdf": PyPDFLoader,
		".docx": Docx2txtLoader,
	}

	with tempfile.TemporaryDirectory() as temp_dir:
		for uploaded_file in uploaded_files:
			filename = Path(uploaded_file.name).name
			extension = Path(filename).suffix.lower()
			loader_class = loaders.get(extension)
			if loader_class is None:
				raise ValueError(f"Unsupported file type: {extension or 'no extension'}")

			temporary_path = Path(temp_dir) / filename
			temporary_path.write_bytes(uploaded_file.getvalue())
			loader = (
				loader_class(str(temporary_path), encoding="utf-8")
				if loader_class is TextLoader
				else loader_class(str(temporary_path))
			)

			for document in loader.load():
				document.metadata["source"] = filename
				documents.append(document)

	return documents


def summarize_documents(documents: list[Document], model: ChatGroq) -> str:
	"""Summarize chunks first, then combine those summaries into one result."""
	splitter = RecursiveCharacterTextSplitter(
		chunk_size=6000,
		chunk_overlap=300,
		add_start_index=True,
	)
	chunks = splitter.split_documents(documents)

	map_prompt = ChatPromptTemplate.from_messages(
		[
			(
				"system",
				"Summarize this excerpt faithfully. Keep its key ideas, definitions, "
				"important details, and caveats. Do not add information that is not present.",
			),
			("human", "{text}"),
		]
	)
	reduce_prompt = ChatPromptTemplate.from_messages(
		[
			(
				"system",
				"Combine the partial summaries into one clear, well-organized summary. "
				"Remove repetition, preserve important details, and do not invent facts.",
			),
			("human", "Partial summaries:\n\n{text}"),
		]
	)
	map_chain = map_prompt | model | StrOutputParser()
	reduce_chain = reduce_prompt | model | StrOutputParser()

	partial_summaries = [
		map_chain.invoke({"text": chunk.page_content}) for chunk in chunks
	]

	# Reduce in small batches so large uploads do not create one oversized prompt.
	while len(partial_summaries) > 1:
		partial_summaries = [
			reduce_chain.invoke({"text": "\n\n".join(partial_summaries[start : start + 8])})
			for start in range(0, len(partial_summaries), 8)
		]

	return partial_summaries[0]


st.set_page_config(page_title="Notes Summarizer", page_icon="📝")
st.title("📝 Notes Summarizer")
st.write("Upload notes as TXT, Markdown, PDF, or DOCX and get a concise summary.")

uploaded_files = st.file_uploader(
	"Choose your notes",
	type=["txt", "md", "pdf", "docx"],
	accept_multiple_files=True,
)

if st.button("Summarize notes", type="primary", disabled=not uploaded_files):
	if not os.getenv("GROQ_API_KEY"):
		st.error("GROQ_API_KEY is missing. Add it to a .env file in this project folder.")
	else:
		try:
			with st.spinner("Loading and summarizing your notes..."):
				documents = load_uploaded_documents(uploaded_files)
				if not documents or not any(doc.page_content.strip() for doc in documents):
					st.warning("No readable text was found in the uploaded files.")
				else:
					model = ChatGroq(
						model="openai/gpt-oss-120b",
						temperature=0.2,
					)
					summary = summarize_documents(documents, model)
					st.subheader("Summary")
					st.markdown(summary)
					st.caption(
						f"Loaded {len(documents)} document page(s) from "
						f"{len(uploaded_files)} file(s)."
					)
		except Exception as error:
			st.error(f"Could not summarize these files ({type(error).__name__}). Check the file and API key, then try again.")

