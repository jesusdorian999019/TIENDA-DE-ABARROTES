#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar la aplicación con manejo de errores visible.
"""

import sys
from pathlib import Path

# Agregar ferreteria_app al path
ferreteria_path = Path(__file__).parent / "ferreteria_app"
sys.path.insert(0, str(ferreteria_path))

print("=" * 60)
print("GESTIÓN DE FERRETERÍA - Iniciando...")
print("=" * 60)

try:
    print("\n✓ Importando módulos...")
    from ferreteria_app.config.settings import APP_TITLE
    from ferreteria_app.business.user_service import UserService
    from ferreteria_app.ui.login_window import LoginWindow
    from ferreteria_app.ui.main_window import MainWindow
    import tkinter as tk
    
    print("✓ Módulos importados exitosamente")
    
    print("\n✓ Inicializando aplicación...")
    
    # Inicializar usuario por defecto
    user_service = UserService()
    user_service.initialize_default_user()
    print("✓ Usuario de demostración inicializado (admin/admin123)")
    
    # Crear ventana para login
    login_root = tk.Tk()
    login_root.withdraw()  # Ocultar la ventana inicial
    
    print("✓ Mostrando ventana de login...")
    print("\n" + "=" * 60)
    print("VENTANA DE LOGIN ABIERTA")
    print("=" * 60)
    print("Credenciales de demo:")
    print("  Usuario: admin")
    print("  Contraseña: admin123")
    print("=" * 60 + "\n")
    
    # Mostrar ventana de login
    login = LoginWindow(login_root)
    username = login.show()
    
    # Si el login fue exitoso, mostrar ventana principal
    if username:
        print(f"✓ Login exitoso: {username}")
        print("\n✓ Abriendo ventana principal...")
        
        # Crear nueva ventana para la aplicación principal
        main_root = tk.Tk()
        main_root.geometry("1000x700+100+100")
        main_root.title(f"{APP_TITLE} - {username}")
        app = MainWindow(main_root, username)
        main_root.mainloop()
        print("✓ Aplicación cerrada normalmente")
    else:
        # Login cancelado
        print("⚠ Login cancelado por el usuario")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    print("\nDetalles del error:")
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Programa terminado")
sys.exit(0)
