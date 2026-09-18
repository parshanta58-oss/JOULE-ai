from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(docs):

    chunking = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = chunking.split_documents(docs)

    return chunks