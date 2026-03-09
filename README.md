## 📁 Project Structure

```text
backend
├─api
│  └─routes
│      └─chat.py
│
├─core
│  └─config.py
│
├─data
│  ├─chunks
│  ├─processed
│  │  └─text
│  └─raw
│      └─pdf
│          ├─대학생을 위한 실용 금융_제4판 3쇄_금융감독원_(책갈피).pdf
│          └─북브리프_돈의심리학.pdf
│
├─docs
│  └─a.text
│
└─service
   └─rag
      ├─rag_pipeline.py
      │
      ├─components
      │  ├─embedding
      │  │  └─embedder.py
      │  │
      │  └─vectorstore
      │     └─faiss
      │        └─vector_store.py
      │
      ├─generation
      │  └─generator.py
      │
      ├─ingestion
      │  ├─chunker.py
      │  └─index_builder.py
      │
      └─retrieval
         └─retriever.py
```

---

## 🧠 RAG Architecture

이 프로젝트는 **RAG (Retrieval-Augmented Generation)** 구조를 학습하기 위한 예제 프로젝트입니다.

전체 흐름

```
Document → Chunking → Embedding → Vector Store → Retrieval → Generation
```

---

## 📦 Module Responsibilities

### ingestion
문서를 벡터 검색이 가능하도록 준비하는 단계

- 문서 로딩
- 텍스트 청킹
- 임베딩 생성
- 벡터 DB 저장

```
chunker.py
index_builder.py
```

---

### retrieval
사용자의 질문을 기반으로 **관련 문서 검색**

```
retriever.py
```

역할

- Query embedding
- Vector similarity search
- 관련 context 반환

---

### generation
검색된 context를 기반으로 **LLM이 최종 답변 생성**

```
generator.py
```

역할

- Prompt 생성
- LLM 호출
- Answer 반환

---

### components
RAG에서 공통적으로 사용하는 핵심 모듈

```
embedder.py
vector_store.py
```

역할

- Embedding 모델 관리
- Vector DB 관리 (FAISS)

---

### rag_pipeline
RAG 전체 흐름 orchestration

```
query
 ↓
retrieval
 ↓
generation
 ↓
answer
```

```
rag_pipeline.py
```

---

## 🔄 RAG Flow

```
User Query
   ↓
Retriever
   ↓
Relevant Documents
   ↓
Generator
   ↓
Final Answer
```

---

## 📂 Data Structure

```
data
├ raw        → 원본 문서 (pdf 등)
├ processed  → 전처리된 텍스트
└ chunks     → 벡터 검색용 청크 데이터
```

---

## 🚀 Purpose

이 프로젝트는 다음을 목표로 합니다.

- RAG 구조 이해
- Vector Search 동작 이해
- LLM 기반 Retrieval 시스템 설계 학습
- AI 아키텍처 스터디용 예제 코드 제공
