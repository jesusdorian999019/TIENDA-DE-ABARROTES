import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config.settings import (
    APP_TITLE, WINDOW_GEOMETRY, PRIMARY_COLOR, SECONDARY_COLOR,
    LIGHT_BG, TEXT_COLOR, SUCCESS_COLOR, WARNING_COLOR
)
from business.inventory_service import InventoryService
from business.sales_service import SalesService
from business.reports_service import ReportsService
from utils.excel_exporter import ExcelExporter
from ui.inventory_tab import InventoryTab
from ui.sales_tab import SalesTab
from ui.reports_tab import ReportsTab


class MainWindow:
    """Ventana principal de la aplicación."""
    
    def __init__(self, root, username):
        """Inicializa la ventana principal."""
        self.root = root
        self.username = username
        self.root.title(f"{APP_TITLE} - {username}")
        self.root.geometry(WINDOW_GEOMETRY)
        
        # Inicializar servicios
        self.inventory_service = InventoryService()
        self.sales_service = SalesService(inventory_service=self.inventory_service)
        self.reports_service = ReportsService(
            inventory_service=self.inventory_service,
            sales_service=self.sales_service
        )
        
        # NEW: Register callbacks for auto-refresh
        self.refresh_callback = self._refresh_all_tabs
        self.inventory_service.register_data_updated_callback(self.refresh_callback)
        self.sales_service.register_data_updated_callback(self.refresh_callback)
        self.reports_service.register_data_updated_callback(self.refresh_callback)
        
        # Crear UI
        self._create_ui()
        self._setup_styles()
        self._check_alerts()
    
    def _setup_styles(self):
        """Configura estilos de la aplicación."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('TFrame', background=LIGHT_BG)
        style.configure('TLabel', background=LIGHT_BG, foreground=TEXT_COLOR)
        style.configure('TButton', font=('Helvetica', 9))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'), foreground=PRIMARY_COLOR)
        style.configure('Treeview', font=('Helvetica', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
    
    def _create_ui(self):
        """Crea la interfaz principal."""
        # Frame superior con logo/título
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        title = ttk.Label(header, text=APP_TITLE, style='Header.TLabel')
        title.pack(side=tk.LEFT)
        
        user_label = ttk.Label(header, text=f"Usuario: {self.username}", font=('Helvetica', 9))
        user_label.pack(side=tk.RIGHT)
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear tabs
        self.inventory_tab = InventoryTab(
            self.notebook,
            self.inventory_service,
            self.sales_service
        )
        self.notebook.add(self.inventory_tab.frame, text="Inventario")
        
        self.sales_tab = SalesTab(
            self.notebook,
            self.sales_service,
            self.inventory_service
        )
        self.notebook.add(self.sales_tab.frame, text="Ventas")
        
        self.reports_tab = ReportsTab(self.notebook, self.reports_service)
        self.notebook.add(self.reports_tab.frame, text="Reportes")
        
        # Frame inferior con botones de acción
        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, padx=10, pady=10)
        
        export_btn = ttk.Button(footer, text="Exportar a Excel", command=self._export_to_excel)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(footer, text="Actualizar", command=self._refresh_all_tabs)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = ttk.Button(footer, text="❌ Salir", command=self._exit)
        exit_btn.pack(side=tk.RIGHT, padx=5)
    
    def _export_to_excel(self):
        """Exporta datos a Excel."""
        try:
            products = self.inventory_service.get_all_products()
            sales = self.sales_service.get_all_sales()
            
            # Convertir a diccionarios
            products_dict = [
                {
                    'id': p.id,
                    'name': p.name,
                    'category': p.category,
                    'code': p.code,
                    'provider': p.provider,
                    'purchase_price': p.purchase_price,
                    'sale_price': p.sale_price,
                    'stock': p.stock,
                    'min_stock': p.min_stock
                }
                for p in products
            ]
            
            sales_dict = [
                {
                    'id': s.id,
                    'product_name': s.product_name,
                    'quantity': s.quantity,
                    'unit_price': s.unit_price,
                    'total': s.total,
                    'date': s.date,
                    'time': s.time
                }
                for s in sales
            ]
            
            exporter = ExcelExporter()
            file_path = exporter.export(products_dict, sales_dict)
            
            if file_path:
                messagebox.showinfo("Éxito", f"Archivo exportado:\n{file_path}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el archivo")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def _refresh_all_tabs(self):
        """Auto-refresh all tabs when data changes."""
        self.inventory_tab.refresh()
        self.sales_tab.refresh()
        self.reports_tab.refresh()

    def _refresh(self):
        """Manual refresh button."""
        self._refresh_all_tabs()
    
    def _check_alerts(self):
        """Verifica alertas de stock bajo."""
        low_stock_products = self.inventory_service.get_low_stock_products()
        
        if low_stock_products:
            products_list = "\n".join([f"- {p.name} (Stock: {p.stock}/{p.min_stock})" 
                                     for p in low_stock_products[:5]])
            message = f"Productos con stock bajo:\n\n{products_list}"
            
            if len(low_stock_products) > 5:
                message += f"\n\n... y {len(low_stock_products) - 5} más"
            
            messagebox.showwarning("Alerta de Stock", message)
    
    def _exit(self):
        """Sale de la aplicación."""
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.root.destroy()
