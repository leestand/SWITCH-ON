__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import uuid
import streamlit as st
from dotenv import load_dotenv

from components.style import load_custom_css, display_ad_banner
# Assume other modules are implemented correctly
# For this example, we will comment them out
# from retriever.preprocessor import LegalQueryPreprocessor
# from retriever.embedding import OptimizedKoSBERTEmbeddings, OptimizedChromaDefaultEmbeddings
# from retriever.system import OptimizedConditionalRAGSystem
# from utils.format import format_docs_optimized
# from utils.chat import create_chat_chain_with_memory

load_dotenv()

st.set_page_config(
    page_title="AI 스위치온 - 판례 검색 시스템", 
    page_icon="🏠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 로드
load_custom_css()

# ——— 헤더 ———
st.markdown("""
<div class="header-container">
    <div class="header-title">💡 <span class="highlight">AI 스위치온</span></div>
    <div class="header-subtitle">판례 기반 AI 부동산 거래 지원 서비스</div>
    <div style="margin-top: 1rem; font-size: 1rem; color: #e5e7eb;">
        💡 상황을 자세하게 설명해주시면 맞춤형 법률 정보를 제공해드립니다
    </div>
</div>
""", unsafe_allow_html=True)

# 세션 초기화
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# chain = create_chat_chain_with_memory()

# ——— 예시 UI: 대화 입력 폼 ———
user_input = st.chat_input("💬 질문을 입력하세요")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("AI가 답변을 준비 중입니다..."):
        # dummy response
        response = f"'{user_input}'에 대한 답변입니다. (모듈 완성 시 연결됩니다)"
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# 대화 출력
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'><div class='user-bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div class='ai-message'><div class='ai-bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
        display_ad_banner()