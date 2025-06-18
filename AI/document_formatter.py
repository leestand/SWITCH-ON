"""
문서 포맷팅 유틸리티
"""


def format_docs_optimized(docs, search_type):
    """최적화된 문서 포맷팅 - 출처별 명확한 구분"""
    if not docs:
        return "관련 자료를 찾을 수 없습니다."
    
    formatted_docs = []
    news_count = 0
    precedent_count = 0
    interpretation_count = 0
    qa_count = 0
    
    for i, doc in enumerate(docs):
        try:
            meta = doc.metadata if doc.metadata else {}
            content = str(doc.page_content)[:1000] if doc.page_content else ""
            
            is_news = ('url' in meta and 'title' in meta) or ('date' in meta and 'title' in meta)
            
            if is_news:
                news_count += 1
                title = str(meta.get("title", "제목없음"))[:80]
                date = str(meta.get("date", "날짜미상"))
                source = str(meta.get("source", "뉴스"))
                
                formatted = f"[뉴스-{news_count}] 📰 뉴스\n"
                formatted += f"제목: {title}\n"
                formatted += f"출처: {source} | 날짜: {date}\n"
                formatted += f"내용: {content}...\n"
                
            else:
                doc_type = str(meta.get("doc_type", "")).lower()
                
                if any(keyword in doc_type for keyword in ["판례", "판결", "대법원", "고등법원", "지방법원"]) or \
                   any(key in meta for key in ["판결요지", "판시사항", "case_id", "court"]):
                    
                    case_id = str(meta.get("case_id", ""))
                    if case_id and case_id.strip() != "":
                        formatted = f"[판례-{case_id}] 🏛️ 판례\n"
                    else:
                        precedent_count += 1
                        formatted = f"[판례-{precedent_count}] 🏛️ 판례\n"
                    
                    formatted += f"내용: {content}...\n"
                    
                elif any(keyword in doc_type for keyword in ["법령해석", "해석례", "유권해석", "행정해석"]) or \
                     any(key in meta for key in ["해석내용", "법령명", "interpretation_id"]):
                    
                    interpretation_id = str(meta.get("interpretation_id", ""))
                    if interpretation_id and interpretation_id.strip() != "":
                        formatted = f"[법령해석례-{interpretation_id}] ⚖️ 법령해석례\n"
                    else:
                        interpretation_count += 1
                        formatted = f"[법령해석례-{interpretation_count}] ⚖️ 법령해석례\n"
                    
                    formatted += f"내용: {content}...\n"
                    
                elif any(keyword in doc_type for keyword in ["백문백답", "생활법령", "qa", "질의응답", "faq"]) or \
                     any(key in meta for key in ["질문", "답변", "question", "answer", "qa_id"]):
                    
                    qa_id = str(meta.get("qa_id", ""))
                    if qa_id and qa_id.strip() != "":
                        formatted = f"[백문백답-{qa_id}] 💡 생활법령 Q&A\n"
                    else:
                        qa_count += 1
                        formatted = f"[백문백답-{qa_count}] 💡 생활법령 Q&A\n"
                    
                    formatted += f"내용: {content}...\n"
                    
                else:
                    precedent_count += 1
                    source = str(meta.get("doc_type", "법률자료"))
                    formatted = f"[법률-{precedent_count}] 📋 {source}\n"
                    formatted += f"내용: {content}...\n"
            
            formatted_docs.append(formatted)
            
        except Exception as e:
            print(f"⚠️ 문서 포맷팅 오류: {e}")
            try:
                content = str(doc.page_content)[:1000] if doc.page_content else "내용 없음"
                formatted_docs.append(f"[문서-{i+1}] {content}...")
            except:
                continue
    
    # 결과 조합 - 유형별 개수 표시
    header_parts = []
    if precedent_count > 0:
        header_parts.append(f"판례 {precedent_count}개")
    if interpretation_count > 0:
        header_parts.append(f"법령해석례 {interpretation_count}개")
    if qa_count > 0:
        header_parts.append(f"생활법령Q&A {qa_count}개")
    if news_count > 0:
        header_parts.append(f"뉴스 {news_count}개")
    
    header = f"📋 검색결과: {', '.join(header_parts)}\n"
    header += "="*60 + "\n"
    header += "⚠️ AI가 아래 자료 유형을 정확히 확인하고 답변하세요:\n"
    
    if precedent_count > 0:
        header += f"• 판례 자료: [판례-번호] 🏛️ 판례 형태로 표시됨\n"
    if interpretation_count > 0:
        header += f"• 법령해석례 자료: [법령해석례-번호] ⚖️ 법령해석례 형태로 표시됨\n"
    if qa_count > 0:
        header += f"• 생활법령 자료: [백문백답-번호] 💡 생활법령 Q&A 형태로 표시됨\n"
    if news_count > 0:
        header += f"• 뉴스 자료: [뉴스-번호] 📰 뉴스 형태로 표시됨\n"
    
    header += "="*60 + "\n\n"
    
    result = header + "\n\n".join(formatted_docs)
    
    return result
