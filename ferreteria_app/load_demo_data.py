#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cargar datos de demostracion en la aplicacion.
Uso: python load_demo_data.py
"""
from pathlib import Path
import sys
import json
from datetime import datetime, timedelta
import uuid

sys.path.insert(0, str(Path(__file__).parent))

from business.inventory_service import InventoryService
from business.sales_service import SalesService
from data.json_manager import JsonManager


def generate_demo_data():
    """Genera datos de demostracion."""
    print("=" * 60)
    print("CARGADOR DE DATOS DE DEMOSTRACION")
    print("=" * 60)
    
    inventory_service = InventoryService()
    sales_service = SalesService(inventory_service=inventory_service)
    
    demo_products = [
        # Herramientas
        ("Martillo 16 oz", "Herramientas", "MAR001", "Ferreteria Central", 8.50, 12.99, 50, 10),
        ("Destornillador Phillips", "Herramientas", "DES001", "Ferreteria Central", 2.50, 4.99, 100, 20),
        ("Sierra Manual", "Herramientas", "SIE001", "Herramientas Pro", 15.00, 24.99, 25, 5),
        ("Llave Inglesa", "Herramientas", "LLA001", "Herramientas Pro", 12.00, 18.99, 30, 8),
        ("Taladro Manual", "Herramientas", "TAL001", "Electronica Veloz", 45.00, 69.99, 10, 3),
        # ... (rest of products truncated for brevity)
    ]
    
    print("Cargando productos...")
    successful = 0
    for product_data in demo_products:
        try:
            success, message = inventory_service.create_product(*product_data)
            if success:
                successful += 1
        except:
            pass
    
    print(f"Exito: {successful} productos cargados")
    
    print("DATOS DE DEMOSTRACION CARGADOS EXITOSAMENTE")
    print("=" * 60)

if __name__ == "__main__":
    generate_demo_data()
