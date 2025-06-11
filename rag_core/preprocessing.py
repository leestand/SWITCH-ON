
class LegalQueryPreprocessor:
    def __init__(self):
        self.replacements = {
            "전세 사기": "보증금 반환 문제",
            "월세 미납": "임대차 계약 위반",
            "계약 파기": "임대차 계약 해지",
            "이사 나가야 하는데": "임대차 계약 종료",
            "돈 못 받음": "보증금 반환 청구",
        }

    def preprocess(self, query: str) -> str:
        for key, val in self.replacements.items():
            query = query.replace(key, val)
        return query
