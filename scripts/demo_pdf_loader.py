# 실행 명령어 : python -m scripts.deom_pdf_loader
# 옵션       : python -m scripts.deom_pdf_loader --loader fitz
#              python -m scripts.deom_pdf_loader --loader pdfplumber
#              python -m scripts.deom_pdf_loader --loader both   ← 둘 다 비교 (기본값)
# 사용하는 클래스임

import argparse
from pathlib import Path
from service.rag.ingestion.index_builder import IndexBuilder
from service.rag.ingestion.loader.fitz_loader import FitzLoader
from service.rag.ingestion.loader.pdfplumber_loader import PdfplumberLoader

OUTPUT_DIR = Path("data/output/inspection")                             # pdf로부터 추출된 텍스트를 파일로 저장할 경로.

# CLI 인자 → loader 클래스 매핑
LOADER_MAP = {
      "fitz":       FitzLoader
    , "pdfplumber": PdfplumberLoader
}

def run_loader(loader_name: str) -> list[str]:
    
    """loader 이름을 받아 인스턴스 생성 → IndexBuilder에 주입 → 결과 저장"""

    loader  = LOADER_MAP[loader_name]()         # FitzLoader() or PdfplumberLoader()
    builder = IndexBuilder(loader=loader)        # 주입
    documents = builder.load_documents()

    print(f"\n{'='*60}")
    print(f"  LOADER : {loader_name.upper()}  |  PAGE COUNT : {len(documents)}")
    print(f"{'='*60}")

    lines = [
        f"LOADER : {loader_name.upper()}",
        f"PAGE COUNT : {len(documents)}",
        "",
    ]

    for i, doc in enumerate(documents):
        header = f"===== PAGE {i+1} ====="
        preview = doc[:500]
        separator = "-" * 60

        # 콘솔 출력
        print(f"\n{header}")
        print(preview)
        print(separator)

        # 파일 기록용
        lines += [header, doc, separator, ""]   # 파일엔 전체 텍스트 저장

    # 텍스트 파일로 저장
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"result_{loader_name}.txt"                  # loader명이 들어간  txt 파일 생성
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n✅ 저장 완료 → {output_path}")

    return documents

def save_comparison(docs_a: list[str], docs_b: list[str]) -> None:
    """fitz / pdfplumber 결과를 페이지별로 나란히 비교 파일로 저장"""
 
    lines = ["[COMPARISON] fitz vs pdfplumber", "=" * 60, ""]
 
    for i in range(max(len(docs_a), len(docs_b))):
        lines += [
            f"===== PAGE {i+1} =====",
            "--- fitz ---",
            docs_a[i] if i < len(docs_a) else "(페이지 없음)",
            "",
            "--- pdfplumber ---",
            docs_b[i] if i < len(docs_b) else "(페이지 없음)",
            "=" * 60,
            "",
        ]
 
    output_path = OUTPUT_DIR / "result_comparison.txt"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ 비교 파일 저장 완료 → {output_path}")

def main():
    
    parser = argparse.ArgumentParser(description="PDF loader 비교 테스트")
    parser.add_argument(
          "--loader"
        , choices=["fitz", "pdfplumber", "both"]
        , default="both"
        , help="사용할 loader (기본값: both — 둘 다 실행하여 비교)"
    )
    
    args = parser.parse_args()

    if args.loader == "both":
        
        docs_fitz       = run_loader("fitz")
        docs_pdfplumber = run_loader("pdfplumber")
        save_comparison(docs_fitz, docs_pdfplumber)

        #_save_diff_file(docs_fitz, docs_pdfplumber)

    else:
        run_loader(args.loader)


if __name__ == "__main__":
    main()