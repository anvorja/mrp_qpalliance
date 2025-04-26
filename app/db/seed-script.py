# app/db/seed-script.py
"""
Script para poblar la base de datos con datos iniciales de prueba.
"""

import os
import sys
from sqlalchemy.orm import Session

# Asegurar que podemos importar desde el directorio raíz
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.base import engine, Base
from app.models.product import Product

# Lista de productos de ejemplo para insertar
SAMPLE_PRODUCTS = [
    {
        "name": "Tornillo hexagonal 10mm",
        "code": "TOR-HEX-001",
        "current_stock": 150,
        "min_stock": 50
    },
    {
        "name": "Tuerca autoblocante 8mm",
        "code": "TUE-AUTO-002",
        "current_stock": 300,
        "min_stock": 100
    },
    {
        "name": "Arandela plana 12mm",
        "code": "ARA-PLA-003",
        "current_stock": 400,
        "min_stock": 100
    },
    {
        "name": "Cable eléctrico 2.5mm (metro)",
        "code": "CAB-ELEC-004",
        "current_stock": 200,
        "min_stock": 50
    },
    {
        "name": "Pintura blanca mate (litro)",
        "code": "PIN-BLA-005",
        "current_stock": 25,
        "min_stock": 10
    },
    {
        "name": "Cemento Portland (saco 25kg)",
        "code": "CEM-PORT-006",
        "current_stock": 15,
        "min_stock": 5
    },
    {
        "name": "Varilla de acero 10mm x 6m",
        "code": "VAR-ACE-007",
        "current_stock": 50,
        "min_stock": 15
    },
    {
        "name": "Ladrillo cerámico estándar",
        "code": "LAD-CER-008",
        "current_stock": 1000,
        "min_stock": 200
    },
    {
        "name": "Perfil de aluminio 2m",
        "code": "PERF-ALU-009",
        "current_stock": 30,
        "min_stock": 10
    },
    {
        "name": "Disco de corte metal 115mm",
        "code": "DISC-MET-010",
        "current_stock": 45,
        "min_stock": 20
    },
    {
        "name": "Silicona transparente (tubo)",
        "code": "SIL-TRA-011",
        "current_stock": 28,
        "min_stock": 15
    },
    {
        "name": "Cinta aislante negra",
        "code": "CIN-AIS-012",
        "current_stock": 60,
        "min_stock": 25
    },
    # Productos con stock por debajo del mínimo (para probar alertas)
    {
        "name": "Madera contrachapada 120x240cm",
        "code": "MAD-CONT-013",
        "current_stock": 5,
        "min_stock": 10
    },
    {
        "name": "Bisagra de acero inoxidable",
        "code": "BIS-INOX-014",
        "current_stock": 12,
        "min_stock": 20
    },
    {
        "name": "Clavos 2 pulgadas (caja)",
        "code": "CLA-2P-015",
        "current_stock": 8,
        "min_stock": 15
    }
]

def create_sample_products():
    """Crea productos de ejemplo en la base de datos."""
    # Crear una sesión
    with Session(engine) as session:
        # Verificar si ya existen productos
        existing_products = session.query(Product).count()
        if existing_products > 0:
            print(f"La base de datos ya tiene {existing_products} productos.")
            option = input("¿Desea borrar los datos existentes y crear nuevos? (s/n): ")
            if option.lower() != 's':
                print("Operación cancelada.")
                return
            
            # Borrar datos existentes
            session.query(Product).delete()
            session.commit()
            print("Datos existentes eliminados.")
        
        # Insertar nuevos productos
        for product_data in SAMPLE_PRODUCTS:
            product = Product(
                name=product_data["name"],
                code=product_data["code"],
                current_stock=product_data["current_stock"],
                min_stock=product_data["min_stock"]
            )
            session.add(product)
        
        # Guardar cambios
        session.commit()
        
        print(f"Se han creado {len(SAMPLE_PRODUCTS)} productos de ejemplo en la base de datos.")
        
        # Mostrar algunos productos para verificar
        products = session.query(Product).limit(5).all()
        print("\nAlgunos productos creados:")
        for product in products:
            print(f"- {product.code}: {product.name} (Stock: {product.current_stock}/{product.min_stock})")
        
        # Mostrar productos con alerta
        alerts = session.query(Product).filter(Product.current_stock < Product.min_stock).all()
        print(f"\nProductos con alerta de stock bajo: {len(alerts)}")
        for product in alerts:
            print(f"- {product.code}: {product.name} (Stock: {product.current_stock}/{product.min_stock})")

if __name__ == "__main__":
    create_sample_products()
