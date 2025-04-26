# app/models/product.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Product(Base):
    """
    Modelo SQLAlchemy para la tabla de productos.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    current_stock = Column(Float, nullable=False, default=0)
    min_stock = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Product {self.code}: {self.name}>"
