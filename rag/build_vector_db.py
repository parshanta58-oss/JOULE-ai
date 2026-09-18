from rag.document_loader import load_documents
from rag.text_splitter import split_text
from rag.embedding import get_embedding
from rag.vector_store import create_vector_db


documents = load_documents()

print("Documents loaded:", len(documents))


chunks = split_text(documents)

print("Chunks created:", len(chunks))


embedding = get_embedding()


vector_store = create_vector_db(
    chunks,
    embedding
)

print("Vector database created successfully.")