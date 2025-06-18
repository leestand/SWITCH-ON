# 설정 및 상수 관리
import logging

# 로그 레벨 설정
logging.basicConfig(level=logging.WARNING)

# 데이터베이스 URL 설정
DATABASE_URLS = {
    "chroma_db_law_real_final": "https://huggingface.co/datasets/sujeonggg/chroma_db_law_real_final/resolve/main/chroma_db_law_real_final.zip",
    "ja_chroma_db": "https://huggingface.co/datasets/sujeonggg/chroma_db_law_real_final/resolve/main/ja_chroma_db.zip",
}

# 임베딩 모델 설정
EMBEDDING_MODEL_NAME = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"

# OpenAI 모델 설정
OPENAI_MODEL = "gpt-4o"
OPENAI_TEMPERATURE = 0.3
MAX_TOKENS = 3000

# 법률 용어 매핑
TERM_MAPPING = {
    "집주인": "임대인", "세입자": "임차인", "전세금": "임대차보증금",
    "보증금": "임대차보증금", "월세": "차임", "방세": "차임",
    "계약서": "임대차계약서", "집 나가라": "명도청구", "쫓겨나다": "명도",
    "돈 안줘": "채무불이행", "돈 못받아": "보증금반환청구", "사기": "사기죄",
    "속았다": "기망행위", "깡통전세": "전세사기", "이중계약": "중복임대",
    "고소": "형사고발", "고발": "형사고발", "소송": "민사소송",
    "재판": "소송", "변호사": "법무사", "상담": "법률상담",
    "해결": "분쟁해결", "보상": "손해배상", "배상": "손해배상",
    "계약": "법률행위", "약속": "계약", "위반": "채무불이행", "어기다": "위반하다"
}

# 법률 지표어
LEGAL_INDICATORS = [
    "임대인", "임차인", "임대차", "명도", "채무불이행", 
    "손해배상", "민사소송", "형사고발", "보증금반환",
    "법률", "판례", "법령", "소송", "계약서"
]

# 검색 설정
LEGAL_SEARCH_K = 5
NEWS_SEARCH_K = 4
MAX_LEGAL_DOCS = 8
MAX_NEWS_DOCS = 3

# 화면 설정
PAGE_TITLE = "AI 스위치온 - 판례 검색 시스템"
PAGE_ICON = "🏠"
