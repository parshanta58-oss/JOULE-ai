from rag.text_splitter import split_text
from rag.embedding import get_embedding
from langchain_community.vectorstores import Chroma

def create_vector_db(chunks,embedded):
    vectorstore=Chroma.from_documents(
        documents=chunks,
        embedding=embedded,
        persist_directory="rag/chroma_db"
    )

    return vectorstore