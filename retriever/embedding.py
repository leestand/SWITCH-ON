import numpy as np
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
from functools import lru_cache

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class OptimizedKoSBERTEmbeddings(metaclass=SingletonMeta):
    def __init__(self, model_name="jhgan/ko-sbert-sts"):
        self.model = SentenceTransformer(model_name)

    @lru_cache(maxsize=128)
    def embed_query_cached(self, text):
        return tuple(self.model.encode(text))

    def embed_documents(self, texts):
        return self.model.encode(texts, batch_size=32)

    def embed_query(self, text):
        return np.array(self.embed_query_cached(text))

class OptimizedChromaDefaultEmbeddings(metaclass=SingletonMeta):
    def __init__(self):
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()

    @lru_cache(maxsize=128)
    def embed_query_cached(self, text):
        return tuple(self.embedding_function([text])[0])

    def embed_documents(self, texts):
        try:
            return self.embedding_function(texts)
        except Exception:
            return [[0.0] * 384 for _ in texts]

    def embed_query(self, text):
        return np.array(self.embed_query_cached(text))