# (main 파이프라인과 분리된 1회성 실행 스크립트)
# RRAG 핵심 프로세스가 아닌 사전 전처리 과정이기 때문
from backend.service.rag.ingestion.index_builder import IndexBuilder

# 전처리 단계: 문서를 임베딩하고 FAISS 인덱스를 빌드 후 저장
# 클래스 명인 IndexBuilder가 마음에 들지 않음.
# index = vector DB 구조 생성이라는데 잘 와 닿지 않음.
# 문서 → embedding → FAISS index
# 이걸 만드는 걸 Indexing이라고 부름.
# build는 “무언가 사용할 수 있는 구조를 만들어 완성한다”는 의미로 많이 씀.

builder = IndexBuilder()                                            # 자바로 따지면 IndexBuilder 클래스를 가지고 인스턴스 생성 후 builder라는 변수에 할당한 것.
embedder, store = builder.build_index()                             # builder 객체의 build 메서드를 실행하여, build의 멤버 변수를 할당
store.save()                                                        # store 객체의 save 메서드를 실행하여 DB에 저장.

print("✅ FAISS index 저장 완료")