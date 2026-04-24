import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import webbrowser
from config.settings import (
    APP_TITLE, APP_VERSION, WINDOW_GEOMETRY, PRIMARY_COLOR, SECONDARY_COLOR,
    LIGHT_BG, TEXT_COLOR, SUCCESS_COLOR, WARNING_COLOR
)
from business.inventory_service import InventoryService
from business.sales_service import SalesService
from business.reports_service import ReportsService
from business.user_service import UserService
from data.json_manager import JsonManager
from utils.excel_exporter import ExcelExporter
from utils.update_checker import UpdateChecker
from ui.inventory_tab import InventoryTab
from ui.sales_tab import SalesTab
from ui.reports_tab import ReportsTab


class MainWindow:
    """Ventana principal de la aplicación."""

    def __init__(self, root, username, user_service=None):
        """Inicializa la ventana principal."""
        self.root = root
        self.username = username
        self.root.title(f"{APP_TITLE} - {username}")
        self.root.geometry(WINDOW_GEOMETRY)

        # COMPARTIR una única instancia de JsonManager entre todos los servicios
        self.data_manager = JsonManager()

        # Inicializar servicios con el mismo data_manager
        self.user_service = user_service if user_service else UserService()
        self.inventory_service = InventoryService(self.data_manager)
        self.sales_service = SalesService(
            inventory_service=self.inventory_service,
            data_manager=self.data_manager
        )
        self.reports_service = ReportsService(
            inventory_service=self.inventory_service,
            sales_service=self.sales_service,
            data_manager=self.data_manager
        )

        # NEW: Register callbacks for auto-refresh
        self.refresh_callback = self._refresh_all_tabs
        self.inventory_service.register_data_updated_callback(self._schedule_refresh)
        self.sales_service.register_data_updated_callback(self._schedule_refresh)
        self.reports_service.register_data_updated_callback(self._schedule_refresh)

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
        # ==================== PANEL DE RESUMEN RÁPIDO ====================
        summary_frame = ttk.LabelFrame(self.root, text="📊 RESUMEN DEL DÍA", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)

        # Labels del resumen
        self.summary_labels = {}
        summary_items = [
            ('ventas_hoy', 'Ventas Hoy:', '$0.00'),
            ('capital_hoy', 'Capital Recup.:', '$0.00'),
            ('ganancia_hoy', 'Ganancia Hoy:', '$0.00'),
            ('stock_total', 'Stock Total:', '0'),
            ('invertido', 'Capital Invert.:', '$0.00'),
            ('valor_inv', 'Valor Invent.:', '$0.00'),
        ]

        for i, (key, label, value) in enumerate(summary_items):
            ttk.Label(summary_frame, text=label, font=('Helvetica', 10, 'bold')).grid(row=0, column=i*2, padx=5, sticky=tk.W)
            self.summary_labels[key] = ttk.Label(summary_frame, text=value, font=('Helvetica', 10, 'bold'), foreground=PRIMARY_COLOR)
            self.summary_labels[key].grid(row=0, column=i*2+1, padx=5, sticky=tk.W)

        # Actualizar resumen
        self._update_summary()

        # Frame superior con logo/título Y botón exportar
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=10, pady=10)

        # Título
        title_frame = ttk.Frame(header)
        title_frame.pack(side=tk.LEFT)

        title = ttk.Label(title_frame, text=APP_TITLE, style='Header.TLabel')
        title.pack(side=tk.LEFT)

        version_label = ttk.Label(title_frame, text=f" v{APP_VERSION}", font=('Helvetica', 8))
        version_label.pack(side=tk.LEFT)

        # Botones de acción
        action_frame = ttk.Frame(header)
        action_frame.pack(side=tk.LEFT, padx=20)

        export_btn = ttk.Button(action_frame, text="Exportar a Excel", command=self._export_to_excel)
        export_btn.pack(side=tk.LEFT, padx=5)

        update_btn = ttk.Button(action_frame, text="Buscar Actualizaciones", command=self._check_updates)
        update_btn.pack(side=tk.LEFT, padx=5)

        exit_btn = ttk.Button(action_frame, text="Salir", command=self._exit)
        exit_btn.pack(side=tk.LEFT, padx=5)

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

        self.reports_tab = ReportsTab(self.notebook, self.reports_service, self.user_service)
        self.notebook.add(self.reports_tab.frame, text="Reportes")

        # Footer - vacío por ahora
        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, padx=10, pady=10)

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
                    'marca': getattr(p, 'marca', ''),  # NUEVO
                    'unidad': getattr(p, 'unidad', 'UNIDAD'),  # NUEVO
                    'purchase_price': p.purchase_price,
                    'sale_price': p.sale_price,
                    'stock': p.stock,
                    'min_stock': p.min_stock,
                    'flexible_stock': getattr(p, 'flexible_stock', False),  # NUEVO
                }
                for p in products
            ]

            sales_dict = [
                {
                    'id': s.id,
                    'product_name': s.product_name,
                    'quantity': s.quantity,
                    'unit_price': s.unit_price,
                    'purchase_price': s.purchase_price,  # NUEVO: para calcular ganancias
                    'total': s.total,
                    'date': s.date,
                    'time': s.time
                }
                for s in sales
            ]

            exporter = ExcelExporter()
            file_path = exporter.export(products_dict, sales_dict)

            if file_path:
                messagebox.showinfo("Exito", f"Archivo exportado:\n{file_path}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el archivo")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    def _check_updates(self):
        """Verifica actualizaciones y redirige al repo si hay."""
        try:
            checker = UpdateChecker()
            result = checker.check_for_updates()

            if result['available']:
                # Hay actualización disponible
                msg = f"Nueva versión disponible: {result['latest_version']}\nVersión actual: {result['current_version']}\n\n¿Te gustaría descargar la nueva versión?"
                if messagebox.askyesno("Actualización Disponible", msg):
                    # Abrir navegador en el repo
                    repo_url = f"https://github.com/{checker.owner}/{checker.repo}"
                    webbrowser.open(repo_url)
                    messagebox.showinfo("Descargar", "Ve a Releases y descarga el nuevo .exe")
            else:
                # No hay actualización
                if result['latest_version']:
                    msg = f"Ya tienes la última versión ({result['current_version']})"
                else:
                    msg = result['message']
                messagebox.showinfo("Actualizaciones", msg)

        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar actualizaciones: {str(e)}")

    def _refresh_all_tabs(self):
        """Auto-refresh all tabs when data changes."""
        self.inventory_tab.refresh()
        self.sales_tab.refresh()
        self.reports_tab.refresh()
        self._update_summary()  # Actualizar resumen también

    def _schedule_refresh(self):
        """Schedule refresh in the Tkinter event loop (thread-safe)."""
        self.root.after(50, self._refresh_all_tabs)

    def _update_summary(self):
        """Actualiza el panel de resumen."""
        try:
            products = self.data_manager.get_all_products()
            all_sales = self.data_manager.get_all_sales()

            # Ventas de HOY
            today = datetime.now().strftime('%Y-%m-%d')
            today_sales = [s for s in all_sales if s.date == today]

            ventas_hoy = sum(s.total for s in today_sales)
            capital_hoy = sum(s.quantity * s.purchase_price for s in today_sales)
            ganancia_hoy = ventas_hoy - capital_hoy

            # Inventario
            stock_total = sum(p.stock for p in products)
            invertido = sum(p.purchase_price * p.stock for p in products)
            valor_inv = sum(p.sale_price * p.stock for p in products)

            # Actualizar labels
            self.summary_labels['ventas_hoy'].config(text=f"${ventas_hoy:,.2f}")
            self.summary_labels['capital_hoy'].config(text=f"${capital_hoy:,.2f}")
            self.summary_labels['ganancia_hoy'].config(text=f"${ganancia_hoy:,.2f}", foreground='green' if ganancia_hoy >= 0 else 'red')
            self.summary_labels['stock_total'].config(text=f"{stock_total:,.0f}")
            self.summary_labels['invertido'].config(text=f"${invertido:,.2f}")
            self.summary_labels['valor_inv'].config(text=f"${valor_inv:,.2f}")

        except Exception as e:
            print(f"Error actualizando resumen: {e}")

    def _check_alerts(self):
        """Verifica alertas de stock bajo."""
        low_stock_products = self.inventory_service.get_low_stock_products()

        if low_stock_products:
            products_list = "\n".join([f"- {p.name} (Stock: {p.stock}/{p.min_stock})"
                                     for p in low_stock_products[:5]])
            message = f"Productos con stock bajo:\n\n{products_list}"

            if len(low_stock_products) > 5:
                message += f"\n\n... y {len(low_stock_products) - 5} mas"

            messagebox.showwarning("Alerta de Stock", message)

    def _exit(self):
        """Sale de la aplicación."""
        if messagebox.askokcancel("Salir", "Desea salir de la aplicacion?"):
            self.root.destroy()