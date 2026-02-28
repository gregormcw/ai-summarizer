from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.logging import logger
from app.routes.summarize import router as summarize_router
from app.routes.transcribe import router as transcribe_router
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

# CORS middleware - allows frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(summarize_router)
app.include_router(upload_router)
app.include_router(transcribe_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.version,
    }
