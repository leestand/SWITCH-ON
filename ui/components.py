"""
UI 컴포넌트 모듈
"""
import streamlit as st


def display_header():
    """헤더 컴포넌트 표시"""
    st.markdown("""
    <div class="header-container">
        <div class="header-title">💡 <span class="highlight">AI 스위치온</span></div>
        <div class="header-subtitle">판례 기반 AI 부동산 거래 지원 서비스</div>
        <div style="margin-top: 1rem; font-size: 1rem; color: #e5e7eb;">
            💡 상황을 자세하게 설명해주시면 맞춤형 법률 정보를 제공해드립니다
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_sidebar(example_questions):
    """사이드바 컴포넌트 표시"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #6b21a8; margin-bottom: 1rem;">🔍 빠른 질문</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 예시 질문 버튼들
        for i, q in enumerate(example_questions):
            if st.button(f" {q}", key=f"example_{i}", use_container_width=True):
                st.session_state["sidebar_prompt"] = q
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 대화 기록 초기화 버튼
        if st.button("↻ 대화 기록 초기화", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 서비스 안내
        st.markdown("""
        <div class="sidebar-card" style="border: 2px solid #8b5cf6; padding: 1rem; border-radius: 0.5rem; box-shadow: 2px 2px 10px rgba(139, 92, 246, 0.2);">
            <h4 style="color: #6b21a8; margin-bottom: 1rem;">✔️ 서비스 안내</h4>
            <ul style="color: #4b5563; line-height: 1.6; font-weight: bold;">
                <li>부동산 관련 법률 문제 상담</li>
                <li>판례 기반 답변 제공</li>
                <li>전세사기 피해 대처방안 안내</li>
                <li>일반인도 이해하기 쉬운 설명</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # 주의사항
        st.markdown("""
        <div class="sidebar-card" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 2px solid #f5bd5f;">
            <h4 style="color: #80370b; margin-bottom: 1rem;">⚠️ 주의사항</h4>
            <ul style="color: #92400e; line-height: 1.6; margin: 0;">
                <li>본 서비스는 부동산 법률 정보를 참고용으로 제공하는 AI로, 법률 전문가가 아닙니다.</li>
                <li>중요한 법적 문제는 반드시 변호사와 상담하시며, 챗봇의 답변에 대한 법적 책임을 지지 않습니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def display_ad_banner():
    """광고 배너 컴포넌트 표시"""
    st.markdown("---")
    st.markdown('<h5 style="color: #b45309;">✨ 추천 부동산 전문가</h5>', unsafe_allow_html=True)

    ads = [
        {
            "img": "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20180518_269%2F1526627900915a2haI_PNG%2FDhZnKmpdc0bNIHMpMyeDLuUE.png",
            "title": "🏢 대치래미안공인중개사사무소",
            "phone": "0507-1408-0123",
            "desc": "📍 서울 강남구 대치동",
            "link": "https://naver.me/xslBVRJX"
        },
        {
            "img": "https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20250331_213%2F1743412607070OviNF_JPEG%2F1000049538.jpg",
            "title": "🏡 메종공인중개사사무소",
            "phone": "0507-1431-4203",
            "desc": "🏠 전문 부동산 상담",
            "link": "https://naver.me/IgJnnCcG"
        },
        {
            "img": "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20200427_155%2F15879809374237E6dq_PNG%2FALH-zx7fy26wJg1T6EUOHC0W.png",
            "title": "👑 로얄공인중개사사무소",
            "phone": "02-569-8889",
            "desc": "🌟 신뢰할 수 있는 거래",
            "link": "https://naver.me/5GGPXQe8"
        }
    ]

    for ad in ads:
        st.markdown(f"""
        <div style="
            background-color: #fffbea;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
        ">
            <div style="display: flex; align-items: center;">
                <img src="{ad['img']}" style="width: 3cm; height: 2cm; object-fit: cover; border-radius: 8px; margin-right: 15px;" />
                <div>
                    <p style="margin-bottom: 5px; font-size: 16px; font-weight: 600;">{ad['title']}</p>
                    <p style="margin: 0;">☎ <strong>{ad['phone']}</strong></p>
                    <p style="margin: 0;">{ad['desc']}</p>
                    <a href="{ad['link']}" target="_blank" style="color: #b45309; font-weight: bold;">🔗 바로가기</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("💡 **신뢰할 수 있는 부동산 전문가와 상담하세요**")


def display_footer():
    """푸터 컴포넌트 표시"""
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


def display_chat_message(message):
    """채팅 메시지 표시"""
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


def display_chat_input():
    """채팅 입력창 표시"""
    st.markdown("""
    <div style="position: sticky; bottom: 0; background: rgba(255,255,255,0.95); 
                padding: 1rem; border-radius: 15px; margin-top: 2rem;
                box-shadow: 0 -5px 15px rgba(139, 92, 246, 0.1);
                backdrop-filter: blur(10px);">
    """, unsafe_allow_html=True)
    
    prompt = st.chat_input("💭 질문을 입력하세요 (예: 보증금 돌려받을 수 있을까요?)", key="user_input")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return prompt
