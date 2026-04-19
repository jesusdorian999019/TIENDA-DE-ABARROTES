import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from .data_manager import DataManager
from .models import User, Product, Sale
from config.settings import USERS_FILE, PRODUCTS_FILE, SALES_FILE


class JsonManager(DataManager):
    """Implementación de DataManager usando JSON como almacenamiento.
    
    Esta clase implementa la interfaz DataManager usando archivos JSON.
    Puede ser reemplazada por SqliteManager sin modificar el resto del código.
    """
    
    def __init__(self):
        """Inicializa el gestor JSON."""
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Asegura que los archivos JSON existan."""
        for file_path in [USERS_FILE, PRODUCTS_FILE, SALES_FILE]:
            if not file_path.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=2)
    
    def _read_file(self, file_path: Path) -> List[Dict]:
        """Lee un archivo JSON."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _write_file(self, file_path: Path, data: List[Dict]) -> bool:
        """Escribe un archivo JSON."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error escribiendo archivo: {e}")
            return False
    
    # ==================== USUARIOS ==================== 
    
    def create_user(self, user: User) -> bool:
        """Crea un nuevo usuario."""
        users = self._read_file(USERS_FILE)
        user_dict = user.to_dict()
        user_dict['id'] = str(uuid.uuid4())
        users.append(user_dict)
        return self._write_file(USERS_FILE, users)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por nombre de usuario."""
        users = self._read_file(USERS_FILE)
        for user_data in users:
            if user_data.get('username') == username:
                return User.from_dict(user_data)
        return None
    
    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios."""
        users_data = self._read_file(USERS_FILE)
        return [User.from_dict(u) for u in users_data]
    
    def user_exists(self, username: str) -> bool:
        """Verifica si un usuario existe."""
        return self.get_user_by_username(username) is not None
    
    def update_user(self, user: User) -> bool:
        """Actualiza un usuario."""
        users = self._read_file(USERS_FILE)
        for i, user_data in enumerate(users):
            if user_data.get('id') == user.id:
                users[i] = user.to_dict()
                return self._write_file(USERS_FILE, users)
        return False
    
    def delete_user(self, user_id: str) -> bool:
        """Elimina un usuario."""
        users = self._read_file(USERS_FILE)
        users = [u for u in users if u.get('id') != user_id]
        return self._write_file(USERS_FILE, users)
    
    # ==================== PRODUCTOS ==================== 
    
    def create_product(self, product: Product) -> bool:
        """Crea un nuevo producto."""
        products = self._read_file(PRODUCTS_FILE)
        product_dict = product.to_dict()
        product_dict['id'] = str(uuid.uuid4())
        products.append(product_dict)
        return self._write_file(PRODUCTS_FILE, products)
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Obtiene un producto por ID."""
        products = self._read_file(PRODUCTS_FILE)
        for product_data in products:
            if product_data.get('id') == product_id:
                return Product.from_dict(product_data)
        return None
    
    def get_all_products(self, limit: int = None, offset: int = 0) -> List[Product]:
        """Obtiene todos los productos with pagination."""
        products_data = self._read_file(PRODUCTS_FILE)
        products = [Product.from_dict(p) for p in products_data]
        if limit is not None:
            products = products[offset:offset + limit]
        return products
    
    def get_product_by_code(self, code: str) -> Optional[Product]:
        """Obtiene un producto por código."""
        products = self._read_file(PRODUCTS_FILE)
        for product_data in products:
            if product_data.get('code') == code:
                return Product.from_dict(product_data)
        return None
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Obtiene productos por categoría."""
        products = self._read_file(PRODUCTS_FILE)
        return [Product.from_dict(p) for p in products if p.get('category') == category]
    
    def search_products(self, query: str) -> List[Product]:
        """Busca productos por nombre o código."""
        products = self._read_file(PRODUCTS_FILE)
        query_lower = query.lower()
        return [
            Product.from_dict(p) for p in products
            if query_lower in p.get('name', '').lower() or 
            query_lower in p.get('code', '').lower()
        ]
    
    def update_product(self, product: Product) -> bool:
        """Actualiza un producto."""
        products = self._read_file(PRODUCTS_FILE)
        for i, product_data in enumerate(products):
            if product_data.get('id') == product.id:
                product_dict = product.to_dict()
                product_dict['updated_at'] = datetime.now().isoformat()
                products[i] = product_dict
                return self._write_file(PRODUCTS_FILE, products)
        return False
    
    def delete_product(self, product_id: str) -> bool:
        """Elimina un producto."""
        products = self._read_file(PRODUCTS_FILE)
        products = [p for p in products if p.get('id') != product_id]
        return self._write_file(PRODUCTS_FILE, products)
    
    def update_product_stock(self, product_id: str, quantity: int) -> bool:
        """Actualiza el stock de un producto (decrementa)."""
        products = self._read_file(PRODUCTS_FILE)
        for i, product_data in enumerate(products):
            if product_data.get('id') == product_id:
                product_data['stock'] = max(0, product_data.get('stock', 0) - quantity)
                product_data['updated_at'] = datetime.now().isoformat()
                products[i] = product_data
                return self._write_file(PRODUCTS_FILE, products)
        return False
    
    def get_low_stock_products(self) -> List[Product]:
        """Obtiene productos con stock bajo."""
        products = self._read_file(PRODUCTS_FILE)
        return [
            Product.from_dict(p) for p in products
            if p.get('stock', 0) < p.get('min_stock', 0)
        ]
    
    # ==================== VENTAS ==================== 
    
    def create_sale(self, sale: Sale) -> bool:
        """Registra una venta."""
        sales = self._read_file(SALES_FILE)
        sale_dict = sale.to_dict()
        sale_dict['id'] = str(uuid.uuid4())
        sales.append(sale_dict)
        return self._write_file(SALES_FILE, sales)
    
    def get_sale(self, sale_id: str) -> Optional[Sale]:
        """Obtiene una venta por ID."""
        sales = self._read_file(SALES_FILE)
        for sale_data in sales:
            if sale_data.get('id') == sale_id:
                return Sale.from_dict(sale_data)
        return None
    
    def get_all_sales(self, limit: int = None, offset: int = 0) -> List[Sale]:
        """Obtiene todas las ventas with pagination."""
        sales_data = self._read_file(SALES_FILE)
        sales = [Sale.from_dict(s) for s in sales_data]
        if limit is not None:
            sales = sales[offset:offset + limit]
        return sales
    
    def get_sales_by_date(self, date_str: str) -> List[Sale]:
        """Obtiene ventas de una fecha específica."""
        sales = self._read_file(SALES_FILE)
        return [Sale.from_dict(s) for s in sales if s.get('date') == date_str]
    
    def get_sales_by_month(self, year: int, month: int) -> List[Sale]:
        """Obtiene ventas de un mes específico."""
        sales = self._read_file(SALES_FILE)
        result = []
        for sale_data in sales:
            date_str = sale_data.get('date', '')
            try:
                sale_date = datetime.strptime(date_str, '%Y-%m-%d')
                if sale_date.year == year and sale_date.month == month:
                    result.append(Sale.from_dict(sale_data))
            except Exception:
                pass
        return result
    
    def delete_sale(self, sale_id: str) -> bool:
        """Elimina una venta."""
        sales = self._read_file(SALES_FILE)
        sales = [s for s in sales if s.get('id') != sale_id]
        return self._write_file(SALES_FILE, sales)
    
    # ==================== REPORTES ==================== 
    
    def get_sales_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de ventas."""
        sales = self._read_file(SALES_FILE)
        
        total_sales = len(sales)
        total_revenue = sum(s.get('total', 0) for s in sales)
        
        return {
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'average_per_sale': total_revenue / total_sales if total_sales > 0 else 0
        }
    
    def get_top_sold_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene productos más vendidos."""
        sales = self._read_file(SALES_FILE)
        
        # Agrupar por producto
        products_sold = {}
        for sale in sales:
            product_id = sale.get('product_id', '')
            product_name = sale.get('product_name', '')
            quantity = sale.get('quantity', 0)
            total = sale.get('total', 0)
            
            if product_id not in products_sold:
                products_sold[product_id] = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'total_quantity': 0,
                    'total_revenue': 0
                }
            
            products_sold[product_id]['total_quantity'] += quantity
            products_sold[product_id]['total_revenue'] += total
        
        # Ordenar por cantidad vendida
        sorted_products = sorted(
            products_sold.values(),
            key=lambda x: x['total_quantity'],
            reverse=True
        )
        
        return sorted_products[:limit]
