# 첫 번째 코드에 추가할 디버깅 함수들

def debug_database_connection():
    """데이터베이스 연결 상태 디버깅"""
    
    # 1. 파일 존재 확인
    chroma_path = "chroma_db_law_real_final"
    news_path = "ja_chroma_db"
    
    print("=== 데이터베이스 파일 확인 ===")
    print(f"법률 DB 경로 존재: {os.path.exists(chroma_path)}")
    print(f"뉴스 DB 경로 존재: {os.path.exists(news_path)}")
    
    if os.path.exists(chroma_path):
        files = os.listdir(chroma_path)
        print(f"법률 DB 파일들: {files}")
    
    # 2. Chroma DB 연결 테스트
    try:
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
        
        legal_db = Chroma(
            persist_directory=chroma_path,
            embedding_function=embedding_model
        )
        
        # 3. 검색 테스트
        test_docs = legal_db.similarity_search("전세보증금", k=3)
        print(f"테스트 검색 결과: {len(test_docs)}개")
        
        for i, doc in enumerate(test_docs):
            print(f"문서 {i+1}:")
            print(f"  메타데이터: {doc.metadata}")
            print(f"  내용 미리보기: {doc.page_content[:100]}...")
            
        return True
        
    except Exception as e:
        print(f"DB 연결 실패: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def fix_initialization():
    """개선된 초기화 함수"""
    
    try:
        # 1. 다운로드 확인
        download_success = download_and_extract_databases(verbose=True)
        if not download_success:
            print("❌ DB 다운로드 실패")
            return None, None, None, False
        
        # 2. 디버깅 실행
        db_status = debug_database_connection()
        if not db_status:
            print("❌ DB 연결 테스트 실패")
            return None, None, None, False
        
        # 3. 정상 초기화
        embedding_model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
        
        legal_db = Chroma(
            persist_directory="chroma_db_law_real_final",
            embedding_function=embedding_model
        )
        
        news_db = Chroma(
            persist_directory="ja_chroma_db", 
            embedding_function=embedding_model
        )
        
        print("✅ 모든 DB 연결 완료")
        return embedding_model, legal_db, news_db, True
        
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")
        return None, None, None, False

# 메인 함수에서 사용
def main():
    # 기존 초기화 대신 이걸로 교체
    with st.spinner("🔄 AI 시스템 초기화 및 디버깅 중..."):
        embedding_model, legal_db, news_db, system_ready = fix_initialization()
    
    if not system_ready:
        st.error("❌ 시스템 초기화 실패 - 판례 검색이 불가능합니다")
        st.info("💡 해결 방법: 1) 인터넷 연결 확인 2) 다시 시도 3) 로컬 DB 경로 사용")
        return
    
    # 나머지 코드는 동일...
