# app/db/session.py
from .base import SessionLocal

def get_db():
    """
    Obtiene una sesión de la base de datos.
    Se utiliza como generador para asegurar que la sesión se cierre después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
