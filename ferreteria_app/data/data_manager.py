from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .models import User, Product, Sale


class DataManager(ABC):
    """Interfaz abstracta para gestión de datos.
    
    Esta interfaz permite abstraer la capa de datos, permitiendo que la aplicación
    funcione con JSON ahora y migrar fácilmente a SQLite u otra BD en el futuro
    sin modificar el resto del código.
    """
    
    # ==================== USUARIOS ==================== 
    
    @abstractmethod
    def create_user(self, user: User) -> bool:
        """Crea un nuevo usuario."""
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por nombre de usuario."""
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios."""
        pass
    
    @abstractmethod
    def user_exists(self, username: str) -> bool:
        """Verifica si un usuario existe."""
        pass
    
    @abstractmethod
    def update_user(self, user: User) -> bool:
        """Actualiza un usuario."""
        pass
    
    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Elimina un usuario."""
        pass
    
    # ==================== PRODUCTOS ==================== 
    
    @abstractmethod
    def create_product(self, product: Product) -> bool:
        """Crea un nuevo producto."""
        pass
    
    @abstractmethod
    def get_product(self, product_id: str) -> Optional[Product]:
        """Obtiene un producto por ID."""
        pass
    
    @abstractmethod
    def get_all_products(self, limit: int = None, offset: int = 0) -> List[Product]:
        """Obtiene todos los productos with pagination."""
        pass
    
    @abstractmethod
    def get_product_by_code(self, code: str) -> Optional[Product]:
        """Obtiene un producto por código."""
        pass
    
    @abstractmethod
    def get_products_by_category(self, category: str) -> List[Product]:
        """Obtiene productos por categoría."""
        pass
    
    @abstractmethod
    def search_products(self, query: str) -> List[Product]:
        """Busca productos por nombre o código."""
        pass
    
    @abstractmethod
    def update_product(self, product: Product) -> bool:
        """Actualiza un producto."""
        pass
    
    @abstractmethod
    def delete_product(self, product_id: str) -> bool:
        """Elimina un producto."""
        pass
    
    @abstractmethod
    def update_product_stock(self, product_id: str, quantity: int) -> bool:
        """Actualiza el stock de un producto (decrementa)."""
        pass
    
    @abstractmethod
    def get_low_stock_products(self) -> List[Product]:
        """Obtiene productos con stock bajo."""
        pass
    
    # ==================== VENTAS ==================== 
    
    @abstractmethod
    def create_sale(self, sale: Sale) -> bool:
        """Registra una venta."""
        pass
    
    @abstractmethod
    def get_sale(self, sale_id: str) -> Optional[Sale]:
        """Obtiene una venta por ID."""
        pass
    
    @abstractmethod
    def get_all_sales(self, limit: int = None, offset: int = 0) -> List[Sale]:
        """Obtiene todas las ventas with pagination."""
        pass
    
    @abstractmethod
    def get_sales_by_date(self, date_str: str) -> List[Sale]:
        """Obtiene ventas de una fecha específica."""
        pass
    
    @abstractmethod
    def get_sales_by_month(self, year: int, month: int) -> List[Sale]:
        """Obtiene ventas de un mes específico."""
        pass
    
    @abstractmethod
    def delete_sale(self, sale_id: str) -> bool:
        """Elimina una venta."""
        pass
    
    # ==================== REPORTES ==================== 
    
    @abstractmethod
    def get_sales_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de ventas."""
        pass
    
    @abstractmethod
    def get_top_sold_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene productos más vendidos."""
        pass

