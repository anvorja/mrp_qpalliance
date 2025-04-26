# app/services/product_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, AlertProduct
from typing import List, Optional, cast


class ProductService:
    """
    Servicio para operaciones relacionadas con productos.
    """

    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Obtiene lista de productos paginada.
        """
        products = db.query(Product).offset(skip).limit(limit).all()
        return cast(List[Product], products)  # Cast para asegurar el tipo correcto

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID.
        """
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_product_by_code(db: Session, code: str) -> Optional[Product]:
        """
        Obtiene un producto por su código.
        """
        return db.query(Product).filter(Product.code == code.upper()).first()

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        """
        Crea un nuevo producto.
        """
        # Verificar si ya existe un producto con el mismo código
        existing_product = ProductService.get_product_by_code(db, product.code)
        if existing_product:
            raise ValueError(f"Ya existe un producto con el código {product.code}")

        # Crear nuevo producto
        try:
            db_product = Product(
                name=product.name,
                code=product.code,
                current_stock=product.current_stock,
                min_stock=product.min_stock
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product
        except IntegrityError:
            db.rollback()
            raise ValueError("Error al crear el producto. Verifique los datos.")

    @staticmethod
    def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """
        Actualiza un producto existente.
        """
        db_product = ProductService.get_product_by_id(db, product_id)
        if db_product is None:
            return None

        # Actualizar solo los campos presentes
        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)

        try:
            db.commit()
            db.refresh(db_product)
            return db_product
        except IntegrityError:
            db.rollback()
            raise ValueError("Error al actualizar el producto.")

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """
        Elimina un producto por su ID.
        """
        db_product = ProductService.get_product_by_id(db, product_id)
        if db_product is None:
            return False

        try:
            db.delete(db_product)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise ValueError("Error al eliminar el producto.")

    @staticmethod
    def get_low_stock_products(db: Session) -> List[AlertProduct]:
        """
        Obtiene productos con stock por debajo del mínimo.
        """
        products = cast(List[Product], db.query(Product).filter(Product.current_stock < Product.min_stock).all())

        # Transformar a modelo de alerta
        alerts = []
        for p in products:
            # Convertir explícitamente los valores a tipos primitivos usando getattr para evitar problemas de tipado
            product_id = int(getattr(p, 'id'))
            name = str(getattr(p, 'name'))
            code = str(getattr(p, 'code'))
            current_stock = float(getattr(p, 'current_stock'))
            min_stock = float(getattr(p, 'min_stock'))
            difference = min_stock - current_stock

            alert = AlertProduct(
                id=product_id,
                name=name,
                code=code,
                current_stock=current_stock,
                min_stock=min_stock,
                difference=difference
            )
            alerts.append(alert)

        return alerts