def format_docs_optimized(docs, search_type):
    if not docs:
        return "관련 자료를 찾을 수 없습니다."
    results = []
    for i, doc in enumerate(docs):
        content = doc.page_content[:500]
        results.append(f"[{i+1}] {content}...")
    return "\n\n".join(results)