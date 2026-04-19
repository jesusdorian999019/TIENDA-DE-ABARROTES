#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico EXHAUSTIVO con logs detallados
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Crear archivo de log
log_file = Path("d:\\Proyectos Codigo\\TIENDA DE ABARROTES\\app_diagnostic.log")

def log_msg(msg):
    """Registra mensaje en archivo y pantalla"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_line = f"[{timestamp}] {msg}"
    print(log_line)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

# Limpiar log previo
log_file.write_text("")

log_msg("=" * 80)
log_msg("DIAGNOSTICO EXHAUSTIVO DE FERRETERIAPOS")
log_msg("=" * 80)

try:
    log_msg(f"\n[1] PYTHON VERSION: {sys.version}")
    log_msg(f"[2] WORKING DIRECTORY: {os.getcwd()}")
    log_msg(f"[3] PYTHON EXECUTABLE: {sys.executable}")
    
    # Agregar path
    ferreteria_path = Path("d:\\Proyectos Codigo\\TIENDA DE ABARROTES\\ferreteria_app")
    sys.path.insert(0, str(ferreteria_path))
    log_msg(f"\n[4] FERRETERIA PATH: {ferreteria_path}")
    log_msg(f"[5] FERRETERIA PATH EXISTS: {ferreteria_path.exists()}")
    
    # Importaciones
    log_msg("\n[IMPORTS] Iniciando importaciones...")
    
    log_msg("   -> Importando tkinter...")
    import tkinter as tk
    log_msg("      [OK] tkinter")
    
    log_msg("   -> Importando config.settings...")
    from config.settings import APP_TITLE, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD
    log_msg(f"      [OK] APP_TITLE = {APP_TITLE}")
    
    log_msg("   -> Importando business.user_service...")
    from business.user_service import UserService
    log_msg("      [OK] UserService")
    
    log_msg("   -> Importando ui.login_window...")
    from ui.login_window import LoginWindow
    log_msg("      [OK] LoginWindow")
    
    log_msg("   -> Importando ui.main_window...")
    from ui.main_window import MainWindow
    log_msg("      [OK] MainWindow")
    
    log_msg("\n[SETUP] Inicializando servicios...")
    
    log_msg("   -> Creando UserService...")
    user_service = UserService()
    log_msg("      [OK] UserService creado")
    
    log_msg("   -> Inicializando usuario por defecto...")
    user_service.initialize_default_user()
    log_msg(f"      [OK] Usuario por defecto: {DEFAULT_ADMIN_USERNAME}")
    
    log_msg("\n[GUI] Iniciando interfaz gráfica...")
    
    log_msg("   -> Creando Tk root...")
    login_root = tk.Tk()
    log_msg("      [OK] Tk root creado")
    
    log_msg("   -> Ocultando ventana inicial...")
    login_root.withdraw()
    log_msg("      [OK] Ventana oculta")
    
    log_msg("   -> Creando LoginWindow...")
    login = LoginWindow(login_root)
    log_msg("      [OK] LoginWindow creado")
    
    log_msg("\n[WINDOW] MOSTRANDO VENTANA DE LOGIN")
    log_msg("========================================")
    log_msg(f"USUARIO DEMO: {DEFAULT_ADMIN_USERNAME}")
    log_msg(f"PASSWORD DEMO: {DEFAULT_ADMIN_PASSWORD}")
    log_msg("========================================")
    
    log_msg("\n   -> Mostrando ventana...")
    username = login.show()
    log_msg(f"   <- Usuario retornado: {username}")
    
    if username:
        log_msg(f"\n[LOGIN] Login exitoso: {username}")
        
        log_msg("   -> Creando ventana principal...")
        main_root = tk.Tk()
        log_msg("      [OK] Tk root creado")
        
        main_root.geometry("1000x700+100+100")
        main_root.title(f"{APP_TITLE} - {username}")
        log_msg(f"      [OK] Ventana configurada")
        
        log_msg("   -> Creando MainWindow...")
        app = MainWindow(main_root, username)
        log_msg("      [OK] MainWindow creado")
        
        log_msg("   -> Iniciando mainloop...")
        main_root.mainloop()
        log_msg("      [OK] Mainloop completado (ventana cerrada)")
    else:
        log_msg("\n[LOGIN] Login cancelado o fallido")
    
    log_msg("\n[FINISH] Aplicacion finalizada normalmente")
    
except Exception as e:
    log_msg(f"\n[ERROR] EXCEPCION: {e}")
    log_msg(f"[ERROR] TYPE: {type(e).__name__}")
    import traceback
    log_msg("[TRACEBACK]:")
    for line in traceback.format_exc().split("\n"):
        log_msg(f"  {line}")
    sys.exit(1)

log_msg("\n" + "=" * 80)
log_msg(f"LOG GUARDADO EN: {log_file}")
log_msg("=" * 80)
