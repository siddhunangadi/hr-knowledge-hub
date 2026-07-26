"""FastAPI application entrypoint for HR Knowledge Hub."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.api.retrieval import router as retrieval_router
from app.config.settings import get_settings
from app.utils.logging_config import setup_logging

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(retrieval_router)
app.include_router(chat_router)


@app.get("/")
def root() -> dict[str, object]:
    """Return basic project information."""
    return {
        "project": settings.app_name,
        "version": settings.app_version,
        "phase": 1,
        "status": settings.environment,
    }
