#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitarios para la aplicación de Gestión de Ferretería.

Uso:
    python -m pytest tests.py -v

Requisitos previos:
    pip install pytest
"""

import pytest
import sys
from pathlib import Path
import tempfile
import json

# Añadir el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from data.models import User, Product, Sale
from data.json_manager import JsonManager
from business.user_service import UserService
from business.inventory_service import InventoryService
from business.sales_service import SalesService
from business.reports_service import ReportsService
from utils.security import SecurityManager
from utils.validators import Validators


class TestSecurityManager:
    """Tests para el gestor de seguridad."""
    
    def test_hash_password(self):
        """Test: Las contraseñas se hashean correctamente."""
        password = "testpassword123"
        hashed = SecurityManager.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert password not in hashed
    
    def test_verify_password_correct(self):
        """Test: Verificación de contraseña correcta."""
        password = "testpassword123"
        hashed = SecurityManager.hash_password(password)
        
        assert SecurityManager.verify_password(password, hashed)
    
    def test_verify_password_incorrect(self):
        """Test: Verificación de contraseña incorrecta."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = SecurityManager.hash_password(password)
        
        assert not SecurityManager.verify_password(wrong_password, hashed)


class TestValidators:
    """Tests para validadores."""
    
    def test_validate_product_name_empty(self):
        """Test: Validación falla para nombre vacío."""
        valid, msg = Validators.validate_product_name("")
        assert not valid
    
    def test_validate_product_name_valid(self):
        """Test: Validación pasa para nombre válido."""
        valid, msg = Validators.validate_product_name("Martillo")
        assert valid
    
    def test_validate_price_valid(self):
        """Test: Validación de precio válido."""
        valid, msg = Validators.validate_price("10.50")
        assert valid
    
    def test_validate_price_negative(self):
        """Test: Validación falla para precio negativo."""
        valid, msg = Validators.validate_price("-10.50")
        assert not valid
    
    def test_validate_quantity_valid(self):
        """Test: Validación de cantidad válida."""
        valid, msg = Validators.validate_quantity("100")
        assert valid
    
    def test_validate_quantity_invalid(self):
        """Test: Validación falla para cantidad no numérica."""
        valid, msg = Validators.validate_quantity("abc")
        assert not valid
    
    def test_validate_username_valid(self):
        """Test: Validación de usuario válido."""
        valid, msg = Validators.validate_username("usuario123")
        assert valid
    
    def test_validate_username_short(self):
        """Test: Validación falla para usuario corto."""
        valid, msg = Validators.validate_username("ab")
        assert not valid


class TestModels:
    """Tests para modelos de datos."""
    
    def test_user_to_dict(self):
        """Test: User se convierte a diccionario correctamente."""
        user = User(id="123", username="admin", password_hash="hash123")
        user_dict = user.to_dict()
        
        assert user_dict['id'] == "123"
        assert user_dict['username'] == "admin"
        assert user_dict['password_hash'] == "hash123"
    
    def test_user_from_dict(self):
        """Test: User se crea desde diccionario correctamente."""
        user_dict = {
            'id': '123',
            'username': 'admin',
            'password_hash': 'hash123',
            'created_at': '2026-04-18T10:00:00'
        }
        user = User.from_dict(user_dict)
        
        assert user.id == "123"
        assert user.username == "admin"
    
    def test_product_to_dict(self):
        """Test: Product se convierte a diccionario correctamente."""
        product = Product(
            id="123",
            name="Martillo",
            category="Herramientas",
            code="MAR001",
            provider="Proveedor A",
            purchase_price=8.50,
            sale_price=12.99,
            stock=50,
            min_stock=10
        )
        product_dict = product.to_dict()
        
        assert product_dict['name'] == "Martillo"
        assert product_dict['sale_price'] == 12.99
        assert product_dict['stock'] == 50


