# app/utils/swagger.py
import os
from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint

# Ruta donde estará disponible la documentación Swagger
SWAGGER_URL = '/api/docs'
# Ruta donde estará el archivo JSON con la especificación
API_URL = '/api/spec'


def create_swagger_spec():
    """
    Crea la especificación OpenAPI/Swagger para la API.
    """
    swagger_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Inventory Management API",
            "description": "API para la gestión de inventario de productos",
            "version": "1.0.0",
            "contact": {
                "email": "contact@example.com"
            },
        },
        "servers": [
            {
                "url": "/api/v1",
                "description": "API v1"
            }
        ],
        "tags": [
            {
                "name": "products",
                "description": "Operaciones con productos"
            }
        ],
        "paths": {
            "/products": {
                "get": {
                    "tags": ["products"],
                    "summary": "Obtiene lista de productos",
                    "description": "Retorna una lista paginada de productos",
                    "parameters": [
                        {
                            "name": "skip",
                            "in": "query",
                            "schema": {
                                "type": "integer",
                                "default": 0
                            },
                            "description": "Número de registros a omitir"
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {
                                "type": "integer",
                                "default": 100
                            },
                            "description": "Número máximo de registros a retornar"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Operación exitosa",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Product"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Parámetros de consulta inválidos"
                        },
                        "500": {
                            "description": "Error interno del servidor"
                        }
                    }
                },
                "post": {
                    "tags": ["products"],
                    "summary": "Crea un nuevo producto",
                    "description": "Crea un nuevo producto en el inventario",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ProductCreate"
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Producto creado exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Product"
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Datos inválidos"
                        },
                        "500": {
                            "description": "Error interno del servidor"
                        }
                    }
                }
            },
            "/products/{product_id}": {
                "get": {
                    "tags": ["products"],
                    "summary": "Obtiene un producto por su ID",
                    "description": "Retorna un producto específico basado en su ID",
                    "parameters": [
                        {
                            "name": "product_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "ID del producto"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Operación exitosa",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Product"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Producto no encontrado"
                        },
                        "500": {
                            "description": "Error interno del servidor"
                        }
                    }
                },
                "put": {
                    "tags": ["products"],
                    "summary": "Actualiza un producto",
                    "description": "Actualiza un producto existente por su ID (método tradicional)",
                    "parameters": [
                        {
                            "name": "product_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "ID del producto a actualizar"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ProductUpdate"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Producto actualizado exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Product"
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Datos inválidos"
                        },
                        "404": {
                            "description": "Producto no encontrado"
                        },
                        "500": {
                            "description": "Error interno del servidor"
                        }
                    }
                },
                "patch": {
                    "tags": ["products"],
                    "summary": "Actualiza parcialmente un producto",
                    "description": "Actualiza parcialmente un producto existente por su ID (solo los campos que se envían)",
                    "parameters": [
                        {
                            "name": "product_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "ID del producto a actualizar parcialmente"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ProductUpdate"
                                },
                                "examples": {
                                    "stock_only": {
                                        "summary": "Actualizar solo el stock actual",
                                        "value": {
                                            "current_stock": 100
                                        }
                                    },
                                    "name_only": {
                                        "summary": "Actualizar solo el nombre",
                                        "value": {
                                            "name": "Nuevo nombre del producto"
                                        }
                                    },
                                    "min_stock_only": {
                                        "summary": "Actualizar solo el stock mínimo",
                                        "value": {
                                            "min_stock": 25
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Producto actualizado parcialmente con éxito",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Product"
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Datos inválidos"
                        },
                        "404": {
                            "description": "Producto no encontrado"
                        },
                        "500": {
                            "description": "Error interno del servidor"
                        }
                    }
                },
                "delete": {
                    "tags": ["products"],
                    "summary": "Elimina un producto",
                    "description": "Elimina un producto existente por su ID",
                    "parameters": [
                        {
                            "name": "product_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "ID del producto a eliminar"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Producto eliminado exitosamente"
                        },
                        "404": {
                            "description": "Producto no encontrado"
                        },
                        "500": {
                            "description": "Error interno del servidor"
                        }
                    }
                }
            },
            "/products/alerts": {
                "get": {
                    "tags": ["products"],
                    "summary": "Obtiene productos con alerta de stock",
                    "description": "Retorna productos con stock por debajo del mínimo",
                    "responses": {
                        "200": {
                            "description": "Operación exitosa",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/AlertProduct"
                                        }
                                    }
                                }
                            }
                        },
                        "500": {
                            "description": "Error interno del servidor"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "ProductBase": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Nombre del producto",
                            "maxLength": 100
                        },
                        "code": {
                            "type": "string",
                            "description": "Código único del producto",
                            "maxLength": 50
                        },
                        "current_stock": {
                            "type": "number",
                            "format": "float",
                            "description": "Stock actual del producto",
                            "minimum": 0
                        },
                        "min_stock": {
                            "type": "number",
                            "format": "float",
                            "description": "Stock mínimo del producto",
                            "minimum": 0
                        }
                    },
                    "required": ["name", "code", "current_stock", "min_stock"]
                },
                "ProductCreate": {
                    "$ref": "#/components/schemas/ProductBase"
                },
                "ProductUpdate": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Nombre del producto",
                            "maxLength": 100
                        },
                        "current_stock": {
                            "type": "number",
                            "format": "float",
                            "description": "Stock actual del producto",
                            "minimum": 0
                        },
                        "min_stock": {
                            "type": "number",
                            "format": "float",
                            "description": "Stock mínimo del producto",
                            "minimum": 0
                        }
                    }
                },
                "Product": {
                    "allOf": [
                        {
                            "$ref": "#/components/schemas/ProductBase"
                        },
                        {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "description": "ID único del producto"
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Fecha de creación"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Fecha de última actualización",
                                    "nullable": True
                                }
                            }
                        }
                    ]
                },
                "AlertProduct": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "ID único del producto"
                        },
                        "name": {
                            "type": "string",
                            "description": "Nombre del producto"
                        },
                        "code": {
                            "type": "string",
                            "description": "Código del producto"
                        },
                        "current_stock": {
                            "type": "number",
                            "format": "float",
                            "description": "Stock actual del producto"
                        },
                        "min_stock": {
                            "type": "number",
                            "format": "float",
                            "description": "Stock mínimo del producto"
                        },
                        "difference": {
                            "type": "number",
                            "format": "float",
                            "description": "Diferencia entre stock mínimo y actual"
                        }
                    },
                    "required": ["id", "name", "code", "current_stock", "min_stock", "difference"]
                }
            }
        }
    }

    return swagger_spec


def setup_swagger(app):
    """
    Configura Swagger UI para la aplicación Flask.
    """

    # Endpoint para servir la especificación OpenAPI
    @app.route(API_URL)
    def get_spec():
        return jsonify(create_swagger_spec())

    # Crear y registrar el blueprint de Swagger UI
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Inventory Management API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app