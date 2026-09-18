from langchain_chroma import Chroma


def create_vector_db(chunks, embedded):

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedded,
        persist_directory="rag/chroma_db"
    )

    return vectorstore