class TestJsonManager:
    """Tests para el gestor JSON."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        # Usar directorio temporal para tests
        self.temp_dir = tempfile.mkdtemp()
        
        # Crear archivo JSON temporal
        self.test_file = Path(self.temp_dir) / "test.json"
        with open(self.test_file, 'w') as f:
            json.dump([], f)
    
    def test_create_user(self):
        """Test: Crear usuario en JSON."""
        user = User(id="", username="testuser", password_hash="hash123")
        # Este test requeriría una implementación más compleja
        # Se mantiene como ejemplo de estructura
        assert user.username == "testuser"
    
    def test_read_write_file(self):
        """Test: Lectura y escritura de archivos JSON."""
        manager = JsonManager()
        
        # Test que los archivos se crean
        assert manager._read_file(Path(self.temp_dir) / "nonexistent.json") == []


class TestUserService:
    """Tests para el servicio de usuarios."""
    
    def test_initialize_default_user(self):
        """Test: Usuario administrador se inicializa."""
        service = UserService()
        success = service.initialize_default_user()
        
        assert success
        assert service.data_manager.user_exists("admin")
    
    def test_authenticate_correct(self):
        """Test: Autenticación con credenciales correctas."""
        service = UserService()
        service.initialize_default_user()
        
        success, msg = service.authenticate("admin", "admin123")
        assert success
    
    def test_authenticate_incorrect(self):
        """Test: Autenticación falla con credenciales incorrectas."""
        service = UserService()
        service.initialize_default_user()
        
        success, msg = service.authenticate("admin", "wrongpassword")
        assert not success


class TestInventoryService:
    """Tests para el servicio de inventario."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.service = InventoryService()
    
    def test_create_product_valid(self):
        """Test: Crear producto con datos válidos."""
        success, msg = self.service.create_product(
            name="Martillo",
            category="Herramientas",
            code="MAR001",
            provider="Proveedor A",
            purchase_price=8.50,
            sale_price=12.99,
            stock=50,
            min_stock=10
        )
        
        assert success
        assert "exitosamente" in msg.lower()
    
    def test_create_product_invalid_name(self):
        """Test: Crear producto con nombre inválido."""
        success, msg = self.service.create_product(
            name="",
            category="Herramientas",
            code="MAR001",
            provider="Proveedor A",
            purchase_price=8.50,
            sale_price=12.99,
            stock=50,
            min_stock=10
        )
        
        assert not success
    
    def test_create_product_invalid_price(self):
        """Test: Crear producto con precio inválido."""
        success, msg = self.service.create_product(
            name="Martillo",
            category="Herramientas",
            code="MAR001",
            provider="Proveedor A",
            purchase_price="invalid",
            sale_price=12.99,
            stock=50,
            min_stock=10
        )
        
        assert not success
    
    def test_get_all_products(self):
        """Test: Obtener todos los productos."""
        products = self.service.get_all_products()
        assert isinstance(products, list)
    
    def test_search_products(self):
        """Test: Buscar productos."""
        self.service.create_product(
            name="Martillo",
            category="Herramientas",
            code="MAR001",
            provider="Proveedor A",
            purchase_price=8.50,
            sale_price=12.99,
            stock=50,
            min_stock=10
        )
        
        results = self.service.search_products("Martillo")
        assert len(results) > 0
        assert results[0].name == "Martillo"


class TestSalesService:
    """Tests para el servicio de ventas."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.inventory_service = InventoryService()
        self.sales_service = SalesService(inventory_service=self.inventory_service)
        
        # Crear un producto de prueba
        self.inventory_service.create_product(
            name="Producto Test",
            category="Test",
            code="TST001",
            provider="Proveedor",
            purchase_price=10.00,
            sale_price=15.00,
            stock=100,
            min_stock=10
        )
    
    def test_register_sale_valid(self):
        """Test: Registrar venta válida."""
        products = self.inventory_service.get_all_products()
        if products:
            product = products[0]
            success, msg = self.sales_service.register_sale(
                product_id=product.id,
                product_name=product.name,
                quantity=5,
                unit_price=product.sale_price
            )
            
            assert success
    
    def test_register_sale_invalid_quantity(self):
        """Test: Registrar venta con cantidad inválida."""
        products = self.inventory_service.get_all_products()
        if products:
            product = products[0]
            success, msg = self.sales_service.register_sale(
                product_id=product.id,
                product_name=product.name,
                quantity="invalid",
                unit_price=product.sale_price
            )
            
            assert not success


class TestReportsService:
    """Tests para el servicio de reportes."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.reports_service = ReportsService()
    
    def test_get_dashboard_data(self):
        """Test: Obtener datos del dashboard."""
        data = self.reports_service.get_dashboard_data()
        
        assert 'today_sales_count' in data
        assert 'today_revenue' in data
        assert 'total_products' in data
        assert 'low_stock_count' in data
    
    def test_get_sales_summary(self):
        """Test: Obtener resumen de ventas."""
        summary = self.reports_service.get_sales_summary()
        
        assert 'total_sales' in summary
        assert 'total_revenue' in summary
        assert 'average_per_sale' in summary
    
    def test_get_inventory_report(self):
        """Test: Obtener reporte de inventario."""
        report = self.reports_service.get_inventory_report()
        
        assert 'total_products' in report
        assert 'total_items' in report
        assert 'total_value' in report
        assert 'low_stock_count' in report


# Tests de integración
class TestIntegration:
    """Tests de integración del sistema completo."""
    
    def test_complete_workflow(self):
        """Test: Flujo completo de operación."""
        # Inicializar servicios
        user_service = UserService()
        inventory_service = InventoryService()
        sales_service = SalesService(inventory_service=inventory_service)
        reports_service = ReportsService(
            inventory_service=inventory_service,
            sales_service=sales_service
        )
        
        # 1. Inicializar usuario
        user_service.initialize_default_user()
        assert user_service.data_manager.user_exists("admin")
        
        # 2. Autenticar
        success, _ = user_service.authenticate("admin", "admin123")
        assert success
        
        # 3. Crear producto
        success, _ = inventory_service.create_product(
            name="Producto Test",
            category="Test",
            code="TEST001",
            provider="Proveedor",
            purchase_price=10.00,
            sale_price=15.00,
            stock=100,
            min_stock=10
        )
        assert success
        
        # 4. Obtener producto
        products = inventory_service.get_all_products()
        assert len(products) > 0
        product = products[0]
        
        # 5. Registrar venta
        success, _ = sales_service.register_sale(
            product_id=product.id,
            product_name=product.name,
            quantity=5,
            unit_price=product.sale_price
        )
        assert success
        
        # 6. Verificar stock actualizado
        updated_product = inventory_service.get_product(product.id)
        assert updated_product.stock < 100
        
        # 7. Obtener reportes
        dashboard = reports_service.get_dashboard_data()
        assert dashboard['today_sales_count'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
