#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestión de Ferretería - Aplicación Desktop

Prototipo funcional para gestión de una pequeña ferretería.
Almacenamiento en JSON, arquitectura preparada para migración a SQL.

Características:
- Gestión de inventario
- Registro de ventas
- Reportes y análisis
- Exportación a Excel
- Sistema de login seguro
"""

import tkinter as tk
from pathlib import Path
import sys

# Añadir el directorio actual al path para importar módulos locales
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import APP_TITLE
from business.user_service import UserService
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main():
    """Punto de entrada de la aplicación."""
    
    # Inicializar usuario por defecto
    user_service = UserService()
    user_service.initialize_default_user()
    
    # Crear una única ventana raíz
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana inicial
    
    # Mostrar ventana de login
    login = LoginWindow(root)
    username = login.show()
    
    # Si el login fue exitoso, mostrar ventana principal en la misma ventana
    if username:
        root.deiconify()  # Mostrar la ventana
        root.geometry("1000x700+100+100")
        root.title("Gestión de Ferretería - Principal")
        app = MainWindow(root, username)
        root.mainloop()
    else:
        root.destroy()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        input("Presione Enter para salir...")
