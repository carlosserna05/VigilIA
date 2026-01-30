from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import init_db
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s-%(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    tittle=settings.app_name,
    version=settings.app_version,
    description="Sistema de vigilancia con reconocimiento facial con IA",
    debug =settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup_event():
    logger.info(f"Inicilizando {settings.app_name} v{settings.app_version}")
    init_db()
    logger.info("Aplicacion iniciada")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Apagando ")

@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )