"""
Streamlit 커스텀 CSS 스타일 정의
"""
import streamlit as st


def load_custom_css():
    """커스텀 CSS 스타일 로드"""
    st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #f5f3ff 0%, #faf9ff 50%, #fffbeb 100%);
    }
    
    /* 메인 컨테이너 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* 헤더 스타일 */
    .header-container {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 50%, #c4b5fd 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        color: #fef3c7;
        font-size: 1.2rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .highlight {
        color: #fbbf24;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 채팅 컨테이너 */
    .chat-container {
        background: transparent;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* 사용자 메시지 */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 1rem 0;
        animation: slideInRight 0.3s ease-out;
    }
    
    .user-bubble {
        max-width: 75%;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 8px 20px;
        border: 2px solid #f59e0b;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
        position: relative;
    }
    
    .user-bubble::before {
        content: '👤';
        position: absolute;
        right: -0.5rem;
        top: -0.5rem;
        background: #f59e0b;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    /* AI 메시지 */
    .ai-message {
        display: flex;
        justify-content: flex-start;
        margin: 1rem 0;
        animation: slideInLeft 0.3s ease-out;
    }
    
    .ai-bubble {
        max-width: 75%;
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 8px;
        border: 2px solid #8b5cf6;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
        position: relative;
    }
    
    .ai-bubble::before {
        content: '🤖';
        position: absolute;
        left: -0.5rem;
        top: -0.5rem;
        background: #8b5cf6;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #c4b5fd;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
    }
    
    /* 사이드바 카드 스타일 */
    .sidebar-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* 제목 스타일 개선 */
    h1, h2, h3 {
        color: #6b21a8;
        font-weight: 700;
    }
    
    /* 구분선 스타일 */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #c4b5fd 50%, transparent 100%);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
