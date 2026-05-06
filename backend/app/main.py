from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.db_init import init_db

app = FastAPI(title="Ebook2LateX API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(api_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Ebook2LateX backend is running"}
