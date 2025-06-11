"""
쿼리 전처리 모듈 - 일상어를 법률어로 변환
"""
from functools import lru_cache
from langchain_openai import ChatOpenAI
from config.settings import LLM_MODEL


class LegalQueryPreprocessor:
    """일상어를 법률 용어로 변환하는 전처리기"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0.1,  # 일관된 변환을 위해 낮게 설정
            max_tokens=200,
        )
        
        # 캐시를 위한 딕셔너리 (세션 동안 유지)
        self._query_cache = {}
        
        # 기본 용어 매핑 (빠른 처리를 위한 룰베이스)
        self.term_mapping = {
            # 부동산 관련
            "집주인": "임대인",
            "세입자": "임차인", 
            "전세금": "임대차보증금",
            "보증금": "임대차보증금",
            "월세": "차임",
            "방세": "차임",
            "계약서": "임대차계약서",
            "집 나가라": "명도청구",
            "쫓겨나다": "명도",
            "돈 안줘": "채무불이행",
            "돈 못받아": "보증금반환청구",
            "사기": "사기죄",
            "속았다": "기망행위",
            "깡통전세": "전세사기",
            "이중계약": "중복임대",
            
            # 법적 절차 관련
            "고소": "형사고발",
            "고발": "형사고발", 
            "소송": "민사소송",
            "재판": "소송",
            "변호사": "법무사",
            "상담": "법률상담",
            "해결": "분쟁해결",
            "보상": "손해배상",
            "배상": "손해배상",
            
            # 기타
            "계약": "법률행위",
            "약속": "계약",
            "위반": "채무불이행",
            "어기다": "위반하다"
        }
    
    def _apply_rule_based_conversion(self, query: str) -> str:
        """룰베이스 용어 변환 (빠른 처리)"""
        converted_query = query
        for common_term, legal_term in self.term_mapping.items():
            if common_term in converted_query:
                converted_query = converted_query.replace(common_term, legal_term)
        return converted_query
    
    def _is_already_legal_query(self, query: str) -> bool:
        """이미 법률 용어가 포함된 쿼리인지 확인"""
        legal_indicators = [
            "임대인", "임차인", "임대차", "명도", "채무불이행", 
            "손해배상", "민사소송", "형사고발", "보증금반환",
            "법률", "판례", "법령", "소송", "계약서"
        ]
        return any(term in query for term in legal_indicators)
    
    @lru_cache(maxsize=100)
    def _gpt_convert_to_legal_terms(self, user_query: str) -> str:
        """GPT를 사용한 정교한 법률 용어 변환 (캐싱 적용)"""
        try:
            prompt = f"""다음 일상어 질문을 법률 검색에 적합한 전문 용어로 변환해주세요.
            
            원래 질문: {user_query}

            변환 규칙:
            1. 일상어를 정확한 법률 용어로 바꾸기
            - 집주인 → 임대인
            - 세입자 → 임차인  
            - 전세금/보증금 → 임대차보증금
            - 월세 → 차임
            - 계약서 → 임대차계약서
            - 사기 → 전세사기 또는 사기죄
            - 쫓겨나다 → 명도청구

            2. 핵심 법적 쟁점을 부각시키기
            3. 검색에 도움이 되는 관련 법률 키워드 추가
            4. 원래 의미는 유지하면서 더 정확하고 전문적으로 표현

            변환된 검색 쿼리:"""

            messages = [{"role": "user", "content": prompt}]
            response = self.llm.invoke(messages)
            
            # 응답에서 불필요한 부분 제거
            converted = response.content.strip()
            if "변환된 검색 쿼리:" in converted:
                converted = converted.split("변환된 검색 쿼리:")[-1].strip()
            
            return converted
            
        except Exception as e:
            print(f"⚠️ GPT 변환 실패, 룰베이스 변환 사용: {e}")
            return self._apply_rule_based_conversion(user_query)
    
    def convert_query(self, user_query: str) -> tuple[str, str]:
        """
        사용자 쿼리를 법률 검색에 적합하게 변환
        
        Returns:
            tuple: (변환된_쿼리, 변환_방법)
        """
        try:
            # 1. 이미 법률 용어인 경우 그대로 사용
            if self._is_already_legal_query(user_query):
                return user_query, "no_conversion"
            
            # 2. 캐시 확인
            if user_query in self._query_cache:
                return self._query_cache[user_query], "cached"
            
            # 3. 먼저 룰베이스 변환 시도
            rule_converted = self._apply_rule_based_conversion(user_query)
            
            # 4. 룰베이스 변환으로 충분한 경우 (많은 변환이 일어난 경우)
            if len(rule_converted) != len(user_query) or rule_converted != user_query:
                # 룰베이스 변환이 효과가 있었다면 결과 캐싱
                self._query_cache[user_query] = rule_converted
                return rule_converted, "rule_based"
            
            # 5. 복잡한 경우 GPT 변환 (시간이 더 걸리지만 정확함)
            print("🔄 정교한 법률 용어 변환 중...")
            gpt_converted = self._gpt_convert_to_legal_terms(user_query)
            
            # 결과 캐싱
            self._query_cache[user_query] = gpt_converted
            return gpt_converted, "gpt_converted"
            
        except Exception as e:
            print(f"⚠️ 쿼리 변환 오류: {e}")
            return user_query, "error"
