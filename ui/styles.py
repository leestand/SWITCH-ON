"""
UI 스타일 관리 모듈
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
