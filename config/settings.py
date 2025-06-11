"""
설정 관리 모듈
"""
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

# ChromaDB 설정
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "D:\\chroma_db_law_real_final")
NEWS_DB_PATH = os.getenv("NEWS_DB_PATH", "D:\\ja_chroma_db")
LEGAL_COLLECTION_NAME = os.getenv("LEGAL_COLLECTION_NAME", "legal_db")
NEWS_COLLECTION_NAME = os.getenv("NEWS_COLLECTION_NAME", "jeonse_fraud_embedding")

# 임베딩 모델 설정
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "jhgan/ko-sbert-sts")

# RAG 시스템 설정
LEGAL_SIMILARITY_THRESHOLD = 0.7
NEWS_SIMILARITY_THRESHOLD = 0.6
MIN_RELEVANT_DOCS = 3

# Streamlit 설정
PAGE_TITLE = "AI 스위치온 - 판례 검색 시스템"
PAGE_ICON = "🏠"

# 채팅 설정
MAX_CHAT_HISTORY = 20
MAX_TOKENS = 3000
TEMPERATURE = 0.3

# 로그 레벨
LOG_LEVEL = "WARNING"
