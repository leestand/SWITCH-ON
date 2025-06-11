
from rag_core.memory import get_session_history
from rag_core.formatter import format_docs_optimized
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def create_user_friendly_chat_chain(retriever):
    prompt = ChatPromptTemplate.from_template(
        "다음은 사용자의 질문과 관련된 법률 문서입니다:\n{context}\n\n"
        "사용자의 질문: {question}\n"
        "도움이 되는 법률 상담 답변을 작성해 주세요."
    )
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return (
        {"context": retriever | format_docs_optimized, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

def create_chat_chain_with_memory(chat_chain):
    return RunnableWithMessageHistory(
        chat_chain,
        get_session_history(),
        input_messages_key="question",
        history_messages_key="history",
    )
