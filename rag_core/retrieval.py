
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.document_transformers import LongContextReorder
from rag_core.embeddings import OptimizedKoSBERTEmbeddings, OptimizedChromaDefaultEmbeddings
from rag_core.config import CHROMA_DB_PATH, NEWS_DB_PATH, LEGAL_COLLECTION_NAME, NEWS_COLLECTION_NAME
from rag_core.preprocessing import LegalQueryPreprocessor

class OptimizedConditionalRAGSystem:
    def __init__(self):
        self.legal_db = Chroma(
            collection_name=LEGAL_COLLECTION_NAME,
            persist_directory=CHROMA_DB_PATH,
            embedding_function=OptimizedKoSBERTEmbeddings().get(),
        )
        self.news_db = Chroma(
            collection_name=NEWS_COLLECTION_NAME,
            persist_directory=NEWS_DB_PATH,
            embedding_function=OptimizedChromaDefaultEmbeddings().get(),
        )
        self.legal_keyword_retriever = BM25Retriever.from_documents(self.legal_db.get())
        self.legal_keyword_retriever.k = 10
        self.reorder = LongContextReorder()
        self.preprocessor = LegalQueryPreprocessor()

    def get_retriever(self, query: str):
        if any(x in query for x in ["뉴스", "기사", "언론"]):
            return self.news_db.as_retriever(search_kwargs={"k": 5})
        else:
            processed_query = self.preprocessor.preprocess(query)
            keyword_retriever = self.legal_keyword_retriever
            vector_retriever = self.legal_db.as_retriever(search_kwargs={"k": 10})
            return EnsembleRetriever(
                retrievers=[keyword_retriever, vector_retriever],
                weights=[0.5, 0.5]
            ) | self.reorder
