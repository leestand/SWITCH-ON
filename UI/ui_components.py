"""
UI 컴포넌트 관리
"""
import streamlit as st


def render_header():
    """헤더 렌더링"""
    st.markdown("""
    <div class="header-container">
        <div class="header-title">💡 <span class="highlight">AI 스위치온</span></div>
        <div class="header-subtitle">판례 기반 AI 부동산 거래 지원 서비스</div>
        <div style="margin-top: 1rem; font-size: 1rem; color: #e5e7eb;">
            💡 상황을 자세하게 설명해주시면 맞춤형 법률 정보를 제공해드립니다
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #6b21a8; margin-bottom: 1rem;">🔍 빠른 질문</h2>
        </div>
        """, unsafe_allow_html=True)
        
        example_questions = [
            "전세사기 당했을 때 대처방법은?",
            "보증금을 돌려받을 수 있을까요?",
            "임차권등기명령이란 무엇인가요?",
            "집주인이 등기이전을 안 해줄 때 어떻게 하나요?",
            "집이 경매로 넘어갔을 때 전세보증금은 어떻게 되나요?"
        ]
        
        for i, q in enumerate(example_questions):
            if st.button(f" {q}", key=f"example_{i}", use_container_width=True):
                st.session_state["sidebar_prompt"] = q
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("↻ 대화 기록 초기화", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        
        return True


def render_system_status(system_ready, legal_db, news_db):
    """시스템 상태 표시"""
    st.markdown("""
    <div class="sidebar-card" style="border: 2px solid #10b981; background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);">
        <h4 style="color: #065f46; margin-bottom: 1rem;">📊 시스템 상태</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if system_ready:
        st.success("✅ 시스템 준비완료")
    else:
        st.error("❌ 시스템 초기화 실패")
    
    # 데이터베이스 상태
    if legal_db:
        st.success("✅ 법률 DB 연결됨")
    else:
        st.warning("⚠️ 법률 DB 미연결")
        
    if news_db:
        st.success("✅ 뉴스 DB 연결됨")
    else:
        st.warning("⚠️ 뉴스 DB 미연결")


def render_service_info():
    """서비스 안내 정보"""
    st.markdown("""
    <div class="sidebar-card" style="border: 2px solid #8b5cf6;">
        <h4 style="color: #6b21a8; margin-bottom: 1rem;">✔️ 서비스 안내</h4>
        <ul style="color: #4b5563; line-height: 1.6; font-weight: bold;">
            <li>부동산 관련 법률 문제 상담</li>
            <li>판례 기반 답변 제공</li>
            <li>전세사기 피해 대처방안 안내</li>
            <li>일반인도 이해하기 쉬운 설명</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def render_disclaimer():
    """주의사항 표시"""
    st.markdown("""
    <div class="sidebar-card" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 2px solid #f5bd5f;">
        <h4 style="color: #80370b; margin-bottom: 1rem;">⚠️ 주의사항</h4>
        <ul style="color: #92400e; line-height: 1.6; margin: 0;">
            <li>본 서비스는 부동산 법률 정보를 참고용으로 제공하는 AI입니다.</li>
            <li>중요한 법적 문제는 반드시 변호사와 상담하시기 바랍니다.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def render_chat_messages(chat_history):
    """채팅 메시지 렌더링"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for message in chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="user-bubble">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif message["role"] == "assistant":
            st.markdown(f"""
            <div class="ai-message">
                <div class="ai-bubble">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_chat_input():
    """채팅 입력 인터페이스"""
    st.markdown("""
    <div style="position: sticky; bottom: 0; background: rgba(255,255,255,0.95); 
                padding: 1rem; border-radius: 15px; margin-top: 2rem;
                box-shadow: 0 -5px 15px rgba(139, 92, 246, 0.1);
                backdrop-filter: blur(10px);">
    """, unsafe_allow_html=True)
    
    prompt = st.chat_input("💭 질문을 입력하세요 (예: 보증금 돌려받을 수 있을까요?)", key="user_input")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return prompt


def render_footer():
    """푸터 렌더링"""
    st.markdown("""
    <div style="margin-top: 3rem; padding: 2rem; text-align: center; 
               background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
               border-radius: 15px; border-top: 3px solid #8b5cf6;">
        <p style="color: #6b7280; margin: 0;">
            💡 <strong>AI 스위치온</strong> | 부동산 법률 상담 AI 서비스<br>
            <span style="font-size: 0.9rem;">※ 본 서비스는 참고용이며, 실제 법률 문제는 전문가와 상담하시기 바랍니다.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
