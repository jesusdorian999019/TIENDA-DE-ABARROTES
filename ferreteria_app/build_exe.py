#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para compilar la aplicación a un ejecutable .exe usando PyInstaller.

Uso:
    python build_exe.py

Requisitos previos:
    pip install pyinstaller
"""

import os
import shutil
from pathlib import Path


def build_executable():
    """Construye el archivo ejecutable."""
    
    print("=" * 60)
    print("COMPILACIÓN - Gestión de Ferretería")
    print("=" * 60)
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
    except ImportError:
        print("\n❌ Error: PyInstaller no está instalado")
        print("Instálelo con: pip install pyinstaller")
        return False
    
    # Rutas
    project_dir = Path(__file__).parent
    build_dir = project_dir / "build"
    dist_dir = project_dir / "dist"
    spec_file = project_dir / "ferreteria_app.spec"
    
    print("\n📁 Rutas:")
    print(f"  Proyecto: {project_dir}")
    print(f"  Build: {build_dir}")
    print(f"  Dist: {dist_dir}")
    
    # Limpiar builds anteriores
    print("\n🧹 Limpiando builds anteriores...")
    for directory in [build_dir, dist_dir]:
        if directory.exists():
            shutil.rmtree(directory)
            print(f"   Eliminado: {directory}")
    
    if spec_file.exists():
        spec_file.unlink()
        print(f"   Eliminado: {spec_file}")
    
    # Comando de PyInstaller
    import subprocess
    
    print("\n🔨 Compilando...")
    print("   Esto puede tomar unos minutos...\n")
    
    cmd = [
        "pyinstaller",
        str(project_dir / "main.py"),
        "--onefile",
        "--windowed",
        "--name=FerreteriaPOS",
        "--console",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        "--noconfirm"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Error durante la compilación:")
        print(e.stderr)
        return False
    
    # Verificar que se creó el ejecutable
    exe_path = dist_dir / "FerreteriaPOS.exe"
    if not exe_path.exists():
        print("\n❌ Error: El archivo ejecutable no se creó")
        return False
    
    print("\n" + "=" * 60)
    print("✅ COMPILACIÓN EXITOSA")
    print("=" * 60)
    print(f"\n📦 Ejecutable creado: {exe_path}")
    print(f"   Tamaño: {exe_path.stat().st_size / (1024*1024):.2f} MB")
    
    print("\n📋 Instrucciones de distribución:")
    print("   1. Copie el archivo 'Ferreteria.exe' a los clientes")
    print("   2. No se necesitan dependencias externas")
    print("   3. El programa creará las carpetas de datos automáticamente")
    
    print("\n🚀 Para ejecutar:")
    print(f"   Haga doble clic en: {exe_path.name}")
    
    return True


if __name__ == "__main__":
    import sys
    
    try:
        success = build_executable()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
