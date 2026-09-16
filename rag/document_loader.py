from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


file_path = Path("documents")


def load_documents():
    document_list = []

    pdf_files = list(file_path.glob("*.pdf"))

    for pdf_file in pdf_files:
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()

        document_list.extend(docs)

    return document_list

