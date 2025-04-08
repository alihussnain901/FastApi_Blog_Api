from sqlalchemy import create_engine, false
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{settings.database_user}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()