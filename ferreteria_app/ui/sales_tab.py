import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class SalesTab:
    """Tab de gestión de ventas."""
    
    def __init__(self, parent, sales_service, inventory_service):
        """Inicializa el tab de ventas."""
        self.frame = ttk.Frame(parent)
        self.sales_service = sales_service
        self.inventory_service = inventory_service
        self.selected_sale = None
        self.current_product = None
        
        self._create_ui()
        self.refresh()
    
    def _create_ui(self):
        """Crea la interfaz del tab."""
        # Frame de registro de venta
        register_frame = ttk.LabelFrame(self.frame, text="Registrar Nueva Venta", padding=10)
        register_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Seleccionar producto
        ttk.Label(register_frame, text="Producto:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(register_frame, textvariable=self.product_var, width=40)
        self.product_combo.grid(row=0, column=1, padx=5, pady=5)
        self.product_combo.bind('<<ComboboxSelected>>', self._on_product_selected)
        self._update_product_list()
        
        # Boton de actualizar productos
        ttk.Button(register_frame, text="Buscar Nuevos", command=self._refresh_products).grid(row=0, column=2, padx=5, pady=5)
        
        # Cantidad
        ttk.Label(register_frame, text="Cantidad:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        # Ahora permite decimales
        quantity_spin = ttk.Spinbox(register_frame, from_=0.1, to=10000, increment=0.1,
                                   textvariable=self.quantity_var, width=43)
        quantity_spin.grid(row=1, column=1, padx=5, pady=5)

        # Tipo de venta (Unidad/Kilo)
        ttk.Label(register_frame, text="Tipo:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.type_var = tk.StringVar(value="UNIDAD")
        type_combo = ttk.Combobox(register_frame, textvariable=self.type_var,
                                values=["UNIDAD", "KILO", "METRO", "LITRO"],
                                width=41)
        type_combo.grid(row=2, column=1, padx=5, pady=5)
        type_combo.bind('<<ComboboxSelected>>', self._on_type_selected)
        
        # Precio unitario (mostrado automáticamente)
        ttk.Label(register_frame, text="Precio Unitario:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.price_label = ttk.Label(register_frame, text="$0.00", font=('Helvetica', 10, 'bold'))
        self.price_label.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Total (calculado automáticamente)
        ttk.Label(register_frame, text="Total:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.total_label = ttk.Label(register_frame, text="$0.00", font=('Helvetica', 10, 'bold'), foreground='green')
        self.total_label.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # Botones
        button_frame = ttk.Frame(register_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.E)
        
        ttk.Button(button_frame, text="✓ Confirmar Venta", command=self._register_sale).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="↻ Limpiar", command=self._clear_form).pack(side=tk.LEFT, padx=5)
        
        # Bind para cálculo automático
        self.quantity_var.trace('w', self._calculate_total)
        
        # Frame de historial de ventas
        history_frame = ttk.LabelFrame(self.frame, text="Historial de Ventas", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Controles de filtrado
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar por fecha:").pack(side=tk.LEFT, padx=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(filter_frame, textvariable=self.date_var, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Aplicar Filtro", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            history_frame,
            columns=('Producto', 'Cantidad', 'Precio Unit.', 'Total', 'Fecha', 'Hora'),
            height=10,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Producto', anchor=tk.W, width=200)
        self.tree.column('Cantidad', anchor=tk.CENTER, width=80)
        self.tree.column('Precio Unit.', anchor=tk.CENTER, width=120)
        self.tree.column('Total', anchor=tk.CENTER, width=120)
        self.tree.column('Fecha', anchor=tk.CENTER, width=100)
        self.tree.column('Hora', anchor=tk.CENTER, width=80)
        
        # Encabezados
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('Producto', text='Producto', anchor=tk.W)
        self.tree.heading('Cantidad', text='Cantidad', anchor=tk.CENTER)
        self.tree.heading('Precio Unit.', text='Precio Unit.', anchor=tk.CENTER)
        self.tree.heading('Total', text='Total', anchor=tk.CENTER)
        self.tree.heading('Fecha', text='Fecha', anchor=tk.CENTER)
        self.tree.heading('Hora', text='Hora', anchor=tk.CENTER)
        
        self.tree.bind('<ButtonRelease-1>', self._on_select)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Info frame
        info_frame = ttk.Frame(self.frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="")
        self.info_label.pack(side=tk.LEFT)
    
    def _update_product_list(self):
        """Actualiza la lista de productos en el combobox."""
        products = self.inventory_service.get_all_products()
        product_list = [f"{p.name} ({p.code})" for p in products if p.stock > 0]
        self.product_combo['values'] = product_list
    
    def _refresh_products(self):
        """Actualiza la lista de productos desde el inventario."""
        self._update_product_list()
        messagebox.showinfo("Actualizar", "Lista de productos actualizada")
    
    def _on_product_selected(self, event=None):
        """Evento cuando se selecciona un producto."""
        selection = self.product_var.get()
        if selection:
            # Extraer código del producto seleccionado
            code = selection.split('(')[-1].rstrip(')')
            product = self.inventory_service.data_manager.get_product_by_code(code)

            if product:
                self.price_label.config(text=f"${product.sale_price:.2f}")
                self.current_product = product
                # Actualizar tipo según la unidad del producto
                self.type_var.set(product.unidad)
                self._calculate_total()

    def _on_type_selected(self, event=None):
        """Evento cuando se cambia el tipo de venta."""
        self._calculate_total()

    def _calculate_total(self, *args):
        """Calcula el total automáticamente."""
        try:
            quantity = float(self.quantity_var.get() or 0)
            price_text = self.price_label.cget('text').replace('$', '')
            price = float(price_text or 0)

            # Ajustar precio si es por kilo (mostrar precio por kilo)
            venta_tipo = self.type_var.get()

            total = quantity * price
            self.total_label.config(text=f"${total:.2f}")
        except:
            pass
    
    def _calculate_total(self, *args):
        """Calcula el total automáticamente."""
        try:
            quantity = int(self.quantity_var.get() or 0)
            price_text = self.price_label.cget('text').replace('$', '')
            price = float(price_text or 0)
            total = quantity * price
            self.total_label.config(text=f"${total:.2f}")
        except:
            pass
    
    def _register_sale(self):
        """Registra una venta."""
        product_selection = self.product_var.get()
        quantity_str = self.quantity_var.get()

        if not product_selection:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        if not quantity_str or float(quantity_str) <= 0:
            messagebox.showwarning("Advertencia", "Ingrese una cantidad válida")
            return

        try:
            # Obtener el producto
            code = product_selection.split('(')[-1].rstrip(')')
            product = self.inventory_service.data_manager.get_product_by_code(code)

            if not product:
                messagebox.showerror("Error", "Producto no encontrado")
                return

            quantity = float(quantity_str)

            if quantity > float(product.stock):
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {product.stock}")
                return

            # Obtener tipo de venta
            venta_tipo = self.type_var.get()

            # Registrar venta (ahora acepta float y pasa la unidad)
            success, message = self.sales_service.register_sale(
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.sale_price,
                unidad=venta_tipo
            )

            if success:
                messagebox.showinfo("Éxito", message)
                self._clear_form()
                self.refresh()
                self._update_product_list()
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número")
    
    def _clear_form(self):
        """Limpia el formulario."""
        self.product_var.set('')
        self.quantity_var.set('1')
        self.type_var.set('UNIDAD')
        self.price_label.config(text='$0.00')
        self.total_label.config(text='$0.00')
    
    def _on_select(self, event):
        """Evento de selección en la tabla."""
        selection = self.tree.selection()
        if selection:
            self.selected_sale = selection[0]
    
    def refresh(self):
        """Actualiza el historial de ventas."""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener ventas del día seleccionado
        date_str = self.date_var.get()
        sales = self.sales_service.get_sales_by_date(date_str)
        
        total_revenue = 0
        
        # Añadir ventas a la tabla
        for sale in sales:
            self.tree.insert('', 'end', iid=sale.id, values=(
                sale.product_name,
                sale.quantity,
                f"${sale.unit_price:.2f}",
                f"${sale.total:.2f}",
                sale.date,
                sale.time
            ))
            total_revenue += sale.total
        
        # Actualizar info
        self.info_label.config(text=f"Ventas del día: {len(sales)} | Ingresos: ${total_revenue:.2f}")
