from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, PieChart, Reference
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class ExcelExporter:
    """Exportador de datos a archivos Excel."""
    
    # Estilos
    HEADER_FILL = PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")
    HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
    BORDER = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    def __init__(self, output_path: str = None):
        """Inicializa el exportador."""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"Reporte_Ferreteria_{timestamp}.xlsx"
        self.output_path = output_path
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
    
    def _style_header(self, cell):
        """Aplica estilos a una celda de encabezado."""
        cell.fill = self.HEADER_FILL
        cell.font = self.HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = self.BORDER
    
    def _style_cell(self, cell, alignment="left"):
        """Aplica estilos a una celda de datos."""
        cell.border = self.BORDER
        if alignment == "center":
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif alignment == "right":
            cell.alignment = Alignment(horizontal="right", vertical="center")
        else:
            cell.alignment = Alignment(horizontal=alignment, vertical="center")
    
    def add_inventory_sheet(self, products: List[Dict[str, Any]]):
        """Añade hoja de inventario."""
        ws = self.wb.create_sheet("Inventario")
        
        # Encabezados
        headers = ["ID", "Nombre", "Categoría", "Código", "Proveedor", 
                  "Precio Compra", "Precio Venta", "Stock", "Stock Mínimo", "Diferencia"]
        
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            self._style_header(cell)
        
        # Datos
        for row_num, product in enumerate(products, 2):
            ws.cell(row=row_num, column=1, value=product.get("id", ""))
            ws.cell(row=row_num, column=2, value=product.get("name", ""))
            ws.cell(row=row_num, column=3, value=product.get("category", ""))
            ws.cell(row=row_num, column=4, value=product.get("code", ""))
            ws.cell(row=row_num, column=5, value=product.get("provider", ""))
            ws.cell(row=row_num, column=6, value=product.get("purchase_price", 0))
            ws.cell(row=row_num, column=7, value=product.get("sale_price", 0))
            ws.cell(row=row_num, column=8, value=product.get("stock", 0))
            ws.cell(row=row_num, column=9, value=product.get("min_stock", 0))
            
            # Diferencia entre stock y mínimo
            stock = product.get("stock", 0)
            min_stock = product.get("min_stock", 0)
            ws.cell(row=row_num, column=10, value=stock - min_stock)
            
            # Estilos a datos
            for col in range(1, 11):
                cell = ws.cell(row=row_num, column=col)
                self._style_cell(cell, "center" if col in [1, 8, 9, 10] else "left")
                
                # Formato de precio
                if col in [6, 7]:
                    cell.number_format = "$#,##0.00"
        
        # Ajustar ancho de columnas
        ws.column_dimensions['A'].width = 6
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 20
        ws.column_dimensions['F'].width = 14
        ws.column_dimensions['G'].width = 14
        ws.column_dimensions['H'].width = 10
        ws.column_dimensions['I'].width = 13
        ws.column_dimensions['J'].width = 12
    
    def add_sales_sheet(self, sales: List[Dict[str, Any]]):
        """Añade hoja de ventas."""
        ws = self.wb.create_sheet("Ventas")
        
        # Encabezados
        headers = ["ID", "Producto", "Cantidad", "Precio Unitario", "Total", "Fecha", "Hora"]
        
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            self._style_header(cell)
        
        # Datos
        for row_num, sale in enumerate(sales, 2):
            ws.cell(row=row_num, column=1, value=sale.get("id", ""))
            ws.cell(row=row_num, column=2, value=sale.get("product_name", ""))
            ws.cell(row=row_num, column=3, value=sale.get("quantity", 0))
            ws.cell(row=row_num, column=4, value=sale.get("unit_price", 0))
            ws.cell(row=row_num, column=5, value=sale.get("total", 0))
            ws.cell(row=row_num, column=6, value=sale.get("date", ""))
            ws.cell(row=row_num, column=7, value=sale.get("time", ""))
            
            # Estilos
            for col in range(1, 8):
                cell = ws.cell(row=row_num, column=col)
                self._style_cell(cell, "center" if col in [1, 3, 6, 7] else "right")
                
                # Formato de precio
                if col in [4, 5]:
                    cell.number_format = "$#,##0.00"
        
        # Ajustar ancho
        ws.column_dimensions['A'].width = 6
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 10
        ws.column_dimensions['D'].width = 16
        ws.column_dimensions['E'].width = 12
        ws.column_dimensions['F'].width = 12
        ws.column_dimensions['G'].width = 10
    
    def add_summary_sheet(self, products: List[Dict[str, Any]], sales: List[Dict[str, Any]]):
        """Añade hoja de resumen."""
        ws = self.wb.create_sheet("Resumen", 0)
        
        # Título
        title_cell = ws.cell(row=1, column=1, value="RESUMEN DE FERRETERÍA")
        title_cell.font = Font(bold=True, size=14, color="2c3e50")
        ws.merge_cells('A1:D1')
        
        # Fecha de generación
        ws.cell(row=2, column=1, value=f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Estadísticas
        total_products = len(products)
        total_stock = sum(p.get("stock", 0) for p in products)
        total_sales = len(sales)
        total_revenue = sum(s.get("total", 0) for s in sales)
        low_stock_products = len([p for p in products if p.get("stock", 0) < p.get("min_stock", 0)])
        
        row = 4
        stats = [
            ("Total de Productos", total_products),
            ("Stock Total", total_stock),
            ("Productos en Stock Bajo", low_stock_products),
            ("Total de Ventas", total_sales),
            ("Ingresos Totales", f"${total_revenue:,.2f}"),
        ]
        
        for label, value in stats:
            ws.cell(row=row, column=1, value=label).font = Font(bold=True)
            ws.cell(row=row, column=2, value=value)
            row += 1
        
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 20
    
    def save(self) -> bool:
        """Guarda el archivo Excel."""
        try:
            self.wb.save(self.output_path)
            return True
        except Exception as e:
            print(f"Error al guardar Excel: {e}")
            return False
    
    def export(self, products: List[Dict[str, Any]], sales: List[Dict[str, Any]]) -> str:
        """Exporta todos los datos a Excel."""
        try:
            self.add_summary_sheet(products, sales)
            self.add_inventory_sheet(products)
            self.add_sales_sheet(sales)
            
            if self.save():
                return self.output_path
            else:
                return None
        except Exception as e:
            print(f"Error durante exportación: {e}")
            return None
