from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import load_documents

def split_text(document_list):
    chunking=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks=chunking.split(document_list)

    return chunks


