from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentRead
from app.services.parse_pipeline import ParsePipeline

router = APIRouter(prefix="/api", tags=["parse"])
parser = ParsePipeline()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/upload", response_model=DocumentRead)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename
    file_bytes = await file.read()
    file_path.write_bytes(file_bytes)

    document = Document(filename=file.filename, file_path=str(file_path), status="uploaded")
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.post("/process/{document_id}")
def process_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    output_dir = Path(settings.upload_dir) / f"document_{document_id}"
    latex_outputs = parser.parse_pdf(document.file_path, str(output_dir))
    document.status = "processed"
    document.latex_content = "\n".join(filter(None, latex_outputs))
    db.commit()
    db.refresh(document)
    return {"document_id": document.id, "latex_content": document.latex_content, "status": document.status}
