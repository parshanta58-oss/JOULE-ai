from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embedding():

    embedded = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    return embedded