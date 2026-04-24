import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from config.settings import PRODUCT_CATEGORIES
from data.models import Product
from utils.validators import Validators
import os


class InventoryTab:
    """Tab de gestión de inventario."""
    
    def __init__(self, parent, inventory_service, sales_service):
        """Inicializa el tab de inventario."""
        self.frame = ttk.Frame(parent)
        self.inventory_service = inventory_service
        self.sales_service = sales_service
        self.validators = Validators()
        self.selected_product = None
        self.parent_window = parent  # Guardar referencia

        self._create_ui()
        self.refresh()
    
    def _create_ui(self):
        """Crea la interfaz del tab."""
        # Frame de búsqueda y botones
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Búsqueda
        ttk.Label(control_frame, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Botones
        ttk.Button(control_frame, text="Nuevo", command=self._add_product).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Editar", command=self._edit_product).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Eliminar", command=self._delete_product).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Actualizar", command=self.refresh).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Importar", command=self._import_products).pack(side=tk.LEFT, padx=2)
        
        # Tabla de productos
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('Código', 'Nombre', 'Categoría', 'Marca', 'Unidad', 'P. Compra', 'P. Venta', 'Stock', 'Stock Min.', 'Flexible'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Configurar columnas
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Código', anchor=tk.CENTER, width=80)
        self.tree.column('Nombre', anchor=tk.W, width=180)
        self.tree.column('Categoría', anchor=tk.W, width=100)
        self.tree.column('Marca', anchor=tk.W, width=100)
        self.tree.column('Unidad', anchor=tk.CENTER, width=80)
        self.tree.column('P. Compra', anchor=tk.CENTER, width=90)
        self.tree.column('P. Venta', anchor=tk.CENTER, width=90)
        self.tree.column('Stock', anchor=tk.CENTER, width=70)
        self.tree.column('Stock Min.', anchor=tk.CENTER, width=70)
        self.tree.column('Flexible', anchor=tk.CENTER, width=70)

        # Encabezados
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('Código', text='Código', anchor=tk.CENTER)
        self.tree.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tree.heading('Categoría', text='Categoría', anchor=tk.W)
        self.tree.heading('Marca', text='Marca', anchor=tk.W)
        self.tree.heading('Unidad', text='Unidad', anchor=tk.CENTER)
        self.tree.heading('P. Compra', text='P. Compra', anchor=tk.CENTER)
        self.tree.heading('P. Venta', text='P. Venta', anchor=tk.CENTER)
        self.tree.heading('Stock', text='Stock', anchor=tk.CENTER)
        self.tree.heading('Stock Min.', text='Stock Min.', anchor=tk.CENTER)
        self.tree.heading('Flexible', text='Flexible', anchor=tk.CENTER)
        
        # Bind selección
        self.tree.bind('<ButtonRelease-1>', self._on_select)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Info frame
        info_frame = ttk.Frame(self.frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="")
        self.info_label.pack(side=tk.LEFT)
    
    def _on_search_change(self, *args):
        """Evento de cambio en la búsqueda."""
        self.refresh()
    
    def _on_select(self, event):
        """Evento de selección en la tabla."""
        selection = self.tree.selection()
        if selection:
            self.selected_product = selection[0]
    
    def refresh(self):
        """Actualiza la tabla de productos."""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener productos
        search_query = self.search_var.get().strip()
        if search_query:
            products = self.inventory_service.search_products(search_query)
        else:
            products = self.inventory_service.get_all_products()
        
        # Añadir productos a la tabla
        for product in products:
            # Color diferente si stock es bajo
            tag = 'low_stock' if product.stock < product.min_stock else ''
            flexible = "SI" if product.flexible_stock else "NO"

            self.tree.insert('', 'end', iid=product.id, values=(
                product.code,
                product.name,
                product.category,
                product.marca,
                product.unidad,
                f"${product.purchase_price:.2f}",
                f"${product.sale_price:.2f}",
                product.stock,
                product.min_stock,
                flexible
            ), tags=(tag,))
        
        # Configurar estilos de tags
        self.tree.tag_configure('low_stock', foreground='red')
        
        # Actualizar info
        total_products = len(products)
        self.info_label.config(text=f"Total de productos: {total_products}")
    
    def _add_product(self):
        """Añade un nuevo producto."""
        window = tk.Toplevel(self.frame)
        window.title("Nuevo Producto")
        window.geometry("550x750")

        # Frame principal
        main_frame = ttk.Frame(window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Campos
        fields = {}

        # Nombre
        ttk.Label(main_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=name_var, width=40).grid(row=0, column=1, pady=5)
        fields['name'] = name_var

        # Categoría
        ttk.Label(main_frame, text="Categoría:").grid(row=1, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(main_frame, textvariable=category_var, values=PRODUCT_CATEGORIES, width=37)
        category_combo.grid(row=1, column=1, pady=5)
        fields['category'] = category_var

        # Código
        ttk.Label(main_frame, text="Código:").grid(row=2, column=0, sticky=tk.W, pady=5)
        code_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=code_var, width=40).grid(row=2, column=1, pady=5)
        fields['code'] = code_var

        # Proveedor
        ttk.Label(main_frame, text="Proveedor:").grid(row=3, column=0, sticky=tk.W, pady=5)
        provider_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=provider_var, width=40).grid(row=3, column=1, pady=5)
        fields['provider'] = provider_var

        # Marca (nuevo v1.0.2)
        ttk.Label(main_frame, text="Marca:").grid(row=4, column=0, sticky=tk.W, pady=5)
        marca_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=marca_var, width=40).grid(row=4, column=1, pady=5)
        fields['marca'] = marca_var

        # Unidad
        ttk.Label(main_frame, text="Unidad:").grid(row=5, column=0, sticky=tk.W, pady=5)
        unidad_var = tk.StringVar(value="UNIDAD")
        unidad_combo = ttk.Combobox(main_frame, textvariable=unidad_var,
                                    values=["UNIDAD", "KILO", "METRO", "LITRO", "GALON", "BOLSA", "CAJA"],
                                    width=37)
        unidad_combo.grid(row=5, column=1, pady=5)
        fields['unidad'] = unidad_var

        # Stock Flexible
        ttk.Label(main_frame, text="Stock Flexible:").grid(row=6, column=0, sticky=tk.W, pady=5)
        flexible_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Permitir decimales (por kilo)",
                     variable=flexible_var).grid(row=6, column=1, sticky=tk.W, pady=5)
        fields['flexible_stock'] = flexible_var

        # Precio de compra
        ttk.Label(main_frame, text="Precio Compra:").grid(row=7, column=0, sticky=tk.W, pady=5)
        purchase_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=purchase_var, width=40).grid(row=7, column=1, pady=5)
        fields['purchase_price'] = purchase_var

        # Precio de venta
        ttk.Label(main_frame, text="Precio Venta:").grid(row=8, column=0, sticky=tk.W, pady=5)
        sale_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=sale_var, width=40).grid(row=8, column=1, pady=5)
        fields['sale_price'] = sale_var

        # Stock
        ttk.Label(main_frame, text="Stock:").grid(row=9, column=0, sticky=tk.W, pady=5)
        stock_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=stock_var, width=40).grid(row=9, column=1, pady=5)
        fields['stock'] = stock_var

        # Stock mínimo
        ttk.Label(main_frame, text="Stock Mínimo:").grid(row=10, column=0, sticky=tk.W, pady=5)
        min_stock_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=min_stock_var, width=40).grid(row=10, column=1, pady=5)
        fields['min_stock'] = min_stock_var

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=11, column=0, columnspan=2, pady=20, sticky=tk.E)

        def save():
            try:
                success, msg = self.inventory_service.create_product(
                    name=name_var.get(),
                    category=category_var.get(),
                    code=code_var.get(),
                    provider=provider_var.get(),
                    purchase_price=float(purchase_var.get()),
                    sale_price=float(sale_var.get()),
                    stock=float(stock_var.get()),
                    min_stock=float(min_stock_var.get()),
                    marca=marca_var.get(),
                    unidad=unidad_var.get(),
                    flexible_stock=flexible_var.get()
                )

                if success:
                    messagebox.showinfo("Éxito", msg)
                    self.refresh()
                    window.destroy()
                else:
                    messagebox.showerror("Error", msg)
            except ValueError:
                messagebox.showerror("Error", "Precios y cantidades deben ser números")

        ttk.Button(button_frame, text="Guardar", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _edit_product(self):
        """Edita un producto seleccionado."""
        if not self.selected_product:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        product = self.inventory_service.get_product(self.selected_product)
        if not product:
            return

        window = tk.Toplevel(self.frame)
        window.title("Editar Producto")
        window.geometry("550x750")

        # Frame principal
        main_frame = ttk.Frame(window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Campos (pre-llenar con datos existentes)
        # Nombre
        ttk.Label(main_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=product.name)
        ttk.Entry(main_frame, textvariable=name_var, width=40).grid(row=0, column=1, pady=5)

        # Categoría
        ttk.Label(main_frame, text="Categoría:").grid(row=1, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar(value=product.category)
        ttk.Combobox(main_frame, textvariable=category_var, values=PRODUCT_CATEGORIES, width=37).grid(row=1, column=1, pady=5)

        # Código
        ttk.Label(main_frame, text="Código:").grid(row=2, column=0, sticky=tk.W, pady=5)
        code_var = tk.StringVar(value=product.code)
        ttk.Entry(main_frame, textvariable=code_var, width=40).grid(row=2, column=1, pady=5)

        # Proveedor
        ttk.Label(main_frame, text="Proveedor:").grid(row=3, column=0, sticky=tk.W, pady=5)
        provider_var = tk.StringVar(value=product.provider)
        ttk.Entry(main_frame, textvariable=provider_var, width=40).grid(row=3, column=1, pady=5)

        # Marca (nuevo)
        ttk.Label(main_frame, text="Marca:").grid(row=4, column=0, sticky=tk.W, pady=5)
        marca_var = tk.StringVar(value=product.marca)
        ttk.Entry(main_frame, textvariable=marca_var, width=40).grid(row=4, column=1, pady=5)

        # Unidad
        ttk.Label(main_frame, text="Unidad:").grid(row=5, column=0, sticky=tk.W, pady=5)
        unidad_var = tk.StringVar(value=product.unidad)
        ttk.Combobox(main_frame, textvariable=unidad_var,
                   values=["UNIDAD", "KILO", "METRO", "LITRO", "GALON", "BOLSA", "CAJA"],
                   width=37).grid(row=5, column=1, pady=5)

        # Stock Flexible
        ttk.Label(main_frame, text="Stock Flexible:").grid(row=6, column=0, sticky=tk.W, pady=5)
        flexible_var = tk.BooleanVar(value=product.flexible_stock)
        ttk.Checkbutton(main_frame, text="Permitir decimales", variable=flexible_var).grid(row=6, column=1, sticky=tk.W, pady=5)

        # Precio de compra
        ttk.Label(main_frame, text="Precio Compra:").grid(row=7, column=0, sticky=tk.W, pady=5)
        purchase_var = tk.StringVar(value=str(product.purchase_price))
        ttk.Entry(main_frame, textvariable=purchase_var, width=40).grid(row=7, column=1, pady=5)

        # Precio de venta
        ttk.Label(main_frame, text="Precio Venta:").grid(row=8, column=0, sticky=tk.W, pady=5)
        sale_var = tk.StringVar(value=str(product.sale_price))
        ttk.Entry(main_frame, textvariable=sale_var, width=40).grid(row=8, column=1, pady=5)

        # Stock
        ttk.Label(main_frame, text="Stock:").grid(row=9, column=0, sticky=tk.W, pady=5)
        stock_var = tk.StringVar(value=str(product.stock))
        ttk.Entry(main_frame, textvariable=stock_var, width=40).grid(row=9, column=1, pady=5)

        # Stock mínimo
        ttk.Label(main_frame, text="Stock Mínimo:").grid(row=10, column=0, sticky=tk.W, pady=5)
        min_stock_var = tk.StringVar(value=str(product.min_stock))
        ttk.Entry(main_frame, textvariable=min_stock_var, width=40).grid(row=10, column=1, pady=5)

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=11, column=0, columnspan=2, pady=20, sticky=tk.E)

        def save():
            try:
                success, msg = self.inventory_service.update_product(
                    product_id=product.id,
                    name=name_var.get(),
                    category=category_var.get(),
                    code=code_var.get(),
                    provider=provider_var.get(),
                    purchase_price=float(purchase_var.get()),
                    sale_price=float(sale_var.get()),
                    stock=float(stock_var.get()),
                    min_stock=float(min_stock_var.get()),
                    marca=marca_var.get(),
                    unidad=unidad_var.get(),
                    flexible_stock=flexible_var.get()
                )

                if success:
                    messagebox.showinfo("Éxito", msg)
                    self.refresh()
                    window.destroy()
                else:
                    messagebox.showerror("Error", msg)
            except ValueError:
                messagebox.showerror("Error", "Precios y cantidades deben ser números")

        ttk.Button(button_frame, text="Guardar", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _delete_product(self):
        """Elimina el producto seleccionado."""
        if not self.selected_product:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            success, msg = self.inventory_service.delete_product(self.selected_product)
            if success:
                messagebox.showinfo("Éxito", msg)
                self.refresh()
            else:
                messagebox.showerror("Error", msg)

    def _import_products(self):
        """Importa productos desde un archivo CSV o Excel."""
        # Seleccionar archivo
        file_path = filedialog.askopenfilename(
            title="Importar Productos",
            filetypes=[
                ("Archivos CSV", "*.csv"),
                ("Archivos Excel", "*.xlsx"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not file_path:
            return

        # Determinar tipo de archivo
        ext = os.path.splitext(file_path)[1].lower()

        try:
            # Importar según tipo
            if ext == '.csv':
                from utils.product_importer import ProductImporter
                importer = ProductImporter()
                success, msg, products_data = importer.import_from_csv(file_path)
            elif ext in ['.xlsx', '.xls']:
                from utils.product_importer import ProductImporter
                importer = ProductImporter()
                success, msg, products_data = importer.import_from_excel(file_path)
            else:
                messagebox.showerror("Error", "Formato no soportado")
                return

            if not success:
                messagebox.showerror("Error", msg)
                return

            if not products_data:
                messagebox.showwarning("Advertencia", "No se encontraron productos para importar")
                return

            # Confirmar importación
            count = len(products_data)
            if not messagebox.askyesno("Confirmar",
                f"Se importarán {count} productos.\n\n¿Desea continuar?"):
                return

            # Importar cada producto
            imported = 0
            skipped = 0

            for prod_data in products_data:
                # Verificar si ya existe
                existing = self.inventory_service.data_manager.get_product_by_code(prod_data['code'])
                if existing:
                    skipped += 1
                    continue

                # Crear producto
                success2, msg2 = self.inventory_service.create_product(
                    name=prod_data['name'],
                    category=prod_data.get('category', 'Otros'),
                    code=prod_data['code'],
                    provider=prod_data.get('provider', 'Proveedor'),
                    purchase_price=prod_data.get('purchase_price', 0),
                    sale_price=prod_data.get('sale_price', 0),
                    stock=prod_data.get('stock', 0),
                    min_stock=prod_data.get('min_stock', 0),
                    marca=prod_data.get('marca', ''),
                    unidad=prod_data.get('unidad', 'UNIDAD'),
                    flexible_stock=prod_data.get('flexible_stock', False),
                    equivalente_sunat=prod_data.get('equivalente_sunat', ''),
                    tipo_igv=prod_data.get('tipo_igv', '')
                )

                if success2:
                    imported += 1
                else:
                    skipped += 1

            # Mostrar resultado
            self.refresh()

            # Forzar actualización del resumenglobal
            self.frame.update_idletasks()

            messagebox.showinfo("Importar",
                f"Importación completada:\n"
                f"- Importados: {imported}\n"
                f"- Omitidos (ya existen): {skipped}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al importar: {str(e)}")
