from typing import List, Dict, Any
from datetime import datetime, timedelta
from data.json_manager import JsonManager


class ReportsService:
    """Servicio de generación de reportes."""
    
    def __init__(self, data_manager=None, inventory_service=None, sales_service=None):
        """Inicializa el servicio de reportes."""
        self.data_manager = data_manager or JsonManager()
        self.inventory_service = inventory_service
        self.sales_service = sales_service
        self.data_updated_callbacks = []  # NEW: Even though reports derive, notify for refresh

    def register_data_updated_callback(self, callback):
        """Register callback."""
        self.data_updated_callbacks.append(callback)

    def _notify_callbacks(self):
        """Notify callbacks."""
        for cb in self.data_updated_callbacks:
            try:
                cb()
            except:
                pass
    
    def get_inventory_report(self) -> Dict[str, Any]:
        """Genera reporte de inventario."""
        products = self.data_manager.get_all_products()
        
        total_products = len(products)
        total_items = sum(p.stock for p in products)
        total_value = sum(p.stock * p.sale_price for p in products)
        low_stock = len([p for p in products if p.stock < p.min_stock])
        
        return {
            'total_products': total_products,
            'total_items': total_items,
            'total_value': total_value,
            'low_stock_count': low_stock,
            'products': products
        }
    
    def get_sales_report_by_date(self, date_str: str = None) -> Dict[str, Any]:
        """Genera reporte de ventas por fecha."""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        sales = self.data_manager.get_sales_by_date(date_str)
        
        total_sales = len(sales)
        total_revenue = sum(s.total for s in sales)
        
        return {
            'date': date_str,
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'average': total_revenue / total_sales if total_sales > 0 else 0,
            'sales': sales
        }
    
    def get_sales_report_by_month(self, year: int, month: int) -> Dict[str, Any]:
        """Genera reporte de ventas por mes."""
        sales = self.data_manager.get_sales_by_month(year, month)
        
        total_sales = len(sales)
        total_revenue = sum(s.total for s in sales)
        
        # Agrupar por día
        daily_sales = {}
        for sale in sales:
            date = sale.date
            if date not in daily_sales:
                daily_sales[date] = 0
            daily_sales[date] += sale.total
        
        return {
            'year': year,
            'month': month,
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'average': total_revenue / total_sales if total_sales > 0 else 0,
            'daily_breakdown': daily_sales,
            'sales': sales
        }
    
    def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene productos más vendidos."""
        return self.data_manager.get_top_sold_products(limit)
    
    def get_sales_summary(self) -> Dict[str, Any]:
        """Obtiene resumen general de ventas."""
        return self.data_manager.get_sales_summary()
    
    def get_category_report(self) -> Dict[str, Any]:
        """Genera reporte por categoría."""
        products = self.data_manager.get_all_products()
        
        categories = {}
        for product in products:
            cat = product.category
            if cat not in categories:
                categories[cat] = {
                    'count': 0,
                    'total_stock': 0,
                    'total_value': 0
                }
            categories[cat]['count'] += 1
            categories[cat]['total_stock'] += product.stock
            categories[cat]['total_value'] += product.stock * product.sale_price
        
        return categories
    
    def get_last_7_days_sales(self) -> Dict[str, float]:
        """Obtiene ventas de los últimos 7 días."""
        sales = self.data_manager.get_all_sales()
        
        daily_sales = {}
        today = datetime.now()
        
        for i in range(7):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            daily_sales[date] = 0
        
        for sale in sales:
            if sale.date in daily_sales:
                daily_sales[sale.date] += sale.total
        
        return dict(sorted(daily_sales.items()))
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Obtiene datos para el dashboard."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Resumen de hoy
        today_sales = self.data_manager.get_sales_by_date(today)
        today_revenue = sum(s.total for s in today_sales)
        
        # Resumen general
        all_sales = self.data_manager.get_all_sales()
        total_revenue = sum(s.total for s in all_sales)
        
        # Inventario
        products = self.data_manager.get_all_products()
        total_products = len(products)
        low_stock = len([p for p in products if p.stock < p.min_stock])
        
        return {
            'today_sales_count': len(today_sales),
            'today_revenue': today_revenue,
            'total_sales': len(all_sales),
            'total_revenue': total_revenue,
            'total_products': total_products,
            'low_stock_count': low_stock,
            'top_products': self.data_manager.get_top_sold_products(5)
        }
    
    def get_last_30_days_sales(self) -> Dict[str, float]:
        """Obtiene ventas de los últimos 30 días."""
        sales = self.data_manager.get_all_sales()
        
        daily_sales = {}
        today = datetime.now()
        
        for i in range(30):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            daily_sales[date] = 0
        
        for sale in sales:
            if sale.date in daily_sales:
                daily_sales[sale.date] += sale.total
        
        return dict(sorted(daily_sales.items()))
    
    def get_all_sales_by_date(self) -> Dict[str, float]:
        """Obtiene ventas agrupadas por fecha (todas las ventas)."""
        sales = self.data_manager.get_all_sales()
        
        daily_sales = {}
        for sale in sales:
            if sale.date not in daily_sales:
                daily_sales[sale.date] = 0
            daily_sales[sale.date] += sale.total
        
        return dict(sorted(daily_sales.items()))
    
    def reset_all_sales(self) -> bool:
        """Elimina todos los registros de ventas. Requiere autenticación."""
        return self.data_manager.clear_all_sales()
