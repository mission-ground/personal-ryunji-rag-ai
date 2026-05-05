import pdfplumber
import re
from service.rag.ingestion.loader.base_loader import BaseLoader


class PDFLoader(BaseLoader):

    def __init__(self, header_margin=0.08, footer_margin=0.08, x_tolerance=5, y_tolerance=5):
        self.header_margin = header_margin
        self.footer_margin = footer_margin
        self.x_tolerance   = x_tolerance
        self.y_tolerance   = y_tolerance

    def load(self, pdf_path: str) -> list[str]:
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = self._extract_page(page)
                if text.strip():
                    pages.append(text)
        return pages

    def _extract_page(self, page) -> str:
        height  = page.height
        top     = height * self.header_margin
        bottom  = height * (1 - self.footer_margin)
        cropped = page.crop((0, top, page.width, bottom))
        words   = cropped.extract_words(x_tolerance=self.x_tolerance, y_tolerance=self.y_tolerance)
        if not words:
            return ""
        words_sorted = sorted(words, key=lambda w: (round(w["top"] / 5) * 5, w["x0"]))
        lines = self._group_into_lines(words_sorted)
        return self._clean_text("\n".join(lines))

    def _group_into_lines(self, words, line_gap=6):
        if not words:
            return []
        lines, cur_line, cur_top = [], [words[0]], words[0]["top"]
        for w in words[1:]:
            if abs(w["top"] - cur_top) <= line_gap:
                cur_line.append(w)
            else:
                lines.append(" ".join(wd["text"] for wd in cur_line))
                cur_line, cur_top = [w], w["top"]
        lines.append(" ".join(wd["text"] for wd in cur_line))
        return lines

    def _clean_text(self, text):
        text = text.replace("\u00a0", " ").replace("\r", "\n")
        text = re.sub(r" {3,}", "  ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()