"""Importador de productos desde CSV/Excel."""
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple


class ProductImporter:
    """Importador de productos desde archivos CSV/Excel."""

    def import_from_csv(self, file_path: str) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Importa productos desde un archivo CSV.

        Formato esperado:
        CODIGO;NOMBRE;CATEGORIA;MARCA;UNIDAD;P_COMPRA;P_VENTA;STOCK;STOCK_MIN;FLEXIBLE

        Returns:
            Tupla (éxito, mensaje, lista_productos)
        """
        try:
            products = []

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader, None)

                # Verificar si es el formato nuevo o el formato viejo
                is_new_format = 'P_COMPRA' in header[5].upper() if len(header) > 5 else False

                for row_num, row in enumerate(reader, start=2):
                    if not row or not row[0].strip():
                        continue

                    try:
                        code = row[0].strip()
                        if not code:
                            continue

                        # Formato nuevo: CODIGO;NOMBRE;CATEGORIA;MARCA;UNIDAD;P_COMPRA;P_VENTA;STOCK;STOCK_MIN;FLEXIBLE
                        if is_new_format:
                            nombre = row[1].strip() if len(row) > 1 and row[1].strip() else code
                            category = row[2].strip() if len(row) > 2 and row[2].strip() else "Otros"
                            marca = row[3].strip() if len(row) > 3 else ""
                            unidad = row[4].strip().upper() if len(row) > 4 and row[4].strip() else "UNIDAD"
                            p_compra = float(row[5].replace(',', '').strip()) if len(row) > 5 and row[5].strip() else 0.0
                            p_venta = float(row[6].replace(',', '').strip()) if len(row) > 6 and row[6].strip() else 0.0
                            stock = float(row[7].strip()) if len(row) > 7 and row[7].strip() else 0.0
                            stock_min = float(row[8].strip()) if len(row) > 8 and row[8].strip() else 0.0
                            flexible = row[9].strip().upper() == 'SI' if len(row) > 9 and row[9].strip() else False
                        else:
                            # Formato viejo CSV tienda: CODIGO;UNIDAD;EQUIVALENTE_SUNAT;P_VENTA;P_COMPRA;NOMBRE;FLEXIBLE;;STOCK
                            nombre = row[5].strip() if len(row) > 5 and row[5].strip() else code
                            if not nombre or len(nombre) < 2:
                                nombre = code
                            unidad = row[1].strip().upper() if len(row) > 1 and row[1].strip() else "UNIDAD"
                            # Precio venta en columna 3
                            p_venta = 0.0
                            if len(row) > 3 and row[3].strip():
                                try:
                                    p_venta = float(row[3].replace(',', '').strip())
                                except:
                                    pass
                            # Precio compra en columna 4
                            p_compra = 0.0
                            if len(row) > 4 and row[4].strip():
                                try:
                                    p_compra = float(row[4].replace(',', '').strip())
                                except:
                                    pass
                            # Flexible en columna 6
                            flexible = False
                            if len(row) > 6 and row[6].strip():
                                flexible = row[6].strip().upper() == 'SI'
                            # Stock en columna 8
                            stock = 0.0
                            if len(row) > 8 and row[8].strip():
                                try:
                                    stock = float(row[8].strip())
                                except:
                                    pass
                            stock_min = 5.0 if stock > 0 else 0.0
                            category = "Otros"
                            marca = ""

                        # Validaciones y CORRECCIÓN de precios
                        # Si tiene stock > 0 pero precios vacíos, usar valores por defecto
                        if stock > 0 and p_venta <= 0:
                            p_venta = 10.0
                            p_compra = 7.0
                        elif stock > 0 and p_compra <= 0:
                            p_compra = round(p_venta / 1.3, 2)
                            if p_compra <= 0:
                                p_compra = 7.0
                                p_venta = 10.0
                        elif p_venta <= p_compra and p_compra > 0:
                            p_venta = round(p_compra * 1.3, 2)
                        elif p_compra <= 0 and p_venta > 0:
                            p_compra = round(p_venta / 1.3, 2)
                        elif p_venta <= 0:
                            p_venta = 10.0
                            p_compra = 7.0

                        # Aceptar productos con stock 0 también
                        if stock_min <= 0:
                            stock_min = 5.0

                        product_dict = {
                            'code': code,
                            'name': nombre,
                            'category': category,
                            'provider': 'Proveedor',
                            'purchase_price': p_compra,
                            'sale_price': p_venta,
                            'stock': stock,
                            'min_stock': stock_min,
                            'marca': marca,
                            'unidad': unidad,
                            'flexible_stock': flexible,
                            'equivalente_sunat': '',
                            'tipo_igv': ''
                        }
                        products.append(product_dict)

                    except Exception as e:
                        print(f"Fila {row_num}: {e}")
                        continue

            return True, f"Se importaron {len(products)} productos", products

        except FileNotFoundError:
            return False, "Archivo no encontrado", []
        except Exception as e:
            return False, f"Error: {str(e)}", []

    def import_from_excel(self, file_path: str) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Importa productos desde un archivo Excel.

        Returns:
            Tupla (éxito, mensaje, lista_productos)
        """
        try:
            import pandas as pd

            df = pd.read_excel(file_path, header=0)
            products = []

            for _, row in df.iterrows():
                try:
                    code = str(row.get('CODIGO', '')).strip() if pd.notna(row.get('CODIGO')) else ""

                    if not code:
                        continue

                    name = str(row.get('NOMBRE', code)).strip()
                    if pd.isna(row.get('NOMBRE')):
                        name = code

                    category = str(row.get('CATEGORIA', 'Otros')).strip()
                    if pd.isna(row.get('CATEGORIA')):
                        category = 'Otros'

                    marca = str(row.get('MARCA', '')).strip()
                    if pd.isna(row.get('MARCA')):
                        marca = ''

                    unidad = str(row.get('UNIDAD', 'UNIDAD')).strip().upper()
                    if pd.isna(row.get('UNIDAD')):
                        unidad = 'UNIDAD'

                    p_compra = float(row.get('P_COMPRA', 0)) if pd.notna(row.get('P_COMPRA')) else 0.0
                    p_venta = float(row.get('P_VENTA', 0)) if pd.notna(row.get('P_VENTA')) else 0.0
                    stock = float(row.get('STOCK', 0)) if pd.notna(row.get('STOCK')) else 0.0
                    stock_min = float(row.get('STOCK_MIN', 0)) if pd.notna(row.get('STOCK_MIN')) else 0.0
                    flexible = str(row.get('FLEXIBLE', 'NO')).strip().upper() == 'SI'

                    # Validaciones
                    if p_venta <= p_compra:
                        continue
                    if stock < stock_min:
                        continue

                    product_dict = {
                        'code': code,
                        'name': name,
                        'category': category,
                        'provider': 'Proveedor',
                        'purchase_price': p_compra,
                        'sale_price': p_venta,
                        'stock': stock,
                        'min_stock': stock_min,
                        'marca': marca,
                        'unidad': unidad,
                        'flexible_stock': flexible,
                        'equivalente_sunat': '',
                        'tipo_igv': ''
                    }

                    products.append(product_dict)

                except Exception as e:
                    print(f"Error en fila: {e}")
                    continue

            total = len(products)
            return True, f"Se importaron {total} productos", products

        except ImportError:
            return False, "Library 'openpyxl' not installed", []
        except FileNotFoundError:
            return False, "Archivo no encontrado", []
        except Exception as e:
            return False, f"Error al importar: {str(e)}", []