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
    
    # Crear ventana raíz
    root = tk.Tk()
    
    # Mostrar ventana de login
    login = LoginWindow(root)
    username = login.show()
    
    # Si el login fue exitoso, abrir ventana principal
    if username:
        app_root = tk.Tk()
        app = MainWindow(app_root, username)
        app_root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        input("Presione Enter para salir...")
