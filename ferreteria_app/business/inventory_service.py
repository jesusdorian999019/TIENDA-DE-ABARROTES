from typing import List, Optional, Tuple
from data.models import Product
from data.json_manager import JsonManager
from utils.validators import Validators
import uuid


class InventoryService:
    """Servicio de gestión de inventario."""
    
    def __init__(self, data_manager=None):
        """Inicializa el servicio de inventario."""
        self.data_manager = data_manager or JsonManager()
        self.validators = Validators()
        self.data_updated_callbacks = []  # NEW: Observer pattern callbacks

    def register_data_updated_callback(self, callback):
        """Register callback for data updates."""
        self.data_updated_callbacks.append(callback)
    
    def create_product(self, name: str, category: str, code: str, provider: str,
                      purchase_price: float, sale_price: float, stock: int,
                      min_stock: int) -> Tuple[bool, str]:
        """
        Crea un nuevo producto.
        
        Returns:
            Tupla (éxito, mensaje)
        """
        # Validar entrada
        valid, msg = self.validators.validate_product_name(name)
        if not valid:
            return False, msg
        
        valid, msg = self.validators.validate_category(category)
        if not valid:
            return False, msg
        
        valid, msg = self.validators.validate_code(code)
        if not valid:
            return False, msg
        
        valid, msg = self.validators.validate_provider(provider)
        if not valid:
            return False, msg
        
        valid, msg = self.validators.validate_price(str(purchase_price))
        if not valid:
            return False, msg
        
        valid, msg = self.validators.validate_price(str(sale_price))
        if not valid:
            return False, msg
        
        valid, msg = self.validators.validate_quantity(str(stock))
        if not valid:
            return False, msg
        
        valid, msg = self.validators.validate_min_stock(str(min_stock))
        if not valid:
            return False, msg
        
        # Verificar código único
        if self.data_manager.get_product_by_code(code):
            return False, f"El código {code} ya existe"
        
        # Crear producto
        product = Product(
            id=str(uuid.uuid4()),
            name=name,
            category=category,
            code=code,
            provider=provider,
            purchase_price=float(purchase_price),
            sale_price=float(sale_price),
            stock=int(stock),
            min_stock=int(min_stock)
        )
        
        if self.data_manager.create_product(product):
            self._notify_callbacks()  # NEW: Notify UI
            return True, "Producto creado exitosamente"
        else:
            return False, "Error al crear producto"
    
    def update_product(self, product_id: str, name: str, category: str, code: str,
                      provider: str, purchase_price: float, sale_price: float,
                      stock: int, min_stock: int) -> Tuple[bool, str]:
        """Actualiza un producto."""
        # Validar entrada
        valid, msg = self.validators.validate_product_name(name)
        if not valid:
            return False, msg
        
        # Verificar que exista
        product = self.data_manager.get_product(product_id)
        if not product:
            return False, "Producto no encontrado"
        
        # Verificar código único (si cambió)
        if product.code != code:
            if self.data_manager.get_product_by_code(code):
                return False, f"El código {code} ya existe"
        
        # Actualizar
        product.name = name
        product.category = category
        product.code = code
        product.provider = provider
        product.purchase_price = float(purchase_price)
        product.sale_price = float(sale_price)
        product.stock = int(stock)
        product.min_stock = int(min_stock)
        
        if self.data_manager.update_product(product):
            self._notify_callbacks()  # NEW
            return True, "Producto actualizado exitosamente"
        else:
            return False, "Error al actualizar producto"
    
    def delete_product(self, product_id: str) -> Tuple[bool, str]:
        """Elimina un producto."""
        if self.data_manager.delete_product(product_id):
            self._notify_callbacks()  # NEW
            return True, "Producto eliminado exitosamente"
        else:
            return False, "Error al eliminar producto"

    def _notify_callbacks(self):
        """Notify all registered callbacks."""
        for cb in self.data_updated_callbacks:
            try:
                cb()
            except:
                pass
    
    def get_all_products(self, limit: int = None, offset: int = 0) -> List[Product]:
        """Obtiene todos los productos with pagination."""
        return self.data_manager.get_all_products(limit, offset)
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Obtiene un producto por ID."""
        return self.data_manager.get_product(product_id)
    
    def search_products(self, query: str) -> List[Product]:
        """Busca productos."""
        return self.data_manager.search_products(query)
    
    def get_low_stock_products(self) -> List[Product]:
        """Obtiene productos con stock bajo."""
        return self.data_manager.get_low_stock_products()
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Obtiene productos por categoría."""
        return self.data_manager.get_products_by_category(category)
    
    def update_stock(self, product_id: str, quantity: int) -> Tuple[bool, str]:
        """Actualiza stock de un producto."""
        if self.data_manager.update_product_stock(product_id, quantity):
            self._notify_callbacks()  # NEW
            return True, "Stock actualizado"
        else:
            return False, "Error al actualizar stock"
    
    def get_inventory_value(self) -> float:
        """Calcula el valor total del inventario."""
        products = self.data_manager.get_all_products()
        return sum(p.sale_price * p.stock for p in products)
    
    def get_total_items(self) -> int:
        """Obtiene total de items en stock."""
        products = self.data_manager.get_all_products()
        return sum(p.stock for p in products)
