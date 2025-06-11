"""
RAG 시스템 핵심 로직
"""
import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.document_transformers import LongContextReorder
from langchain_core.documents import Document

from config.settings import (
    LEGAL_SIMILARITY_THRESHOLD, 
    NEWS_SIMILARITY_THRESHOLD, 
    MIN_RELEVANT_DOCS
)
from core.embeddings import OptimizedKoSBERTEmbeddings
from core.preprocessor import LegalQueryPreprocessor


class OptimizedConditionalRAGSystem:
    """전처리 기능이 추가된 최적화된 조건부 검색 시스템"""
    
    def __init__(self, legal_db_path, news_db_path, legal_collection, news_collection):
        print("🚀 최적화된 RAG 시스템 초기화 중...")
        start_time = time.time()
        
        # 쿼리 전처리기 초기화
        print("🔄 법률 용어 전처리기 초기화 중...")
        self.query_preprocessor = LegalQueryPreprocessor()
        print("✅ 법률 용어 전처리기 준비 완료")
        
        # 임베딩 함수 초기화
        self.legal_embedding_function = OptimizedKoSBERTEmbeddings()
        print("📊 법률 DB와 뉴스 DB 모두 KoSBERT 768차원 임베딩 사용")
        
        # 임계값 설정
        self.legal_similarity_threshold = LEGAL_SIMILARITY_THRESHOLD
        self.news_similarity_threshold = NEWS_SIMILARITY_THRESHOLD
        self.min_relevant_docs = MIN_RELEVANT_DOCS
        
        # DB 연결 최적화
        self._init_legal_db(legal_db_path, legal_collection)
        self._init_news_db(news_db_path, news_collection)
        
        init_time = time.time() - start_time
        print(f"⚡ 시스템 초기화 완료 ({init_time:.2f}초)")
    
    def _init_legal_db(self, legal_db_path, legal_collection):
        """법률 DB 초기화 최적화"""
        print(f"🏛️ 법률 DB 연결 중...")
        try:
            self.legal_db = Chroma(
                persist_directory=legal_db_path,
                collection_name=legal_collection,
                embedding_function=self.legal_embedding_function
            )
            
            self.legal_documents = None
            self.legal_bm25_retriever = None
            self.legal_hybrid_retriever = None
            
            self.legal_vector_retriever = self.legal_db.as_retriever(
                search_type="similarity", 
                search_kwargs={"k": 5}
            )
            print("✅ 법률 DB 연결 완료")
            
        except Exception as e:
            print(f"❌ 법률 DB 연결 실패: {e}")
            self.legal_db = None
            self.legal_vector_retriever = None
    
    def _init_news_db(self, news_db_path, news_collection):
        """뉴스 DB 초기화 최적화"""
        print(f"📰 뉴스 DB 연결 중...")
        try:
            self.news_db = Chroma(
                persist_directory=news_db_path,
                collection_name=news_collection,
                embedding_function=self.legal_embedding_function
            )
            
            news_count = self.news_db._collection.count()
            print(f"✅ 뉴스 DB 연결 완료 (문서 수: {news_count})")
            
            try:
                test_docs = self.news_db.similarity_search("전세", k=1)
                print(f"🧪 검색 테스트 결과: {len(test_docs)}개")
                if test_docs:
                    print(f"   샘플 제목: {test_docs[0].metadata.get('title', '제목없음')[:50]}...")
            except Exception as test_e:
                print(f"⚠️ 검색 테스트 실패: {test_e}")
            
            self.news_vector_retriever = self.news_db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            print("✅ 뉴스 DB KoSBERT 768차원 임베딩 설정 완료")
            
        except Exception as e:
            print(f"❌ 뉴스 DB 연결 실패: {e}")
            import traceback
            print(f"상세 오류: {traceback.format_exc()}")
            self.news_db = None
            self.news_vector_retriever = None
    
    def _lazy_init_hybrid_retriever(self):
        """하이브리드 리트리버 지연 초기화"""
        if self.legal_hybrid_retriever is None and self.legal_db is not None:
            print("🔄 하이브리드 리트리버 초기화 중...")
            try:
                legal_data = self.legal_db.get()
                
                if not legal_data or not legal_data.get("documents"):
                    print("⚠️ 법률 DB에서 문서를 가져올 수 없음")
                    return
                
                all_legal_docs = legal_data["documents"]
                all_legal_metadatas = legal_data.get("metadatas", [{}] * len(all_legal_docs))
                
                if len(all_legal_metadatas) < len(all_legal_docs):
                    all_legal_metadatas.extend([{}] * (len(all_legal_docs) - len(all_legal_metadatas)))
                
                self.legal_documents = [
                    Document(page_content=doc, metadata=meta or {})
                    for doc, meta in zip(all_legal_docs, all_legal_metadatas)
                ]
                
                print(f"📄 법률 문서 로딩 완료: {len(self.legal_documents)}개")
                
                self.legal_bm25_retriever = BM25Retriever.from_documents(self.legal_documents)
                self.legal_bm25_retriever.k = 8
                
                self.legal_hybrid_retriever = EnsembleRetriever(
                    retrievers=[self.legal_vector_retriever, self.legal_bm25_retriever],
                    weights=[0.65, 0.35]
                )
                print("✅ 하이브리드 리트리버 초기화 완료")
                
            except Exception as e:
                print(f"⚠️ 하이브리드 리트리버 초기화 실패, 벡터 검색만 사용: {e}")
                import traceback
                print(f"상세 오류: {traceback.format_exc()}")
                self.legal_hybrid_retriever = None
    
    def calculate_cosine_similarity_score(self, query, docs, use_news_embedding=False):
        """최적화된 코사인 유사도 계산"""
        if not docs:
            return 0.0
        
        try:
            query_embedding = self.legal_embedding_function.embed_query(query)
            
            if not isinstance(query_embedding, np.ndarray):
                query_embedding = np.array(query_embedding)
            
            if query_embedding.ndim > 1:
                query_embedding = query_embedding.flatten()
            
            limited_docs = docs[:5]
            doc_texts = [doc.page_content[:1500] for doc in limited_docs]
            
            doc_embeddings = self.legal_embedding_function.embed_documents(doc_texts)
            
            if not isinstance(doc_embeddings, np.ndarray):
                doc_embeddings = np.array(doc_embeddings)
            
            if doc_embeddings.ndim == 1:
                doc_embeddings = doc_embeddings.reshape(1, -1)
            
            if query_embedding.shape[0] != doc_embeddings.shape[1]:
                print(f"⚠️ 차원 불일치: 쿼리 {query_embedding.shape[0]}, 문서 {doc_embeddings.shape[1]}")
                return 0.65
            
            similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
            
            return float(np.max(similarities)) if len(similarities) > 0 else 0.0
            
        except Exception as e:
            print(f"⚠️ 유사도 계산 오류: {e}")
            return 0.65
    
    def search_legal_db(self, query):
        """최적화된 법률 DB 검색"""
        if self.legal_db is None:
            print("❌ 법률 DB가 연결되지 않음")
            return [], 0.0
        
        try:
            # 🔍 쿼리 확장 적용
            expanded_query = self._expand_query_with_legal_terms(query)
            if expanded_query != query:
                print(f"🔄 확장된 법률 검색 쿼리: {expanded_query}")
            else:
                print(f"🔍 법률 DB 검색 쿼리: {query}")
            
            # 확장된 쿼리로 검색
            legal_docs = self.legal_vector_retriever.invoke(expanded_query)
            print(f"📄 벡터 검색 결과: {len(legal_docs)}개 문서")
            
            if legal_docs:
                for i, doc in enumerate(legal_docs[:2]):
                    doc_type = doc.metadata.get('doc_type', '유형불명')
                    content_preview = str(doc.page_content)[:50] if doc.page_content else "내용없음"
                    print(f"   [{i+1}] {doc_type}: {content_preview}...")
            else:
                print("   ⚠️ 벡터 검색에서 문서를 찾지 못함")
            
            if len(legal_docs) < self.min_relevant_docs:
                print(f"📊 문서 개수 부족({len(legal_docs)} < {self.min_relevant_docs}), 하이브리드 검색 시도")
                self._lazy_init_hybrid_retriever()
                if self.legal_hybrid_retriever is not None:
                    # 하이브리드 검색도 확장된 쿼리 사용
                    hybrid_docs = self.legal_hybrid_retriever.invoke(expanded_query)
                    print(f"📄 하이브리드 검색 결과: {len(hybrid_docs)}개 문서")
                    if len(hybrid_docs) > len(legal_docs):
                        legal_docs = hybrid_docs
                        print("✅ 하이브리드 검색 결과로 교체")
            
            if len(legal_docs) > 5:
                legal_docs = LongContextReorder().transform_documents(legal_docs)
                print("🔄 문서 재정렬 완료")
            
            # 유사도 계산은 원본 쿼리로 (더 정확한 평가를 위해)
            similarity_score = self.calculate_cosine_similarity_score(query, legal_docs, use_news_embedding=False)
            print(f"📊 법률 DB 최종 점수: {similarity_score:.3f}")
            
            return legal_docs, similarity_score
            
        except Exception as e:
            print(f"❌ 법률 DB 검색 오류: {e}")
            import traceback
            print(f"상세 오류: {traceback.format_exc()}")
            return [], 0.0
    
    def search_news_db(self, query):
        """최적화된 뉴스 DB 검색"""
        if self.news_db is None or self.news_vector_retriever is None:
            print("❌ 뉴스 DB가 연결되지 않음")
            return [], 0.0
        
        try:
            enhanced_query = self._enhance_news_query(query)
            print(f"🔍 뉴스 검색 쿼리: {enhanced_query}")
            
            news_docs = self.news_vector_retriever.invoke(enhanced_query)
            print(f"📰 뉴스 검색 결과: {len(news_docs)}개")
            
            if news_docs:
                for i, doc in enumerate(news_docs[:2]):
                    title = doc.metadata.get('title', '제목없음')
                    print(f"   [{i+1}] {title[:50]}...")
            else:
                print("   ⚠️ 뉴스 검색에서 문서를 찾지 못함")
            
            if news_docs:
                similarity_score = self.calculate_cosine_similarity_score(
                    enhanced_query, news_docs, use_news_embedding=False
                )
                print(f"📊 뉴스 검색 점수: {similarity_score:.3f}")
            else:
                similarity_score = 0.0
            
            return news_docs, similarity_score
            
        except Exception as e:
            print(f"❌ 뉴스 DB 검색 오류: {e}")
            import traceback
            print(f"상세 오류: {traceback.format_exc()}")
            return [], 0.0
    
    def _expand_query_with_legal_terms(self, query):
        """법률 쿼리 확장 - 동의어와 관련 용어 추가"""
        expansion_terms = []
        
        # 부동산 관련 확장
        if "보증금" in query: 
            expansion_terms.extend(["임대차보증금", "전세금"])
        if "집주인" in query: 
            expansion_terms.append("임대인")
        if "세입자" in query: 
            expansion_terms.append("임차인")
        if "월세" in query:
            expansion_terms.append("차임")
        if "계약서" in query:
            expansion_terms.append("임대차계약서")
        
        # 법적 절차 관련 확장
        if "소송" in query:
            expansion_terms.extend(["민사소송", "소송절차"])
        if "손해배상" in query:
            expansion_terms.append("배상청구")
        if "명도" in query:
            expansion_terms.extend(["명도청구", "퇴거"])
        
        # 전세사기 관련 확장
        if any(term in query for term in ["사기", "깡통전세", "전세사기"]):
            expansion_terms.extend(["전세사기", "임대차사기", "보증금사기"])
        
        # 최대 3개 용어만 추가 (너무 길어지지 않게)
        if expansion_terms:
            unique_terms = list(set(expansion_terms))[:3]
            expanded_query = f"{query} {' '.join(unique_terms)}"
            return expanded_query
        
        return query
    
    def _enhance_news_query(self, query):
        """뉴스 쿼리 강화"""
        # 기본 강화
        enhanced = query
        if any(term in query for term in ["전세", "부동산", "임대", "사기"]):
            enhanced = f"{query} 전세사기"
        
        return enhanced
    
    def conditional_retrieve(self, original_query):
        """조건부 검색 - 쿼리 전처리 추가"""
        try:
            print(f"🔍 원본 검색 쿼리: {original_query}")
            
            # ✅ 핵심 추가: 일상어 → 법률어 전처리
            converted_query, conversion_method = self.query_preprocessor.convert_query(original_query)
            
            if conversion_method != "no_conversion":
                print(f"🔄 변환된 검색 쿼리: {converted_query}")
                print(f"📋 변환 방법: {conversion_method}")
                # 실제 검색에는 변환된 쿼리 사용
                search_query = converted_query
            else:
                print("📋 이미 법률 용어로 구성된 쿼리")
                search_query = original_query
            
            # 1단계: 법률 DB 검색 (변환된 쿼리 사용)
            print("🏛️ 법률 DB 검색 중...")
            legal_docs, legal_score = self.search_legal_db(search_query)
            print(f"📊 법률 DB 결과: {len(legal_docs)}개 문서, 점수: {legal_score:.3f}")
            
            # 2단계: 법률 DB 결과 충분성 평가
            is_legal_sufficient = (
                legal_score >= self.legal_similarity_threshold and 
                len(legal_docs) >= self.min_relevant_docs
            )
            
            if is_legal_sufficient:
                print("✅ 법률 DB 결과만으로 충분함")
                return legal_docs, "legal_only"
            
            # 3단계: 법률 DB 결과가 부족한 경우에만 뉴스 DB 검색
            print("📰 법률 DB 결과 부족, 뉴스 DB로 보완 검색...")
            news_docs, news_score = self.search_news_db(search_query)
            print(f"📊 뉴스 DB 결과: {len(news_docs)}개 문서, 점수: {news_score:.3f}")
            
            # 4단계: 결과 결합
            combined_docs = []
            
            if legal_docs:
                combined_docs.extend(legal_docs[:8])  # 법률 문서 최대 8개로 증가
                print(f"✅ 법률 문서 {len(legal_docs[:8])}개 추가")
            
            if news_docs and news_score >= self.news_similarity_threshold:
                combined_docs.extend(news_docs[:3])  # 뉴스는 3개로 조정 (총 11개 방지)
                print(f"✅ 뉴스 문서 {len(news_docs[:5])}개 추가")
                search_type = "legal_and_news"
            elif legal_docs:
                search_type = "legal_only"
            else:
                search_type = "no_results"
            
            print(f"🎯 최종 결과: {len(combined_docs)}개 문서 ({search_type})")
            return combined_docs, search_type
                
        except Exception as e:
            print(f"❌ 검색 오류: {e}")
            return [], "error"
