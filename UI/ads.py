"""
광고 배너 표시 기능
"""
import streamlit as st


def display_ad_banner():
    """광고 배너 표시"""
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
