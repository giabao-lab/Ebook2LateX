from typing import List

try:
    from pix2tex.cli import LatexOCR
except ImportError:  # pragma: no cover - dependency may be installed later
    LatexOCR = None


class OCREngine:
    def __init__(self) -> None:
        self.model = LatexOCR() if LatexOCR is not None else None

    def image_to_latex(self, image_path: str) -> str:
        if self.model is None:
            return ""
        return self.model(image_path)

    def batch_image_to_latex(self, image_paths: List[str]) -> List[str]:
        return [self.image_to_latex(image_path) for image_path in image_paths]
