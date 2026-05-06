from app.core.database import Base, engine
from app.models import document, formula_entry, log, user  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
