import os
import time
import functools
import uuid
import logging

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.document_transformers import LongContextReorder
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI

# 로그 레벨 감소
logging.basicConfig(level=logging.WARNING)

load_dotenv()

# 🎯 원본 코드 그대로 설정값들
PAGE_TITLE = "AI 스위치온 - 판례 검색 시스템"
PAGE_ICON = "🏠"
LOG_LEVEL = "WARNING"
CHROMA_DB_PATH = "D:\\chroma_db_law_real_final"
NEWS_DB_PATH = "D:\\ja_chroma_db"
LEGAL_COLLECTION_NAME = "legal_db"
NEWS_COLLECTION_NAME = "jeonse_fraud_embedding"

# ——— 커스텀 CSS 스타일 ———
def load_custom_css():
    st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #f5f3ff 0%, #faf9ff 50%, #fffbeb 100%);
    }
    
    /* 메인 컨테이너 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* 헤더 스타일 */
    .header-container {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 50%, #c4b5fd 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        color: #fef3c7;
        font-size: 1.2rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .highlight {
        color: #fbbf24;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 채팅 컨테이너 */
    .chat-container {
        background: transparent;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* 사용자 메시지 */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 1rem 0;
        animation: slideInRight 0.3s ease-out;
    }
    
    .user-bubble {
        max-width: 75%;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 8px 20px;
        border: 2px solid #f59e0b;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
        position: relative;
    }
    
    .user-bubble::before {
        content: '👤';
        position: absolute;
        right: -0.5rem;
        top: -0.5rem;
        background: #f59e0b;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    /* AI 메시지 */
    .ai-message {
        display: flex;
        justify-content: flex-start;
        margin: 1rem 0;
        animation: slideInLeft 0.3s ease-out;
    }
    
    .ai-bubble {
        max-width: 75%;
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 8px;
        border: 2px solid #8b5cf6;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
        position: relative;
    }
    
    .ai-bubble::before {
        content: '🤖';
        position: absolute;
        left: -0.5rem;
        top: -0.5rem;
        background: #8b5cf6;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* 광고 배너 */
    .ad-banner {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 2px solid #f59e0b;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .ad-banner:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.25);
    }
    
    .ad-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        transition: background 0.3s ease;
    }
    
    .ad-item:hover {
        background: rgba(255, 255, 255, 0.9);
    }
    
    .ad-icon {
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 80px;
        height: 60px;
        border-radius: 10px;
        color: white;
        font-size: 24px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #c4b5fd;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
    }
    
    /* 사이드바 카드 스타일 */
    .sidebar-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* 스피너 스타일 */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }
    
    /* 제목 스타일 개선 */
    h1, h2, h3 {
        color: #6b21a8;
        font-weight: 700;
    }
    
    /* 정보 박스 스타일 */
    .stInfo {
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        border: 1px solid #8b5cf6;
        border-radius: 12px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
    }
    
    /* 구분선 스타일 */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #c4b5fd 50%, transparent 100%);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 여기에 원본 코드의 나머지 모든 클래스와 함수들을 그대로 붙여넣으세요...
# (LegalQueryPreprocessor, OptimizedKoSBERTEmbeddings, OptimizedConditionalRAGSystem 등)

# 🚀 메인 실행 부분
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
    
    # 여기에 원본 코드의 나머지 UI 코드를 그대로 넣으세요...

if __name__ == "__main__":
    main()
