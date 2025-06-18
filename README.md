# 💡 SWITCH-ON
### 판례 기반 AI 부동산 거래 지원 챗봇 서비스

> **"어두운 곳에 불을 켜듯이, AI 챗봇으로 답답하고 어려운 부동산 계약을 시원하게 해결해요!**

판례, 법령해석, 생활법령 Q&A, 뉴스 기사 등 다양한 법률 데이터를 바탕으로 법률 접근성이 낮은 일반인의 부동산 계약을 돕는 법률 전문가 AI 챗봇입니다.  
특히 전세사기가 많아지는 사회현상을 극복하기 위해 일반인이 쉽지만 꼭 필요한 상황에서 부동산 계약을 검토하고 중개인에게도 매물에 대한 객관적인 정보를 수집할 수 있게 돕습니다.

## 📑 발표자료

👉 [SWITCH-ON 서비스 발표자료 보러가기](./LeeseoAn_Portfolio_SWITCH_ON.pdf)


## 🎥 챗봇 발표 및 시연 영상

[![AI 스위치온 시연 영상](https://img.youtube.com/vi/4jeZ1oXFj5Q/0.jpg)](https://youtu.be/4jeZ1oXFj5Q?feature=shared)

**[🔗 유튜브에서 시연 영상 보기](https://youtu.be/4jeZ1oXFj5Q?feature=shared)**

실제 챗봇의 작동 방식과 주요 기능들을 직접 확인해보실 수 있습니다.


### 팀 정보
- **팀명**: SWITCH-ON
- **팀장**: 안이서
- **팀원**: 김은솔, 신수정


## 🚀 주요 기능

- **판례 기반 답변**: 실제 법원 판례를 바탕으로 한 신뢰성 있는 법률 정보 제공
- **전세사기 대응**: 전세사기 피해 등 부동산 문제에 대한 구체적인 해결방안 제시
- **일상어 변환**: 어려운 법률 용어를 일반인이 이해하기 쉬운 표현으로 변환
- **실시간 검색**: 법률 DB와 뉴스 DB를 통한 최신 정보 제공
- **단계별 가이드**: 실천 가능한 구체적 행동방침 제안

## 📁 프로젝트 구조

```bash
SWITCH-ON/
├── core/
│   ├── main.py                 # 메인 애플리케이션
│   ├── config.py              # 설정 및 상수 중앙 관리
│   └── requirements.txt       # 의존성 패키지 목록
├── data/
│   └── database_utils.py      # DB 다운로드 및 초기화 기능
├── AI/
│   ├── query_preprocessor.py  # 법률 쿼리 전처리 클래스
│   ├── rag_system.py          # RAG 시스템 구현
│   ├── chat_chain.py          # 채팅 체인 및 메모리 관리
│   └── document_formatter.py  # 문서 포맷팅 유틸리티
├── UI/
│   ├── styles.py              # Streamlit 커스텀 CSS
│   ├── ui_components.py       # UI 컴포넌트 모듈화
│   └── ads.py                 # 광고 배너 기능
├──.gitignore                  # Git 제외 파일 설정
├── streamlit_all_code.py     # 스트림릿 연결 서비스 실행
└── README.md                 # 프로젝트 문서

```

## 🛠️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd ai-legal-chatbot
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
OpenAI API 키를 환경변수로 설정하거나 Streamlit secrets에 추가:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

또는 `.streamlit/secrets.toml` 파일 생성:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

### 5. 애플리케이션 실행
```bash
streamlit run main.py
```

## 🔧 핵심 모듈 설명

### config.py
- 전역 설정 및 상수 관리
- 데이터베이스 URL, 모델 설정, 법률 용어 매핑 등

### database_utils.py
- 허깅페이스에서 벡터 DB 자동 다운로드
- 임베딩 모델 및 Chroma DB 초기화

### query_preprocessor.py
- 일상어를 법률 용어로 자동 변환
- 룰 기반 변환 + GPT 기반 정교한 변환

### rag_system.py
- 법률 DB와 뉴스 DB를 활용한 조건부 검색
- 벡터 유사도 기반 문서 검색

### chat_chain.py
- LangChain 기반 대화형 AI 체인
- 메모리 기능으로 대화 맥락 유지

### ui_components.py
- Streamlit UI 컴포넌트 모듈화
- 헤더, 사이드바, 채팅 인터페이스 등

## 🎯 사용법

1. **질문 입력**: 부동산 관련 법률 문제를 자연어로 입력
2. **자동 변환**: AI가 일상어를 법률 용어로 자동 변환
3. **검색 수행**: 법률 DB와 뉴스 DB에서 관련 자료 검색
4. **답변 생성**: 판례, 법령해석례, 뉴스를 종합하여 맞춤형 답변 제공
5. **행동방침**: 단계별 실행 계획과 주의사항 안내

## 📋 주요 기능

### 법률 쿼리 전처리
```python
# 일상어 → 법률 용어 자동 변환
"집주인이 보증금을 안 줘요" → "임대인의 임대차보증금 반환 의무"
```

### 다중 데이터베이스 검색
- **법률 DB**: 판례, 법령해석례, 생활법령 Q&A
- **뉴스 DB**: 최신 부동산 관련 뉴스

### 구조화된 답변 형식
- 유사 판례 요약
- 관련 뉴스
- 법령해석례 참고
- 행동방침 제안
- 유의사항

## ⚠️ 주의사항

- 본 서비스는 법률 정보를 참고용으로 제공하는 AI입니다.
- 중요한 법적 문제는 반드시 변호사와 상담하시기 바랍니다.

## 🔗 의존성

주요 라이브러리:
- `streamlit`: 웹 인터페이스
- `langchain`: AI 체인 구축
- `sentence-transformers`: 텍스트 임베딩
- `chromadb`: 벡터 데이터베이스
- `openai`: GPT 모델 활용

---

**SWITCH-ON 팀**
- 2025년 국민행복 서비스 발굴·창업경진대회 참가작

