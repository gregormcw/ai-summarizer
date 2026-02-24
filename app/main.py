from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import logger
from app.routes.summarize import router as summarize_router
from app.routes.upload import router as upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App is starting...")
    yield
    logger.info("App is shutting down...")


settings = get_settings()
app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
    debug=settings.debug,
)
app.include_router(summarize_router)
app.include_router(upload_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.version,
    }
