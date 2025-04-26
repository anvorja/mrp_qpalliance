from flask import Blueprint
from .endpoints.products import products_bp

# Crear un Blueprint principal para la versión 1 de la API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Registrar los endpoints
api_v1.register_blueprint(products_bp, url_prefix='/products')

# Definir una ruta para verificar el estado de la API
@api_v1.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar el estado de la API.
    """
    return {'status': 'ok', 'version': '1.0.0'}, 200
