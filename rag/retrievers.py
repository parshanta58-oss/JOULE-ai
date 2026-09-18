from langchain_chroma import Chroma

from rag.embedding import get_embedding


def get_retriver():

    embedding = get_embedding()

    vector_store = Chroma(
        persist_directory="rag/chroma_db",
        embedding_function=embedding
    )

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 2,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }
    )

    return retriever

""" 
retriever = get_retriver()

query = "What is the approval process for purchases?"

documents = retriever.invoke(query)

print("Retrieved Documents:")

for doc in documents:
    print(doc.page_content)
    print("-" * 80)

 """