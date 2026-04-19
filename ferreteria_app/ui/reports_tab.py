import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


class ReportsTab:
    """Tab de reportes y análisis."""
    
    def __init__(self, parent, reports_service):
        """Inicializa el tab de reportes."""
        self.frame = ttk.Frame(parent)
        self.reports_service = reports_service
        
        self._create_ui()
        self.refresh()
    
    def _create_ui(self):
        """Crea la interfaz del tab."""
        # Notebook interno para diferentes reportes
        report_notebook = ttk.Notebook(self.frame)
        report_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab de Dashboard
        dashboard_frame = ttk.Frame(report_notebook)
        report_notebook.add(dashboard_frame, text="Dashboard")
        self._create_dashboard(dashboard_frame)
        
        # Tab de Inventario
        inventory_frame = ttk.Frame(report_notebook)
        report_notebook.add(inventory_frame, text="📦 Inventario")
        self._create_inventory_report(inventory_frame)
        
        # Tab de Ventas
        sales_frame = ttk.Frame(report_notebook)
        report_notebook.add(sales_frame, text="💰 Ventas")
        self._create_sales_report(sales_frame)
        
        # Tab de Productos Populares
        products_frame = ttk.Frame(report_notebook)
        report_notebook.add(products_frame, text="⭐ Productos")
        self._create_products_report(products_frame)
    
    def _create_dashboard(self, parent):
        """Crea el dashboard."""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Obtener datos
        dashboard_data = self.reports_service.get_dashboard_data()
        
        # Crear cards
        cards = [
            ("Ventas Hoy", f"{dashboard_data['today_sales_count']}", "🛒"),
            ("Ingresos Hoy", f"${dashboard_data['today_revenue']:.2f}", "💵"),
            ("Total Ventas", f"{dashboard_data['total_sales']}", "📊"),
            ("Ingresos Totales", f"${dashboard_data['total_revenue']:.2f}", "💰"),
            ("Productos", f"{dashboard_data['total_products']}", "📦"),
            ("Stock Bajo", f"{dashboard_data['low_stock_count']}", "⚠️"),
        ]
        
        # Grid de cards
        for idx, (title, value, emoji) in enumerate(cards):
            row = idx // 3
            col = idx % 3
            
            card_frame = ttk.LabelFrame(main_frame, text=f"{emoji} {title}", padding=15)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky=tk.NSEW)
            
            value_label = ttk.Label(
                card_frame,
                text=value,
                font=('Helvetica', 16, 'bold'),
                foreground='#2c3e50'
            )
            value_label.pack(pady=20)
        
        # Productos más vendidos
        products_frame = ttk.LabelFrame(main_frame, text="⭐ Productos Más Vendidos", padding=10)
        products_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)
        
        # Treeview para productos
        scrollbar = ttk.Scrollbar(products_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            products_frame,
            columns=('Producto', 'Cantidad', 'Ingresos'),
            height=5,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)
        
        tree.column('#0', width=0, stretch=tk.NO)
        tree.column('Producto', anchor=tk.W, width=300)
        tree.column('Cantidad', anchor=tk.CENTER, width=100)
        tree.column('Ingresos', anchor=tk.CENTER, width=100)
        
        tree.heading('#0', text='')
        tree.heading('Producto', text='Producto')
        tree.heading('Cantidad', text='Cantidad Vendida')
        tree.heading('Ingresos', text='Ingresos')
        
        for product in dashboard_data['top_products']:
            tree.insert('', 'end', values=(
                product['product_name'],
                product['total_quantity'],
                f"${product['total_revenue']:.2f}"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Botón de actualizar
        ttk.Button(main_frame, text="🔄 Actualizar Dashboard", command=self.refresh).grid(row=3, column=0, columnspan=3, pady=10)
    
    def _create_inventory_report(self, parent):
        """Crea reporte de inventario."""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Obtener datos
        inventory_report = self.reports_service.get_inventory_report()
        
        # Resumen
        summary_frame = ttk.LabelFrame(main_frame, text="Resumen de Inventario", padding=15)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info = [
            f"Total de Productos: {inventory_report['total_products']}",
            f"Items en Stock: {inventory_report['total_items']}",
            f"Valor Total del Inventario: ${inventory_report['total_value']:.2f}",
            f"Productos en Stock Bajo: {inventory_report['low_stock_count']}"
        ]
        
        for info_text in info:
            ttk.Label(summary_frame, text=info_text, font=('Helvetica', 10)).pack(anchor=tk.W, pady=3)
        
        # Tabla de productos
        table_frame = ttk.LabelFrame(main_frame, text="Detalles de Productos", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            table_frame,
            columns=('Nombre', 'Categoría', 'Stock', 'Mínimo', 'Valor'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)
        
        tree.column('#0', width=0, stretch=tk.NO)
        tree.column('Nombre', anchor=tk.W, width=250)
        tree.column('Categoría', anchor=tk.W, width=120)
        tree.column('Stock', anchor=tk.CENTER, width=80)
        tree.column('Mínimo', anchor=tk.CENTER, width=80)
        tree.column('Valor', anchor=tk.CENTER, width=100)
        
        tree.heading('#0', text='')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Categoría', text='Categoría')
        tree.heading('Stock', text='Stock')
        tree.heading('Mínimo', text='Mínimo')
        tree.heading('Valor', text='Valor')
        
        for product in inventory_report['products']:
            tag = 'low_stock' if product.stock < product.min_stock else ''
            tree.insert('', 'end', values=(
                product.name,
                product.category,
                product.stock,
                product.min_stock,
                f"${product.stock * product.sale_price:.2f}"
            ), tags=(tag,))
        
        tree.tag_configure('low_stock', foreground='red')
        tree.pack(fill=tk.BOTH, expand=True)
    
    def _create_sales_report(self, parent):
        """Crea reporte de ventas."""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Mostrar últimos:").pack(side=tk.LEFT, padx=5)
        
        self.period_var_sales = tk.StringVar(value="7_days")
        ttk.Radiobutton(control_frame, text="7 días", variable=self.period_var_sales, value="7_days", 
                       command=lambda: self._update_sales_chart(main_frame)).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="30 días", variable=self.period_var_sales, value="30_days",
                       command=lambda: self._update_sales_chart(main_frame)).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="Todo", variable=self.period_var_sales, value="all",
                       command=lambda: self._update_sales_chart(main_frame)).pack(side=tk.LEFT, padx=5)
        
        # Resumen de ventas
        self.sales_summary_frame = ttk.LabelFrame(main_frame, text="Resumen de Ventas", padding=15)
        self.sales_summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Gráfico de ventas
        self.chart_frame = ttk.LabelFrame(main_frame, text="Ventas", padding=10)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Actualizar gráfico inicial
        self._update_sales_chart(main_frame)
    
    def _update_sales_chart(self, parent):
        """Actualiza el gráfico de ventas según el período seleccionado."""
        # Limpiar frames previos
        for widget in self.sales_summary_frame.winfo_children():
            widget.destroy()
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        period = self.period_var_sales.get()
        
        # Obtener sales según período
        if period == "7_days":
            daily_sales = self.reports_service.get_last_7_days_sales()
            self.chart_frame.config(text="Ventas Últimos 7 Días")
        elif period == "30_days":
            daily_sales = self.reports_service.get_last_30_days_sales()
            self.chart_frame.config(text="Ventas Últimos 30 Días")
        else:  # all
            daily_sales = self.reports_service.get_all_sales_by_date()
            self.chart_frame.config(text="Ventas Totales")
        
        # Resumen de ventas
        sales_summary = self.reports_service.get_sales_summary()
        
        info = [
            f"Total de Transacciones: {sales_summary['total_sales']}",
            f"Ingresos Totales: ${sales_summary['total_revenue']:.2f}",
            f"Promedio por Transacción: ${sales_summary['average_per_sale']:.2f}"
        ]
        
        for info_text in info:
            ttk.Label(self.sales_summary_frame, text=info_text, font=('Helvetica', 10)).pack(anchor=tk.W, pady=3)
        
        # Crear gráfico
        max_revenue = max(daily_sales.values()) if daily_sales.values() else 1
        
        for date, revenue in daily_sales.items():
            bar_length = int((revenue / max_revenue) * 40) if max_revenue > 0 else 0
            bar = "█" * bar_length
            ttk.Label(self.chart_frame, text=f"{date}: {bar} ${revenue:.2f}", font=('Courier', 9)).pack(anchor=tk.W, pady=2)
    
    def _create_products_report(self, parent):
        """Crea reporte de productos más vendidos."""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tabla de productos
        scrollbar = ttk.Scrollbar(main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            main_frame,
            columns=('Ranking', 'Producto', 'Cantidad', 'Ingresos', 'Promedio'),
            height=20,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)
        
        tree.column('#0', width=0, stretch=tk.NO)
        tree.column('Ranking', anchor=tk.CENTER, width=80)
        tree.column('Producto', anchor=tk.W, width=250)
        tree.column('Cantidad', anchor=tk.CENTER, width=100)
        tree.column('Ingresos', anchor=tk.CENTER, width=120)
        tree.column('Promedio', anchor=tk.CENTER, width=100)
        
        tree.heading('#0', text='')
        tree.heading('Ranking', text='Ranking')
        tree.heading('Producto', text='Producto')
        tree.heading('Cantidad', text='Cantidad Vendida')
        tree.heading('Ingresos', text='Ingresos Totales')
        tree.heading('Promedio', text='Promedio por Venta')
        
        top_products = self.reports_service.get_top_products(15)
        
        for idx, product in enumerate(top_products, 1):
            avg = product['total_revenue'] / product['total_quantity'] if product['total_quantity'] > 0 else 0
            tree.insert('', 'end', values=(
                f"#{idx}",
                product['product_name'],
                product['total_quantity'],
                f"${product['total_revenue']:.2f}",
                f"${avg:.2f}"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Botón de actualizar
        ttk.Button(main_frame, text="🔄 Actualizar", command=self.refresh).pack(pady=10)
    
    def refresh(self):
        """Actualiza todos los reportes."""
        # Data refreshed via service calls - no action needed
        pass
