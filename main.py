"""
AI 스위치온 - 부동산 법률 상담 AI 메인 실행 파일
"""
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import logging
import streamlit as st

# 설정 및 모듈 import
from config.settings import (
    PAGE_TITLE, PAGE_ICON, LOG_LEVEL,
    CHROMA_DB_PATH, NEWS_DB_PATH, 
    LEGAL_COLLECTION_NAME, NEWS_COLLECTION_NAME
)
from core.rag_system import OptimizedConditionalRAGSystem
from chains.chat_chain import create_chat_chain_with_memory
from ui.styles import load_custom_css
from ui.chat_interface import ChatInterface

# 로그 레벨 설정
logging.basicConfig(level=getattr(logging, LOG_LEVEL))


@st.cache_resource
def initialize_rag_system():
    """RAG 시스템 초기화 (캐시된 리소스)"""
    return OptimizedConditionalRAGSystem(
        legal_db_path=CHROMA_DB_PATH,
        news_db_path=NEWS_DB_PATH,
        legal_collection=LEGAL_COLLECTION_NAME,
        news_collection=NEWS_COLLECTION_NAME
    )


@st.cache_resource
def initialize_chat_chain(_rag_system):
    """채팅 체인 초기화 (캐시된 리소스)"""
    return create_chat_chain_with_memory(_rag_system)


def main():
    """메인 애플리케이션 함수"""
    # Streamlit 페이지 설정
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 커스텀 CSS 로드
    load_custom_css()
    
    # 시스템 초기화
    try:
        rag_system = initialize_rag_system()
        chain = initialize_chat_chain(rag_system)
    except Exception as e:
        st.error(f"시스템 초기화 중 오류가 발생했습니다: {str(e)}")
        st.stop()
    
    # 채팅 인터페이스 초기화
    chat_interface = ChatInterface()
    chat_interface.initialize_session()
    
    # UI 렌더링
    chat_interface.render_ui()
    
    # 사용자 입력 처리
    prompt = chat_interface.get_user_input()
    chat_interface.process_user_message(prompt, chain)


if __name__ == "__main__":
    main()
