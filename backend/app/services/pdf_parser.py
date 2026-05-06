from pathlib import Path
from typing import List

try:
    import fitz
except ImportError:  # pragma: no cover - dependency may be installed later
    fitz = None


def extract_images_from_pdf(pdf_path: str, output_dir: str) -> List[str]:
    if fitz is None:
        raise RuntimeError("PyMuPDF is not installed yet.")

    source_path = Path(pdf_path)
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    document = fitz.open(source_path)
    extracted_files: List[str] = []

    for page_index in range(len(document)):
        page = document[page_index]
        for image_index, image in enumerate(page.get_images(full=True)):
            xref = image[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            extension = base_image.get("ext", "png")
            image_name = f"page_{page_index + 1}_image_{image_index + 1}.{extension}"
            image_path = target_dir / image_name
            image_path.write_bytes(image_bytes)
            extracted_files.append(str(image_path))

    return extracted_files
