from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import Document, FormulaEntry, Log, User


SEED_USER_EMAIL = "teo@dalat.edu.vn"
SEED_USERNAME = "teovietnam"
SEED_FILE_NAME = "Giao_trinh_Toan_12.pdf"


def get_or_create_user(db: Session) -> User:
    user = db.query(User).filter(User.email == SEED_USER_EMAIL).first()
    if user is None:
        user = User(
            user_id=uuid.uuid4(),
            username=SEED_USERNAME,
            email=SEED_USER_EMAIL,
            hashed_password="hashed_password_here",
            full_name="Lê Văn Tèo",
            role="Admin",
            is_active=True,
        )
        db.add(user)
        db.flush()
    return user


def get_or_create_document(db: Session, user: User) -> Document:
    document = (
        db.query(Document)
        .filter(Document.file_name == SEED_FILE_NAME, Document.user_id == user.user_id)
        .first()
    )
    if document is None:
        document = Document(
            id=uuid.uuid4(),
            user_id=user.user_id,
            file_name=SEED_FILE_NAME,
            file_path_url="/uploads/toan12.pdf",
            status="Processed",
            latex_content=r"\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
        )
        db.add(document)
        db.flush()
    return document


def get_or_create_formula(db: Session, document: Document) -> FormulaEntry:
    formula = (
        db.query(FormulaEntry)
        .filter(FormulaEntry.document_id == document.id, FormulaEntry.order_index == 1)
        .first()
    )
    if formula is None:
        formula = FormulaEntry(
            id=uuid.uuid4(),
            document_id=document.id,
            raw_image_path="/uploads/formulas/toan12_formula_1.png",
            latex_content=r"\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            order_index=1,
        )
        db.add(formula)
        db.flush()
    return formula


def get_or_create_log(db: Session, formula: FormulaEntry) -> Log:
    log = db.query(Log).filter(Log.formula_id == formula.id).first()
    if log is None:
        log = Log(
            log_id=uuid.uuid4(),
            formula_id=formula.id,
            processing_time_ms=1280,
            confidence_score=Decimal("0.97"),
            error_type=None,
            error_message=None,
            environment_info={
                "engine": "pix2tex",
                "device": "CPU",
                "container": None,
            },
        )
        db.add(log)
    return log


def seed_data() -> None:
    db = SessionLocal()
    try:
        print("Đang tạo dữ liệu mẫu...")

        user = get_or_create_user(db)
        document = get_or_create_document(db, user)
        formula = get_or_create_formula(db, document)
        get_or_create_log(db, formula)

        db.commit()
        print("Tạo dữ liệu thành công! Bạn có thể kiểm tra trong pgAdmin4.")
    except Exception as exc:
        db.rollback()
        print(f"Có lỗi xảy ra: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
