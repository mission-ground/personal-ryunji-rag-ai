from abc import ABC, abstractmethod
 
 
class BaseLoader(ABC):
 
    @abstractmethod
    def load(self, pdf_path: str) -> list[str]:
        """PDF 경로를 받아 페이지별 텍스트 리스트를 반환한다."""
        pass
 