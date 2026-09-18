from langchain_core.tools import tool
from rag.retrievers import get_retriver


retriever = get_retriver()


@tool
def search_company_documents(query: str) -> str:
    """
    Search company policies, procedures, SOPs, and other business documents.
    Use this tool when the user asks about company rules, policies,
    procedures, approvals, or documented processes.
    """

    documents = retriever.invoke(query)

    results = []

    for doc in documents:
        results.append(doc.page_content)

    return "\n\n".join(results)


""" result = search_company_documents.invoke(
    "What approval is required for a $35,000 purchase?"
)

print("\nRAG RESULT:\n")
print(result) """