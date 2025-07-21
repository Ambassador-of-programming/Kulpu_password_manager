from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем URL для подключения к SQLite
# Вариант 1: Файловая база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///config/database/passwords.db"

# Создаем движок базы данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Необходимо для SQLite
)

# Создаем класс сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()