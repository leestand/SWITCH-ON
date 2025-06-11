
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

def get_session_history():
    def get_by_session_id(session_id: str):
        return ChatMessageHistory()
    return get_by_session_id
