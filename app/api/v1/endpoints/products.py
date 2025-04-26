# app/api/v1/endpoints/products.py
from flask import Blueprint, request, jsonify
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService
from app.db.session import get_db
from sqlalchemy.exc import SQLAlchemyError

# Crear un Blueprint para los endpoints de productos
products_bp = Blueprint('products', __name__)


@products_bp.route('', methods=['GET'])
def get_products():
    """
    Obtiene la lista de productos.
    """
    try:
        db = next(get_db())
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))

        # Validar que los parámetros son válidos
        if skip < 0 or limit < 1 or limit > 100:
            return jsonify({
                'error': 'Parámetros de paginación inválidos'
            }), 400

        products = ProductService.get_products(db, skip, limit)
        # Convertir productos a objetos Pydantic para la respuesta
        product_responses = [ProductResponse.model_validate(product) for product in products]
        return jsonify([product.model_dump() for product in product_responses]), 200
    except ValueError:
        return jsonify({
            'error': 'Parámetros de paginación inválidos'
        }), 400
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Error al consultar productos'
        }), 500


@products_bp.route('', methods=['POST'])
def create_product():
    """
    Crea un nuevo producto.
    """
    try:
        db = next(get_db())
        data = request.get_json()

        # Validar los datos recibidos
        product_create = ProductCreate(**data)

        # Intenta crear el producto
        new_product = ProductService.create_product(db, product_create)
        return jsonify(ProductResponse.model_validate(new_product).model_dump()), 201
    except ValueError as e:
        return jsonify({
            'error': f'Datos inválidos: {str(e)}'
        }), 400
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Error al crear el producto'
        }), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    """
    Obtiene un producto por su ID.
    """
    try:
        db = next(get_db())
        product = ProductService.get_product_by_id(db, product_id)

        if product is None:
            return jsonify({
                'error': 'Producto no encontrado'
            }), 404

        return jsonify(ProductResponse.model_validate(product).model_dump()), 200
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Error al consultar el producto'
        }), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    """
    Actualiza completamente un producto existente.
    Requiere todos los campos del producto.
    """
    try:
        db = next(get_db())
        data = request.get_json()

        # Validar los datos recibidos
        product_update = ProductUpdate(**data)

        # Intenta actualizar el producto
        updated_product = ProductService.update_product(db, product_id, product_update)

        if updated_product is None:
            return jsonify({
                'error': 'Producto no encontrado'
            }), 404

        return jsonify(ProductResponse.model_validate(updated_product).model_dump()), 200
    except ValueError as e:
        return jsonify({
            'error': f'Datos inválidos: {str(e)}'
        }), 400
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Error al actualizar el producto'
        }), 500


@products_bp.route('/<int:product_id>', methods=['PATCH'])
def patch_product(product_id: int):
    """
    Actualiza parcialmente un producto existente.
    Solo requiere los campos que se desean actualizar.
    """
    try:
        db = next(get_db())
        data = request.get_json()

        # Validar los datos recibidos - solo los campos proporcionados
        product_update = ProductUpdate(**data)

        # Intenta actualizar parcialmente el producto
        updated_product = ProductService.update_product(db, product_id, product_update)

        if updated_product is None:
            return jsonify({
                'error': 'Producto no encontrado'
            }), 404

        return jsonify(ProductResponse.model_validate(updated_product).model_dump()), 200
    except ValueError as e:
        return jsonify({
            'error': f'Datos inválidos: {str(e)}'
        }), 400
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Error al actualizar el producto'
        }), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    """
    Elimina un producto por su ID.
    """
    try:
        db = next(get_db())
        success = ProductService.delete_product(db, product_id)

        if not success:
            return jsonify({
                'error': 'Producto no encontrado'
            }), 404

        return jsonify({
            'message': f'Producto con ID {product_id} eliminado correctamente'
        }), 200
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Error al eliminar el producto'
        }), 500


@products_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """
    Obtiene productos con stock por debajo del mínimo.
    """
    try:
        db = next(get_db())
        low_stock_products = ProductService.get_low_stock_products(db)
        return jsonify([product.model_dump() for product in low_stock_products]), 200
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Error al consultar alertas de stock'
        }), 500