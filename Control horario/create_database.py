from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_size=20,        # eso significa que habrá un máximo de 20 conexiones en el pool
    max_overflow=30,     # eso significa que si se necesitan más conexiones, se pueden crear hasta 30 adicionales (total 50)
    pool_timeout=30      # tiempo de espera antes de error
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()