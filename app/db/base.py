# app/db/base.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Base de datos SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")

# Motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Sesión local para manejar transacciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()
