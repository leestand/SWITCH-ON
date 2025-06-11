__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from rag_core.retrieval import OptimizedConditionalRAGSystem
from rag_core.chain import create_user_friendly_chat_chain, create_chat_chain_with_memory
from ui.css import load_custom_css
from ui.banner import display_ad_banner

st.set_page_config(page_title="스위치온 부동산 법률상담", layout="wide")

load_custom_css()
display_ad_banner()

st.title("🏠 스위치온: 부동산 법률 AI 상담")

query = st.text_input("📌 전세사기, 임대차 관련 고민을 입력하세요:")

if query:
    with st.spinner("🔍 답변을 생성 중입니다..."):
        rag_system = OptimizedConditionalRAGSystem()
        retriever = rag_system.get_retriever(query)
        chat_chain = create_user_friendly_chat_chain(retriever)
        chat_chain_with_memory = create_chat_chain_with_memory(chat_chain)

        result = chat_chain_with_memory.invoke(
            {"question": query},
            config={"configurable": {"session_id": "user-session"}}
        )
        st.success("💬 AI 상담 결과")
        st.write(result)
