from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from backend.config import settings
from backend.models import Base

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug  
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener sesión de base de datos
    Uso en FastAPI:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()