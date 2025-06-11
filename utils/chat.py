from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from retriever.system import OptimizedConditionalRAGSystem
from utils.format import format_docs_optimized

def get_rag_system():
    return OptimizedConditionalRAGSystem(
        legal_db_path="D:/chroma_db_law_real_final",
        news_db_path="D:/ja_chroma_db",
        legal_collection="legal_db",
        news_collection="jeonse_fraud_embedding"
    )

def create_user_friendly_chat_chain():
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3, max_tokens=3000)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 법률 전문가 AI입니다."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
        ("system", "참고자료:
{context}")
    ])
    def user_friendly_retrieve_and_format(x):
        rag = get_rag_system()
        docs, _ = rag.conditional_retrieve(x["question"])
        return format_docs_optimized(docs, "hybrid")
    chain = (
        {
            "context": user_friendly_retrieve_and_format,
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("chat_history", []),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    history = store[session_id]
    if len(history.messages) > 20:
        history.messages = history.messages[-20:]
    return history

def create_chat_chain_with_memory():
    base_chain = create_user_friendly_chat_chain()
    return RunnableWithMessageHistory(
        base_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )