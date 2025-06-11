# 🏠 AI SwitchOn: 판례 기반 부동산 법률 챗봇

GPT-4o와 KoSBERT 기반의 한국 부동산 법률 RAG 시스템

## 주요 기능
- 전세사기, 보증금 반환 등 판례 기반 상담
- KoSBERT + BM25 하이브리드 검색
- 판례, 뉴스, 해석례 구분된 답변
- Streamlit 기반 챗봇 UI

## 실행 방법
```
pip install -r requirements.txt
streamlit run main.py
```

.env 파일에 다음 포함:
```
OPENAI_API_KEY=your_api_key_here
```