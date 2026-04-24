from typing import List, Optional, Tuple
from datetime import datetime
from data.models import Sale
from data.json_manager import JsonManager
from utils.validators import Validators
import uuid


class SalesService:
    """Servicio de gestión de ventas."""
    
    def __init__(self, data_manager=None, inventory_service=None):
        """Inicializa el servicio de ventas."""
        self.data_manager = data_manager or JsonManager()
        self.validators = Validators()
        self.inventory_service = inventory_service
        self.data_updated_callbacks = []  # NEW: Callbacks

    def register_data_updated_callback(self, callback):
        """Register callback for data updates."""
        self.data_updated_callbacks.append(callback)
    
    def register_sale(self, product_id: str, product_name: str, quantity: float,
                     unit_price: float, unidad: str = "UNIDAD") -> Tuple[bool, str]:
        """
        Registra una venta con validación de stock.

        Returns:
            Tupla (éxito, mensaje)
        """
        # Validar entrada
        valid, msg = self.validators.validate_quantity(str(quantity))
        if not valid:
            return False, msg

        valid, msg = self.validators.validate_price(str(unit_price))
        if not valid:
            return False, msg

        # Validar que existe el servicio de inventario
        if not self.inventory_service:
            return False, "Servicio de inventario no disponible"

        # Validar que el producto existe
        product = self.inventory_service.get_product(product_id)
        if not product:
            return False, "Producto no encontrado"

        # Validar que hay suficiente stock (soporta decimales si flexible_stock=True)
        # Convertir a float para comparación
        available_stock = float(product.stock)
        requested_quantity = float(quantity)

        if available_stock < requested_quantity:
            return False, f"Stock insuficiente. Disponible: {available_stock}, Solicitado: {requested_quantity}"

        # Calcular total
        total = requested_quantity * unit_price

        # Obtener fecha y hora
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')

        # Obtener precio de compra para calcular ganancias
        purchase_price = product.purchase_price

        # Crear venta
        sale = Sale(
            id=str(uuid.uuid4()),
            product_id=product_id,
            product_name=product_name,
            quantity=requested_quantity,
            unit_price=float(unit_price),
            total=float(total),
            purchase_price=float(purchase_price),  # Guardar precio de compra
            unidad=unidad,
            date=date_str,
            time=time_str
        )
        
        # Guardar venta
        if self.data_manager.create_sale(sale):
            # Actualizar stock solo si la venta se registró correctamente
            if self.inventory_service:
                self.inventory_service.update_stock(product_id, quantity)
            
            self._notify_callbacks()
            return True, f"Venta registrada: ${total:.2f}"
        else:
            return False, "Error al registrar venta"

    def _notify_callbacks(self):
        """Notify callbacks."""
        for cb in self.data_updated_callbacks:
            try:
                cb()
            except Exception:
                pass
    
    def get_all_sales(self, limit: int = None, offset: int = 0) -> List[Sale]:
        """Obtiene todas las ventas with pagination."""
        return self.data_manager.get_all_sales(limit, offset)
    
    def get_sale(self, sale_id: str) -> Optional[Sale]:
        """Obtiene una venta por ID."""
        return self.data_manager.get_sale(sale_id)
    
    def get_sales_by_date(self, date_str: str) -> List[Sale]:
        """Obtiene ventas de una fecha."""
        return self.data_manager.get_sales_by_date(date_str)
    
    def get_sales_by_month(self, year: int, month: int) -> List[Sale]:
        """Obtiene ventas de un mes."""
        return self.data_manager.get_sales_by_month(year, month)
    
    def delete_sale(self, sale_id: str) -> Tuple[bool, str]:
        """Elimina una venta."""
        if self.data_manager.delete_sale(sale_id):
            self._notify_callbacks()  # NEW
            return True, "Venta eliminada"
        else:
            return False, "Error al eliminar venta"
    
    def get_daily_summary(self, date_str: str = None) -> dict:
        """Obtiene resumen de ventas del día."""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        sales = self.data_manager.get_sales_by_date(date_str)
        
        total_sales = len(sales)
        total_revenue = sum(s.total for s in sales)
        
        return {
            'date': date_str,
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'average_per_sale': total_revenue / total_sales if total_sales > 0 else 0
        }
    
    def get_monthly_summary(self, year: int, month: int) -> dict:
        """Obtiene resumen de ventas del mes."""
        sales = self.data_manager.get_sales_by_month(year, month)
        
        total_sales = len(sales)
        total_revenue = sum(s.total for s in sales)
        
        return {
            'year': year,
            'month': month,
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'average_per_sale': total_revenue / total_sales if total_sales > 0 else 0
        }
