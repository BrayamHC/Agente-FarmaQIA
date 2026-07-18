from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    description="Asistente Inteligente para Farmacias",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(chat_router)