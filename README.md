# 🏠 AI 스위치온

**Streamlit 기반 부동산 법률 상담 RAG 챗봇 시스템**

AI 스위치온은 전세 사기, 보증금 분쟁 등 부동산 관련 법률 문제에 대해  
**판례 기반 상담**을 제공하는 챗봇 서비스입니다.  
일상어 기반 질문을 법률 용어로 전처리하고,  
유사 판례를 찾아 LLM이 상담을 제공합니다.

---

## 🚀 주요 기능

- ✅ 유사 판례 검색 (Chroma Vector DB + KoSBERT)
- ✅ 일상어 → 법률어 전처리 (키워드 매핑)
- ✅ Streamlit 기반 직관적 UI
- ✅ 사건유형, 당사자, 법령 키워드 기반 필터링
- ✅ 사용자 질문 + 판례 문서로 RAG 응답 생성

---

## 💻 실행 방법

```bash
git clone https://github.com/yourname/legal_rag_switchon.git
cd legal_rag_switchon
pip install -r requirements.txt
streamlit run app/main.py
```

---

## 📁 프로젝트 구조

```
legal_rag_switchon/
├── app/
│   └── main.py                        # Streamlit 진입점
├── rag_core/
│   ├── __init__.py
│   ├── config.py                      # DB 경로, 환경변수
│   ├── preprocessing.py               # LegalQueryPreprocessor
│   ├── embeddings.py                  # KoSBERT & Chroma 임베딩
│   ├── retrieval.py                   # OptimizedConditionalRAGSystem
│   ├── formatter.py                   # format_docs_optimized
│   ├── memory.py                      # 세션 히스토리 관리
│   └── chain.py                       # create_user_friendly_chat_chain, etc.
├── ui/
│   ├── __init__.py
│   ├── css.py                         # load_custom_css
│   └── banner.py                      # display_ad_banner
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🎯 사용 예시

**Q. 보증금을 못 돌려받고 있어요. 어떻게 대응해야 할까요?**

→ 유사 판례 검색 → 전세사기 특별법 관련 판결 요약 제공 → 대응 절차 안내

---

## 👥 팀 소개



---

## 🔮 앞으로의 계획

- 🔗 백문백답, 법령해석례 등 데이터 소스 확장
- 💬 카카오톡 / 슬랙 챗봇 버전 배포
- 🤖 GPT-4o 기반 성능 업그레이드
- 📊 사용자 의도 분류 및 동적 컨텍스트 적용

---

📌 **누구나 쉽게 법률 정보를 찾을 수 있도록,  
AI 스위치온이 돕겠습니다.**
