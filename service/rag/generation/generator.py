#LLM을 호출하는 부분
class Generator:

    def generate(self, query, context):

        prompt = f"""
Context:
{context}

Question:
{query}

Answer:
"""

        print(prompt)

        return "LLM 응답 자리"