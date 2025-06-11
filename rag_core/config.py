# DB 경로 및 설정 변수

from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "D:/chroma_db_law_real_final")
NEWS_DB_PATH = os.getenv("NEWS_DB_PATH", "D:/ja_chroma_db")
LEGAL_COLLECTION_NAME = "legal_db"
NEWS_COLLECTION_NAME = "jeonse_fraud_embedding"
