import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta


class ReportsTab:
    """Tab de reportes y analisis."""

    def __init__(self, parent, reports_service, user_service=None):
        """Inicializa el tab de reportes."""
        self.frame = ttk.Frame(parent)
        self.reports_service = reports_service
        self.user_service = user_service

        # Almacenar referencias a los widgets para poder actualizarlos
        self._dashboard_data = {}
        self._dashboard_labels = []  # Labels del dashboard para actualizar
        self._inventory_labels = []  # Labels del inventario para actualizar
        self._sales_chart_main_frame = None
        self._last_update_time = None  # NEW: Tiempo de última actualización
        self._update_indicator = None  # NEW: Indicador visual de tiempo real
        self._auto_refresh_label = None  # NEW: Label de estado

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
        report_notebook.add(inventory_frame, text="Inventario")
        self._create_inventory_report(inventory_frame)

        # Tab de Ventas
        sales_frame = ttk.Frame(report_notebook)
        report_notebook.add(sales_frame, text="Ventas")
        self._create_sales_report(sales_frame)

        # Tab de Productos Populares
        products_frame = ttk.Frame(report_notebook)
        report_notebook.add(products_frame, text="Productos")
        self._create_products_report(products_frame)

        # Guardar referencia al notebook
        self.report_notebook = report_notebook

    def _create_dashboard(self, parent):
        """Crea el dashboard."""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # NEW: Indicador de tiempo real y botón de actualizar
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, pady=5, sticky=tk.EW)

        # Indicador visual de tiempo real
        self._update_indicator = ttk.Label(
            header_frame,
            text="● Tiempo Real",
            font=('Helvetica', 9, 'bold'),
            foreground='#27ae60'  # Verde
        )
        self._update_indicator.pack(side=tk.LEFT, padx=5)

        # NEW: Botón manual de actualizar
        refresh_btn = ttk.Button(
            header_frame,
            text="↻ Actualizar",
            command=self.refresh
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)

        # Label de última actualización
        self._auto_refresh_label = ttk.Label(
            header_frame,
            text="",
            font=('Helvetica', 8),
            foreground='#7f8c8d'
        )
        self._auto_refresh_label.pack(side=tk.LEFT, padx=10)

        # Obtener datos
        dashboard_data = self.reports_service.get_dashboard_data()
        self._dashboard_data = dashboard_data

        # Crear cards (actualizado v1.0.2 con ganancias)
        cards = [
            ("Ventas Hoy", f"{dashboard_data['today_sales_count']}", "T"),
            ("Ingresos Hoy", f"${dashboard_data['today_revenue']:.2f}", "$"),
            ("Ganancia Hoy", f"${dashboard_data.get('today_profit', 0):.2f}", "G"),
            ("Capital Invertido", f"${dashboard_data.get('total_capital_invested', 0):.2f}", "C"),
            ("Ganancia Total", f"${dashboard_data.get('total_profit', 0):.2f}", "P"),
            ("Productos", f"{dashboard_data['total_products']}", "#"),
        ]

        # Grid de cards (3 columnas ahora)
        for idx, (title, value, symbol) in enumerate(cards):
            row = idx // 3
            col = idx % 3

            card_frame = ttk.LabelFrame(main_frame, text=f"{symbol} {title}", padding=15)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky=tk.NSEW)

            value_label = ttk.Label(
                card_frame,
                text=value,
                font=('Helvetica', 14, 'bold'),
                foreground='#2c3e50'
            )
            value_label.pack(pady=20)
            self._dashboard_labels.append(value_label)

        # Productos mas vendidos
        products_frame = ttk.LabelFrame(main_frame, text="Productos Mas Vendidos", padding=10)
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

        # Guardar referencia al treeview del dashboard
        self._dashboard_tree = tree

        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky=tk.EW)

        ttk.Button(button_frame, text="Actualizar Dashboard", command=self.refresh).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Resetear Reportes", command=self._reset_reports).pack(side=tk.LEFT, padx=5)

    def _create_inventory_report(self, parent):
        """Crea reporte de inventario."""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Obtener datos
        inventory_report = self.reports_service.get_inventory_report()

        # Resumen (actualizado v1.0.2)
        summary_frame = ttk.LabelFrame(main_frame, text="Resumen de Inventario", padding=15)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        info = [
            f"Total de Productos: {inventory_report['total_products']}",
            f"Items en Stock: {inventory_report['total_items']}",
            f"Capital Invertido: ${inventory_report['total_capital']:.2f}",
            f"Valor del Inventario: ${inventory_report['total_value']:.2f}",
            f"Ganancia Potencial: ${inventory_report['potential_profit']:.2f}",
            f"Productos en Stock Bajo: {inventory_report['low_stock_count']}"
        ]

        self._inventory_labels = []
        for info_text in info:
            label = ttk.Label(summary_frame, text=info_text, font=('Helvetica', 10))
            label.pack(anchor=tk.W, pady=3)
            self._inventory_labels.append(label)

        # Tabla de productos
        table_frame = ttk.LabelFrame(main_frame, text="Detalles de Productos", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(
            table_frame,
            columns=('Nombre', 'Categoria', 'Stock', 'Minimo', 'Valor'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)

        tree.column('#0', width=0, stretch=tk.NO)
        tree.column('Nombre', anchor=tk.W, width=250)
        tree.column('Categoria', anchor=tk.W, width=120)
        tree.column('Stock', anchor=tk.CENTER, width=80)
        tree.column('Minimo', anchor=tk.CENTER, width=80)
        tree.column('Valor', anchor=tk.CENTER, width=100)

        tree.heading('#0', text='')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Categoria', text='Categoria')
        tree.heading('Stock', text='Stock')
        tree.heading('Minimo', text='Minimo')
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

        # Guardar referencia
        self._inventory_tree = tree

    def _create_sales_report(self, parent):
        """Crea reporte de ventas."""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        ttk.Label(control_frame, text="Mostrar ultimos:").pack(side=tk.LEFT, padx=5)

        self.period_var_sales = tk.StringVar(value="7_days")
        ttk.Radiobutton(control_frame, text="7 dias", variable=self.period_var_sales, value="7_days",
                       command=self._update_sales_chart).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="30 dias", variable=self.period_var_sales, value="30_days",
                       command=self._update_sales_chart).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="Todo", variable=self.period_var_sales, value="all",
                       command=self._update_sales_chart).pack(side=tk.LEFT, padx=5)

        # Resumen de ventas
        self.sales_summary_frame = ttk.LabelFrame(main_frame, text="Resumen de Ventas", padding=15)
        self.sales_summary_frame.pack(fill=tk.X, padx=10, pady=10)

        # Grafico de ventas
        self.chart_frame = ttk.LabelFrame(main_frame, text="Ventas", padding=10)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Guardar referencia para actualizacion
        self._sales_chart_main_frame = main_frame

        # Actualizar grafico inicial
        self._update_sales_chart()

    def _update_sales_chart(self):
        """Actualiza el grafico de ventas segun el periodo seleccionado."""
        # Limpiar frames previos
        for widget in self.sales_summary_frame.winfo_children():
            widget.destroy()
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        period = self.period_var_sales.get()

        # Obtener sales segun periodo
        if period == "7_days":
            daily_sales = self.reports_service.get_last_7_days_sales()
            self.chart_frame.config(text="Ventas Ultrimos 7 Dias")
        elif period == "30_days":
            daily_sales = self.reports_service.get_last_30_days_sales()
            self.chart_frame.config(text="Ventas Ultrimos 30 Dias")
        else:  # all
            daily_sales = self.reports_service.get_all_sales_by_date()
            self.chart_frame.config(text="Ventas Totales")

        # Resumen de ventas
        sales_summary = self.reports_service.get_sales_summary()

        info = [
            f"Total de Transacciones: {sales_summary['total_sales']}",
            f"Ingresos Totales: ${sales_summary['total_revenue']:.2f}",
            f"Promedio por Transaccion: ${sales_summary['average_per_sale']:.2f}"
        ]

        for info_text in info:
            ttk.Label(self.sales_summary_frame, text=info_text, font=('Helvetica', 10)).pack(anchor=tk.W, pady=3)

        # Crear grafico
        if daily_sales:
            max_revenue = max(daily_sales.values()) if daily_sales.values() else 1

            for date, revenue in daily_sales.items():
                bar_length = int((revenue / max_revenue) * 40) if max_revenue > 0 else 0
                bar = "#" * bar_length
                ttk.Label(self.chart_frame, text=f"{date}: {bar} ${revenue:.2f}", font=('Courier', 9)).pack(anchor=tk.W, pady=2)
        else:
            ttk.Label(self.chart_frame, text="No hay ventas en el periodo seleccionado", font=('Helvetica', 10)).pack(pady=20)

    def _create_products_report(self, parent):
        """Crea reporte de productos mas vendidos."""
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

        # Guardar referencia
        self._products_tree = tree

        # Boton de actualizar
        ttk.Button(main_frame, text="Actualizar", command=self.refresh).pack(pady=10)

    def refresh(self):
        """Actualiza todos los reportes."""
        # Forzar recarga de datos desde el archivo
        self.reports_service.data_manager._ensure_files_exist()

        # Forzar actualizacion de UI
        self.frame.update()  # Actualizar la UI inmediatamente

        # NEW: Actualizar indicador de tiempo real
        self._last_update_time = datetime.now()
        if self._update_indicator:
            self._update_indicator.config(text="● Actualizado", foreground='#27ae60')
        if self._auto_refresh_label:
            self._auto_refresh_label.config(
                text=f"Última actualización: {self._last_update_time.strftime('%H:%M:%S')}"
            )

        # Obtener nuevos datos del dashboard
        dashboard_data = self.reports_service.get_dashboard_data()
        self._dashboard_data = dashboard_data

        # Actualizar las etiquetas del dashboard (cards numericos - v1.0.2)
        # Forzar actualización
        if hasattr(self, '_dashboard_labels'):
            card_values = [
                str(dashboard_data['today_sales_count']),
                f"${dashboard_data['today_revenue']:.2f}",
                f"${dashboard_data.get('today_profit', 0):.2f}",
                f"${dashboard_data.get('total_capital_invested', 0):.2f}",
                f"${dashboard_data.get('total_profit', 0):.2f}",
                str(dashboard_data['total_products']),
            ]
            for idx, label in enumerate(self._dashboard_labels):
                label.config(text=card_values[idx])

        # Actualizar el treeview del dashboard si existe
        if hasattr(self, '_dashboard_tree'):
            # Limpiar treeview
            for item in self._dashboard_tree.get_children():
                self._dashboard_tree.delete(item)

            # Insertar nuevos datos
            for product in dashboard_data['top_products']:
                self._dashboard_tree.insert('', 'end', values=(
                    product['product_name'],
                    product['total_quantity'],
                    f"${product['total_revenue']:.2f}"
                ))

        # Actualizar reporte de inventario si existe (v1.0.2)
        if hasattr(self, '_inventory_labels') and self._inventory_labels:
            inventory_report = self.reports_service.get_inventory_report()
            inventory_values = [
                f"Total de Productos: {inventory_report['total_products']}",
                f"Items en Stock: {inventory_report['total_items']}",
                f"Capital Invertido: ${inventory_report['total_capital']:.2f}",
                f"Valor del Inventario: ${inventory_report['total_value']:.2f}",
                f"Ganancia Potencial: ${inventory_report['potential_profit']:.2f}",
                f"Productos en Stock Bajo: {inventory_report['low_stock_count']}"
            ]
            for idx, label in enumerate(self._inventory_labels):
                label.config(text=inventory_values[idx])

        # Actualizar treeview de inventario
        if hasattr(self, '_inventory_tree') and self._inventory_tree:
            inventory_report = self.reports_service.get_inventory_report()
            # Limpiar treeview
            for item in self._inventory_tree.get_children():
                self._inventory_tree.delete(item)
            # Insertar nuevos datos
            for product in inventory_report['products']:
                tag = 'low_stock' if product.stock < product.min_stock else ''
                self._inventory_tree.insert('', 'end', values=(
                    product.name,
                    product.category,
                    product.stock,
                    product.min_stock,
                    f"${product.stock * product.sale_price:.2f}"
                ), tags=(tag,))

        # Actualizar grafico de ventas
        self._update_sales_chart()

        # Actualizar reporte de productos
        if hasattr(self, '_products_tree') and self._products_tree:
            top_products = self.reports_service.get_top_products(15)
            # Limpiar treeview
            for item in self._products_tree.get_children():
                self._products_tree.delete(item)
            # Insertar nuevos datos
            for idx, product in enumerate(top_products, 1):
                avg = product['total_revenue'] / product['total_quantity'] if product['total_quantity'] > 0 else 0
                self._products_tree.insert('', 'end', values=(
                    f"#{idx}",
                    product['product_name'],
                    product['total_quantity'],
                    f"${product['total_revenue']:.2f}",
                    f"${avg:.2f}"
                ))

    def _reset_reports(self):
        """Resetea todos los reportes despues de validar las credenciales del usuario."""
        if not self.user_service:
            messagebox.showerror("Error", "Servicio de usuarios no disponible")
            return

        # Solicitar usuario
        username = simpledialog.askstring("Resetear Reportes", "Usuario:")
        if not username:
            return

        # Solicitar contrasena
        password = simpledialog.askstring("Resetear Reportes", "Contrasena:", show='*')
        if not password:
            return

        # Validar credenciales
        user = self.user_service.get_user(username)
        if not user:
            messagebox.showerror("Error", "Usuario no encontrado")
            return

        # Verificar contrasena
        if not self.user_service.security.verify_password(password, user.password_hash):
            messagebox.showerror("Error", "Contrasena incorrecta")
            return

        # Solicitar confirmacion
        confirm = messagebox.askyesno("Confirmacion", "Se borraran todos los registros de ventas. Continuar?")
        if not confirm:
            return

        # Resetear reportes
        if self.reports_service.reset_all_sales():
            messagebox.showinfo("Exito", "Todos los reportes han sido reseteados")
            self.refresh()
        else:
            messagebox.showerror("Error", "Error al resetear reportes")