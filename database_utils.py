"""
데이터베이스 다운로드 및 초기화 관련 유틸리티
"""
import os
import requests
import zipfile
import streamlit as st
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from config import DATABASE_URLS, EMBEDDING_MODEL_NAME


@st.cache_resource
def download_and_extract_databases(verbose=True):
    """허깅페이스에서 벡터 DB 다운로드"""
    
    def download_and_unzip(url, extract_to):
        os.makedirs(extract_to, exist_ok=True)
        zip_path = os.path.join(extract_to, "temp.zip")

        # 이미 존재하는지 확인
        if os.path.exists(os.path.join(extract_to, "chroma.sqlite3")) or \
           any(os.path.exists(os.path.join(extract_to, f)) for f in ["index", "chroma", "data"]):
            if verbose:
                print(f"✅ Already exists: {extract_to}")
            return True

        try:
            if verbose:
                print(f"📦 Downloading from {url}...")
            r = requests.get(url, stream=True)
            r.raise_for_status()
            
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            if verbose:
                print(f"🧩 Unzipping to {extract_to}...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)

            os.remove(zip_path)
            return True
        except Exception as e:
            if verbose:
                print(f"❌ Failed to download {url}: {e}")
            return False

    success = True
    for name, url in DATABASE_URLS.items():
        if not download_and_unzip(url, name):
            success = False

    return success


@st.cache_resource
def initialize_embeddings_and_databases():
    """임베딩 모델과 벡터 DB 초기화"""
    try:
        # 1. 벡터 DB 다운로드
        print("📥 벡터 DB 다운로드 중...")
        download_success = download_and_extract_databases(verbose=False)
        if not download_success:
            return None, None, None, False
        
        # 2. 임베딩 모델 초기화
        print("🔄 임베딩 모델 로딩 중...")
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("✅ 임베딩 모델 로딩 완료")
        
        # 3. Chroma DB 연결
        legal_db = None
        news_db = None
        
        if os.path.exists("chroma_db_law_real_final"):
            try:
                legal_db = Chroma(
                    persist_directory="chroma_db_law_real_final",
                    embedding_function=embedding_model
                )
                print("✅ 법률 DB 연결 완료")
            except Exception as e:
                print(f"⚠️ 법률 DB 연결 실패: {e}")
        
        if os.path.exists("ja_chroma_db"):
            try:
                news_db = Chroma(
                    persist_directory="ja_chroma_db",
                    embedding_function=embedding_model
                )
                print("✅ 뉴스 DB 연결 완료")
            except Exception as e:
                print(f"⚠️ 뉴스 DB 연결 실패: {e}")
        
        return embedding_model, legal_db, news_db, True
        
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")
        return None, None, None, False
