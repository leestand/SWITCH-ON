"""
RAG 시스템 구현
"""
from query_preprocessor import LegalQueryPreprocessor
from document_formatter import format_docs_optimized
from config import LEGAL_SEARCH_K, NEWS_SEARCH_K, MAX_LEGAL_DOCS, MAX_NEWS_DOCS


class OptimizedConditionalRAGSystem:
    """최적화된 조건부 RAG 시스템"""
    
    def __init__(self, legal_db, news_db):
        print("🚀 RAG 시스템 초기화 중...")
        
        # 데이터베이스 연결
        self.legal_db = legal_db
        self.news_db = news_db
        
        # 쿼리 전처리기 초기화
        self.query_preprocessor = LegalQueryPreprocessor()
        print("✅ 법률 용어 전처리기 준비 완료")
        
        # 리트리버 초기화
        if self.legal_db:
            self.legal_vector_retriever = self.legal_db.as_retriever(
                search_type="similarity", 
                search_kwargs={"k": LEGAL_SEARCH_K}
            )
        else:
            self.legal_vector_retriever = None
            
        if self.news_db:
            self.news_vector_retriever = self.news_db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": NEWS_SEARCH_K}
            )
        else:
            self.news_vector_retriever = None
    
    def search_legal_db(self, query):
        """법률 DB 검색"""
        if self.legal_vector_retriever is None:
            return [], 0.0
        
        try:
            legal_docs = self.legal_vector_retriever.invoke(query)
            print(f"📄 법률 검색 결과: {len(legal_docs)}개 문서")
            return legal_docs, 0.8
        except Exception as e:
            print(f"❌ 법률 DB 검색 오류: {e}")
            return [], 0.0
    
    def search_news_db(self, query):
        """뉴스 DB 검색"""
        if self.news_vector_retriever is None:
            return [], 0.0
        
        try:
            news_docs = self.news_vector_retriever.invoke(query)
            print(f"📰 뉴스 검색 결과: {len(news_docs)}개")
            return news_docs, 0.7
        except Exception as e:
            print(f"❌ 뉴스 DB 검색 오류: {e}")
            return [], 0.0
    
    def conditional_retrieve(self, original_query):
        """조건부 검색"""
        try:
            print(f"🔍 검색 쿼리: {original_query}")
            
            # 쿼리 전처리
            converted_query, conversion_method = self.query_preprocessor.convert_query(original_query)
            
            if conversion_method != "no_conversion":
                print(f"🔄 변환된 쿼리: {converted_query}")
                search_query = converted_query
            else:
                search_query = original_query
            
            # 법률 DB 검색
            legal_docs, legal_score = self.search_legal_db(search_query)
            
            # 뉴스 DB 검색
            news_docs, news_score = self.search_news_db(search_query)
            
            # 결과 결합
            combined_docs = []
            if legal_docs:
                combined_docs.extend(legal_docs[:MAX_LEGAL_DOCS])
            if news_docs:
                combined_docs.extend(news_docs[:MAX_NEWS_DOCS])
            
            search_type = "legal_and_news" if (legal_docs and news_docs) else ("legal_only" if legal_docs else "news_only")
            
            print(f"🎯 최종 결과: {len(combined_docs)}개 문서 ({search_type})")
            return combined_docs, search_type
                
        except Exception as e:
            print(f"❌ 검색 오류: {e}")
            return [], "error"


def optimized_retrieve_and_format(query, rag_system):
    """최적화된 검색 및 포맷팅 - 전처리 포함"""
    try:
        docs, search_type = rag_system.conditional_retrieve(query)
        
        if not isinstance(docs, list):
            return f"검색 결과 형식 오류: {type(docs)}"
        
        return format_docs_optimized(docs, search_type)
        
    except Exception as e:
        print(f"❌ 검색 오류: {e}")
        return f"검색 중 오류가 발생했습니다: {str(e)}"
