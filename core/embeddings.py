"""
임베딩 모델 관리 모듈
"""
import numpy as np
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL


class SingletonMeta(type):
    """싱글톤 메타클래스"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class OptimizedKoSBERTEmbeddings(metaclass=SingletonMeta):
    """최적화된 KoSBERT 임베딩 클래스"""
    
    def __init__(self, model_name=EMBEDDING_MODEL):
        if not hasattr(self, 'model'):
            print(f"🔄 KoSBERT 모델 로딩: {model_name}")
            self.model = SentenceTransformer(model_name)
            print("✅ KoSBERT 모델 로딩 완료")
    
    @lru_cache(maxsize=128)
    def embed_query_cached(self, text):
        """캐시된 쿼리 임베딩"""
        return tuple(self.model.encode(text))
    
    def embed_documents(self, texts):
        """문서 배치 임베딩"""
        return self.model.encode(texts, batch_size=32)
    
    def embed_query(self, text):
        """단일 쿼리 임베딩"""
        cached_result = self.embed_query_cached(text)
        return np.array(cached_result)


class OptimizedChromaDefaultEmbeddings(metaclass=SingletonMeta):
    """최적화된 ChromaDB 기본 임베딩 클래스"""
    
    def __init__(self):
        if not hasattr(self, 'embedding_function'):
            from chromadb.utils import embedding_functions
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
    
    @lru_cache(maxsize=128)
    def embed_query_cached(self, text):
        """캐시된 쿼리 임베딩"""
        result = self.embedding_function([text])
        return tuple(result[0])
    
    def embed_documents(self, texts):
        """문서 배치 임베딩"""
        try:
            return self.embedding_function(texts)
        except Exception as e:
            print(f"⚠️ 배치 임베딩 실패, 개별 처리: {e}")
            results = []
            for text in texts:
                try:
                    result = self.embedding_function([text])
                    results.append(result[0])
                except Exception as ex:
                    print(f"⚠️ 개별 텍스트 임베딩 실패: {ex}")
                    results.append([0.0] * 384)
            return results
    
    def embed_query(self, text):
        """단일 쿼리 임베딩"""
        try:
            cached_result = self.embed_query_cached(text)
            return np.array(cached_result)
        except Exception as e:
            print(f"⚠️ 쿼리 임베딩 캐시 실패: {e}")
            result = self.embedding_function([text])
            return np.array(result[0])
