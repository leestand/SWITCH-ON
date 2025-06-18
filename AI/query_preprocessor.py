"""
법률 쿼리 전처리 클래스
"""
import functools
from langchain_openai import ChatOpenAI
from config import TERM_MAPPING, LEGAL_INDICATORS, OPENAI_MODEL


class LegalQueryPreprocessor:
    """일상어를 법률 용어로 변환하는 전처리기"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.1,
            max_tokens=200,
        )
        
        self._query_cache = {}
        self.term_mapping = TERM_MAPPING
    
    def _apply_rule_based_conversion(self, query: str) -> str:
        """룰 기반 용어 변환"""
        converted_query = query
        for common_term, legal_term in self.term_mapping.items():
            if common_term in converted_query:
                converted_query = converted_query.replace(common_term, legal_term)
        return converted_query
    
    def _is_already_legal_query(self, query: str) -> bool:
        """이미 법률 용어인지 확인"""
        return any(term in query for term in LEGAL_INDICATORS)
    
    @functools.lru_cache(maxsize=100)
    def _gpt_convert_to_legal_terms(self, user_query: str) -> str:
        """GPT를 이용한 법률 용어 변환"""
        try:
            prompt = f"""다음 일상어 질문을 법률 검색에 적합한 전문 용어로 변환해주세요.
            원래 질문: {user_query}
            변환 규칙:
            1. 일상어를 정확한 법률 용어로 바꾸기
            2. 핵심 법적 쟁점을 부각시키기
            3. 검색에 도움이 되는 관련 법률 키워드 추가
            4. 원래 의미는 유지하면서 더 정확하고 전문적으로 표현
            변환된 검색 쿼리:"""

            messages = [{"role": "user", "content": prompt}]
            response = self.llm.invoke(messages)
            
            converted = response.content.strip()
            if "변환된 검색 쿼리:" in converted:
                converted = converted.split("변환된 검색 쿼리:")[-1].strip()
            
            return converted
            
        except Exception as e:
            print(f"⚠️ GPT 변환 실패, 룰베이스 변환 사용: {e}")
            return self._apply_rule_based_conversion(user_query)
    
    def convert_query(self, user_query: str) -> tuple[str, str]:
        """쿼리 변환 메인 함수"""
        try:
            if self._is_already_legal_query(user_query):
                return user_query, "no_conversion"
            
            if user_query in self._query_cache:
                return self._query_cache[user_query], "cached"
            
            rule_converted = self._apply_rule_based_conversion(user_query)
            
            if len(rule_converted) != len(user_query) or rule_converted != user_query:
                self._query_cache[user_query] = rule_converted
                return rule_converted, "rule_based"
            
            print("🔄 정교한 법률 용어 변환 중...")
            gpt_converted = self._gpt_convert_to_legal_terms(user_query)
            
            self._query_cache[user_query] = gpt_converted
            return gpt_converted, "gpt_converted"
            
        except Exception as e:
            print(f"⚠️ 쿼리 변환 오류: {e}")
            return user_query, "error"
