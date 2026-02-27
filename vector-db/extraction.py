"""Extraction load PDF and chunk with page-number metadata."""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_and_chunk(pdf_path, chunk_size=1600, chunk_overlap=200):
    pages = PyPDFLoader(pdf_path).load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\\n", "\n", r"(?<=\. )", " ", ""],
    )
    chunks = splitter.split_documents(pages)

    docs = []
    for chunk in chunks:
        docs.append({
            "text": chunk.page_content,
            "metadata": {
                "source": chunk.metadata.get("source", ""),
                "page_number": chunk.metadata.get("page", 0) + 1,
            },
        })
    return docs