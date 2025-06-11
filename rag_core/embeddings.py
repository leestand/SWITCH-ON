
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import OpenAIEmbeddings
import os

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class OptimizedKoSBERTEmbeddings(metaclass=SingletonMeta):
    def __init__(self):
        self.embedder = HuggingFaceEmbeddings(
            model_name="jhgan/ko-sbert-nli",
            model_kwargs={'device': 'cpu'}
        )

    def get(self):
        return self.embedder

class OptimizedChromaDefaultEmbeddings(metaclass=SingletonMeta):
    def __init__(self):
        self.embedder = OpenAIEmbeddings(model="text-embedding-3-small")

    def get(self):
        return self.embedder
