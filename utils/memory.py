"""
메모리 관리 모듈
"""
from langchain_community.chat_message_histories import ChatMessageHistory
from config.settings import MAX_CHAT_HISTORY

# 전역 메모리 저장소
store = {}


def get_session_history(session_id):
    """세션별 채팅 히스토리 관리"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    
    history = store[session_id]
    
    # 최대 히스토리 개수 제한
    if len(history.messages) > MAX_CHAT_HISTORY:
        history.messages = history.messages[-MAX_CHAT_HISTORY:]
    
    return history


def clear_session_history(session_id):
    """특정 세션의 히스토리 삭제"""
    if session_id in store:
        del store[session_id]


def clear_all_history():
    """모든 세션 히스토리 삭제"""
    global store
    store = {}
