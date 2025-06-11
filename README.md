# AI 스위치온 - 부동산 법률 상담 AI

부동산 임대차, 전세사기, 법령해석 등 다양한 법률 데이터를 바탕으로 청년을 돕는 법률 전문가 AI 챗봇입니다.

## 🌟 주요 기능

- **판례 기반 답변**: 실제 법원 판례를 바탕으로 한 법률 정보 제공
- **일상어 자동 변환**: 일반인의 질문을 법률 용어로 자동 변환하여 검색 정확도 향상
- **하이브리드 검색**: 벡터 검색과 키워드 검색을 결합한 최적화된 검색 시스템
- **실시간 뉴스 연동**: 최신 부동산 관련 뉴스와 판례 정보 통합 제공
- **사용자 친화적 UI**: 직관적이고 아름다운 채팅 인터페이스

## 🏗️ 시스템 구조

```
ai-law-assistant/
├── main.py                 # Streamlit 앱 실행 파일
├── config/
│   └── settings.py         # 설정 관리
├── core/
│   ├── embeddings.py       # 임베딩 모델 클래스들
│   ├── preprocessor.py     # 쿼리 전처리기
│   ├── rag_system.py       # RAG 시스템 핵심 로직
│   └── document_formatter.py # 문서 포맷팅
├── chains/
│   └── chat_chain.py       # LangChain 체인 관리
├── ui/
│   ├── styles.py           # CSS 스타일
│   ├── components.py       # UI 컴포넌트들
│   └── chat_interface.py   # 채팅 인터페이스
└── utils/
    └── memory.py           # 메모리 관리
```

## 🚀 설치 및 실행

### 1. 필요 조건

- Python 3.8 이상
- OpenAI API 키
- ChromaDB 데이터베이스 (법률 데이터 및 뉴스 데이터)

### 2. 설치

```bash
# 저장소 클론
git clone https://github.com/your-username/ai-law-assistant.git
cd ai-law-assistant

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 설정

`.env.example` 파일을 `.env`로 복사하고 설정값을 입력하세요:

```bash
cp .env.example .env
```

`.env` 파일 내용:
```bash
# OpenAI API 키
OPENAI_API_KEY=your_openai_api_key_here

# ChromaDB 경로 설정
CHROMA_DB_PATH=D:/chroma_db_law_real_final
NEWS_DB_PATH=D:/ja_chroma_db

# 컬렉션 이름
LEGAL_COLLECTION_NAME=legal_db
NEWS_COLLECTION_NAME=jeonse_fraud_embedding
```

### 4. 실행

```bash
streamlit run main.py
```

## 🎯 핵심 기술

### 쿼리 전처리 시스템
- **룰베이스 변환**: 빠른 처리를 위한 일상어→법률어 매핑
- **GPT 기반 변환**: 복잡한 질문에 대한 정교한 법률 용어 변환
- **캐싱 시스템**: 변환 결과 캐싱으로 성능 최적화

### 하이브리드 RAG 시스템
- **벡터 검색**: KoSBERT 768차원 임베딩 기반 의미적 검색
- **키워드 검색**: BM25 알고리즘 기반 정확한 키워드 매칭
- **조건부 검색**: 법률 DB 우선 검색 후 뉴스 DB 보완 검색
- **유사도 임계값**: 검색 결과 품질 보장을 위한 임계값 설정

### 임베딩 최적화
- **싱글톤 패턴**: 메모리 효율적인 모델 관리
- **배치 처리**: 다중 문서 임베딩 최적화
- **캐시 시스템**: LRU 캐시를 통한 반복 쿼리 최적화

## 📊 데이터 소스

- **판례 데이터**: 대법원, 고등법원, 지방법원 판례
- **법령해석례**: 정부 기관 유권해석
- **생활법령 Q&A**: 법제처 생활법령 백문백답
- **뉴스 데이터**: 부동산 관련 최신 뉴스

## 🎨 UI/UX 특징

- **반응형 디자인**: 다양한 화면 크기 지원
- **애니메이션**: 부드러운 메시지 표시 애니메이션
- **그라디언트 스타일**: 현대적이고 시각적으로 매력적인 디자인
- **직관적 네비게이션**: 빠른 질문 버튼 및 사이드바 메뉴

## 🔧 설정 옵션

### 검색 임계값 조정
```python
# config/settings.py
LEGAL_SIMILARITY_THRESHOLD = 0.7  # 법률 검색 임계값
NEWS_SIMILARITY_THRESHOLD = 0.6   # 뉴스 검색 임계값
MIN_RELEVANT_DOCS = 3              # 최소 관련 문서 수
```

### 모델 설정 변경
```python
# config/settings.py
EMBEDDING_MODEL = "jhgan/ko-sbert-sts"  # 임베딩 모델
LLM_MODEL = "gpt-4o"                    # 언어 모델
TEMPERATURE = 0.3                       # 창의성 조절
```

## 📝 사용 예시

### 기본 질문
```
사용자: "전세금을 돌려받을 수 있을까요?"
AI: 법률 용어로 변환하면 '임대차보증금 반환청구'에 관한 문제입니다...
```

### 복잡한 상황 질문
```
사용자: "집주인이 사라지고 집이 경매로 넘어갔는데 어떻게 해야 하나요?"
AI: 이는 '임대차보증금 우선변제권'과 '경매절차에서의 임차인 보호'에 관한 문제입니다...
```

## 🤝 기여 가이드

1. 이슈 생성 또는 기존 이슈 확인
2. 브랜치 생성: `git checkout -b feature/기능명`
3. 변경사항 커밋: `git commit -m "기능: 새로운 기능 추가"`
4. 브랜치 푸시: `git push origin feature/기능명`
5. Pull Request 생성

## ⚠️ 주의사항

- 본 서비스는 **참고용 법률 정보**를 제공하며, 실제 법률 조언을 대체하지 않습니다
- 중요한 법적 문제는 반드시 **변호사와 상담**하시기 바랍니다
- AI 생성 답변에 대한 **법적 책임을 지지 않습니다**

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

- 이슈 제기: [GitHub Issues](https://github.com/your-username/ai-law-assistant/issues)
- 문의: your-email@example.com

## 🙏 감사

- **LangChain**: RAG 시스템 구축
- **Streamlit**: 웹 인터페이스 제공
- **ChromaDB**: 벡터 데이터베이스
- **OpenAI**: GPT 모델 제공
- **KoSBERT**: 한국어 임베딩 모델

---

**AI 스위치온**으로 더 쉽고 정확한 부동산 법률 정보를 얻어보세요! 🏠✨
