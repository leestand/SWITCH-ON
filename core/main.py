"""
AI 스위치온 - 판례 기반 AI 부동산 거래 지원 서비스
메인 애플리케이션
"""
# SQLite 호환성 설정
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import uuid
import streamlit as st

# 모듈 임포트
from config import PAGE_TITLE, PAGE_ICON
from database_utils import initialize_embeddings_and_databases
from styles import load_custom_css
from rag_system import OptimizedConditionalRAGSystem
from chat_chain import create_chat_chain_with_memory
from ui_components import (
    render_header, render_sidebar, render_system_status,
    render_service_info, render_disclaimer, render_chat_messages,
    render_chat_input, render_footer
)
from ads import display_ad_banner


def initialize_session_state():
    """세션 상태 초기화"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


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

    # 헤더 렌더링
    render_header()

    # 시스템 초기화
    with st.spinner("🔄 AI 시스템 초기화 중..."):
        embedding_model, legal_db, news_db, system_ready = initialize_embeddings_and_databases()

    # 세션 상태 초기화
    initialize_session_state()

    # RAG 시스템 및 채팅 체인 생성
    if system_ready and (legal_db or news_db):
        try:
            rag_system = OptimizedConditionalRAGSystem(legal_db, news_db)
            chain = create_chat_chain_with_memory(rag_system)
        except Exception as e:
            st.error(f"❌ RAG 시스템 오류: {str(e)}")
            chain = None
            rag_system = None
    else:
        chain = None
        rag_system = None

    # 사이드바 렌더링
    render_sidebar()
    
    # 시스템 상태 표시
    render_system_status(system_ready, legal_db, news_db)
    
    # 서비스 안내
    render_service_info()
    
    # 주의사항
    render_disclaimer()

    # 채팅 메시지 렌더링
    render_chat_messages(st.session_state.chat_history)
    
    # AI 답변 후 광고 배너 표시
    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "assistant":
        display_ad_banner()

    # 질문 입력 처리
    prompt = st.session_state.pop("sidebar_prompt", None)
    if not prompt:
        prompt = render_chat_input()

    # 질문 처리
    if prompt:
        # 사용자 메시지 저장
        st.session_state.chat_history.append({"role": "user", "content": prompt
