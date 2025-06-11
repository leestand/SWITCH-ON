"""
채팅 인터페이스 관리 모듈
"""
import uuid
import streamlit as st
from ui.components import (
    display_header, display_sidebar, display_ad_banner, 
    display_footer, display_chat_message, display_chat_input
)


class ChatInterface:
    """채팅 인터페이스 관리 클래스"""
    
    def __init__(self):
        self.example_questions = [
            "전세사기 당했을 때 대처방법은?",
            "보증금을 돌려받을 수 있을까요?",
            "임차권등기명령이란 무엇인가요?",
            "집주인이 등기이전을 안 해줄 때 어떻게 하나요?",
            "집이 경매로 넘어갔을 때 전세보증금은 어떻게 되나요?"
        ]
    
    def initialize_session(self):
        """세션 초기화"""
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
    
    def render_ui(self):
        """UI 렌더링"""
        # 헤더 표시
        display_header()
        
        # 사이드바 표시
        display_sidebar(self.example_questions)
        
        # 채팅 컨테이너 시작
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # 채팅 기록 표시
        for message in st.session_state.chat_history:
            display_chat_message(message)
            
            # AI 답변 후 광고 배너 표시
            if message["role"] == "assistant":
                display_ad_banner()
        
        # 채팅 컨테이너 종료
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 푸터 표시
        display_footer()
    
    def get_user_input(self):
        """사용자 입력 처리"""
        # 사이드바에서의 질문 선택 처리
        prompt = st.session_state.pop("sidebar_prompt", None)
        
        if not prompt:
            # 직접 입력 처리
            prompt = display_chat_input()
        
        return prompt
    
    def add_message(self, role, content):
        """메시지 추가"""
        st.session_state.chat_history.append({"role": role, "content": content})
    
    def process_user_message(self, prompt, chain):
        """사용자 메시지 처리"""
        if not prompt:
            return
        
        # 사용자 메시지 저장
        self.add_message("user", prompt)

        # 로딩 애니메이션과 함께 답변 생성
        with st.spinner("🤖 AI가 판례를 검색하고 답변을 생성하고 있습니다..."):
            try:
                response = chain.invoke(
                    {"question": prompt},
                    config={"configurable": {"session_id": st.session_state.session_id}},
                )
                self.add_message("assistant", response)
            except Exception as e:
                error_message = f"죄송합니다. 답변 생성 중 오류가 발생했습니다: {str(e)}"
                self.add_message("assistant", error_message)

        # 답변 생성 후 페이지 새로고침
        st.rerun()
