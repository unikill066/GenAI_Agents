from langchain_community.retrievers import BM25Retriever  # pip install rank_bm25
from langchain.tools import Tool

from data_loader import load_docs

# BM25Retriever is a powerful text retrieval algorithm that doesn't require embeddings
bm25_retriever = BM25Retriever.from_documents(load_docs())

print(bm25_retriever)

def extract_text(query: str) -> str:
    """Retrieves detailed information about gala guests based on their name or relation."""
    results = bm25_retriever.invoke(query)
    if results:
        return "\n\n".join([doc.page_content for doc in results[:3]])
    else:
        return "No matching guest information found."

guest_info_tool = Tool(
    name="guest_info_retriever",
    func=extract_text,
    description="Retrieves detailed information about gala guests based on their name or relation."
)