
def format_docs_optimized(docs):
    return "\n\n".join(
        f"[출처: {doc.metadata.get('source', '출처없음')}]\n{doc.page_content}"
        for doc in docs
    )
