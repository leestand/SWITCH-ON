from langchain_openai import ChatOpenAI
from functools import lru_cache

class LegalQueryPreprocessor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=200)
        self._query_cache = {}
        self.term_mapping = {
            "집주인": "임대인", "세입자": "임차인", "전세금": "임대차보증금", "보증금": "임대차보증금",
            "월세": "차임", "방세": "차임", "계약서": "임대차계약서", "집 나가라": "명도청구",
            "쫓겨나다": "명도", "돈 안줘": "채무불이행", "돈 못받아": "보증금반환청구", "사기": "사기죄",
            "속았다": "기망행위", "깡통전세": "전세사기", "이중계약": "중복임대", "고소": "형사고발",
            "소송": "민사소송", "변호사": "법무사", "상담": "법률상담", "보상": "손해배상",
            "계약": "법률행위", "위반": "채무불이행", "어기다": "위반하다"
        }

    def _apply_rule_based_conversion(self, query: str) -> str:
        for k, v in self.term_mapping.items():
            query = query.replace(k, v)
        return query

    def _is_already_legal_query(self, query: str) -> bool:
        legal_indicators = ["임대인", "임차인", "임대차", "명도", "채무불이행", "손해배상", "민사소송", "형사고발"]
        return any(term in query for term in legal_indicators)

    @lru_cache(maxsize=100)
    def _gpt_convert_to_legal_terms(self, user_query: str) -> str:
        prompt = f"일상어를 법률 용어로 변환: {user_query}"
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content.strip()

    def convert_query(self, user_query: str) -> tuple[str, str]:
        if self._is_already_legal_query(user_query):
            return user_query, "no_conversion"
        if user_query in self._query_cache:
            return self._query_cache[user_query], "cached"
        rule_converted = self._apply_rule_based_conversion(user_query)
        if rule_converted != user_query:
            self._query_cache[user_query] = rule_converted
            return rule_converted, "rule_based"
        gpt_converted = self._gpt_convert_to_legal_terms(user_query)
        self._query_cache[user_query] = gpt_converted
        return gpt_converted, "gpt_converted"