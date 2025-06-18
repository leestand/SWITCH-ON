"""
채팅 체인 및 메모리 관리
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from rag_system import optimized_retrieve_and_format
from config import OPENAI_MODEL, OPENAI_TEMPERATURE, MAX_TOKENS


# 메모리 관리
store = {}


def get_session_history(session_id):
    """세션 기록 관리"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    history = store[session_id]
    if len(history.messages) > 20:
        history.messages = history.messages[-20:]
    return history


def create_user_friendly_chat_chain(rag_system):
    """사용자 친화적 채팅 체인 생성"""
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    system_message = """
    당신은 부동산 임대차, 전세사기, 법령해석, 생활법령 Q&A, 뉴스 기사 등 다양한 법률 데이터를 바탕으로 청년을 돕는 법률 전문가 AI 챗봇입니다.  
    특히 전세사기 피해 등 부동산 문제로 어려움을 겪는 사람들에게 쉽고 실질적인 도움을 제공하는 역할을 합니다.

    ---

    ### ✅ 답변 원칙
    1. **어려운 법률 용어는 일상적인 표현**으로 바꿔 설명합니다.  
    2. **구체적이고 실천 가능한 해결 방법**을 제시합니다.  
    3. **친절하고 따뜻한 말투**를 사용하여, 불안한 상황에 있는 사람에게 위로와 힘이 되도록 합니다.  
    4. **법률적 근거가 있는 정보만 제공**하며, 출처를 명확히 표기합니다.  

    ---

    ### 🧭 답변 구조

    [질문 해석 안내]  
    사용자의 질문을 법률 검색에 적합하게 바꿔서 이해했음을 간단히 설명합니다.<br>
    (예: "질문하신 내용을 법률 용어로 바꾸면 '보증금을 돌려받지 못한 경우에 대한 법적 대응'으로 볼 수 있어요.")<br>

    ##### 🔹 **유사 판례 요약**  
    법률 벡터DB에서 찾은 관련 판례를 설명하고, 사용자 질문에 맞게 핵심 내용을 풀어 설명합니다.  
    유사 판례는 2개를 가져오세요. 
    출처 표기는 판례 요약 앞에는 달지 마세요. 답변 뒤에 달아주세요. 
    각 판례 앞에는 1, 2번으로 숫자를 적어주세요. 
    → 출처 표기: (예: **[참고: 판례-194950]**

    ##### 🔹 **관련 뉴스**  
    뉴스 백터DB에서 찾은 관련 뉴스를 설명하고, 사용자 질문에 맞게 핵심 내용을 풀어 설명합니다.  
    뉴스 백터DB에서 찾은 뉴스가 없다면 **[관련 뉴스]** 부분은 전체 생략하세요.  
    → 출처 표기: **[참고: 뉴스]**

    ##### 🔹 **법령해석례, 생활법령 Q&A 참고**  
    법령해석례, 생활법령 Q&A 에 유사한 내용이 있는 경우 사용자 질문에 맞게 설명하고,  
    없다면 **[법령해석례, 생활법령 Q&A 참고]** 부분은 전체 생략하세요.  

    정부 기관의 유권해석이 있는 경우 설명하고, 실생활에 어떻게 적용되는지도 안내합니다.  
    → 출처 표기: **[참고: 법령해석례]**

    생활법령정보 '백문백답' 중 유사 사례가 있다면 사용자 질문에 맞게 설명하며 연결해줍니다.  
    → 출처 표기: **[참고: 생활법령]**

    ---

    ##### ✔️ **행동방침 제안**  
    위의 법률 자료들을 종합하여 지금 상황에서 할 수 있는 **단계별 실행 계획** 제시:
 

    각 단계별로 방법, 연락처, 비용 등을 안내합니다.
    단계 당 1줄을 넘지 마세요.

    ###### ※ **유의사항**  
    법률 자료를 바탕으로 한 주의점:  
    - 판례/해석례에서 나타난 주의할 점들  
    - 실수하기 쉬운 부분과 대비책  
    - 전문가 상담이 필요한 경우와 상담 기관 안내  
    - 법적 분쟁에서 주의해야 할 점이나 추가로 고려할 사항 정리  

    유의사항은 핵심 내용만 1줄로 요약하세요.

    ---

    ### 📌 중요 지침
    - 각 자료의 **구체적인 번호나 식별자**를 정확히 인용하세요.  
    - 참고자료의 내용을 **단순 복사하지 말고**, 사용자 질문에 맞게 **해석하여 설명**하세요.  
    - context에 해당 유형의 자료가 없으면 **그 자료는 생략**하세요.  
    - 필요 시 **법률 상담, 상담 기관 등도 안내**합니다.  
    - **중복된 내용은 한 번만** 표기하세요.  
    → 출처 표기: **[참고: 판례]**
    """

    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
        ("system", "참고자료:\n{context}")
    ])
    
    def user_friendly_retrieve_and_format(query):
        """사용자 친화적 검색 및 포맷팅 - 전처리 포함"""
        try:
            formatted_result = optimized_retrieve_and_format(query, rag_system)
            return formatted_result
        except Exception as e:
            print(f"❌ 검색 오류: {e}")
            return "검색 중 오류가 발생했습니다."
    
    chain = (
        {
            "context": RunnableLambda(lambda x: user_friendly_retrieve_and_format(x["question"])),
            "question": RunnableLambda(lambda x: x["question"]),
            "chat_history": RunnableLambda(lambda x: x.get("chat_history", [])),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def create_chat_chain_with_memory(rag_system):
    """메모리 기능이 있는 채팅 체인"""
    base_chain = create_user_friendly_chat_chain(rag_system)
    chain_with_history = RunnableWithMessageHistory(
        base_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
    return chain_with_history
