from app.services.ocr_service import OCREngine
from app.services.pdf_parser import extract_images_from_pdf


class ParsePipeline:
    def __init__(self) -> None:
        self.ocr_engine = OCREngine()

    def parse_pdf(self, pdf_path: str, output_dir: str) -> list[str]:
        image_paths = extract_images_from_pdf(pdf_path, output_dir)
        return self.ocr_engine.batch_image_to_latex(image_paths)
