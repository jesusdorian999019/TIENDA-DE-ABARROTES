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
import sys
import shutil
from pathlib import Path


def build_executable():
    """Construye el archivo ejecutable."""
    
    print("=" * 60)
    print("COMPILACION - Gestion de Ferreteria")
    print("=" * 60)
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
    except ImportError:
        print("\nERROR: PyInstaller no esta instalado")
        print("Instalelo con: pip install pyinstaller")
        return False
    
    # Rutas
    project_dir = Path(__file__).parent
    build_dir = project_dir / "build"
    dist_dir = project_dir / "dist"
    spec_file = project_dir / "FerreteriaPOS.spec"
    
    print("\nRutas:")
    print(f"  Proyecto: {project_dir}")
    print(f"  Build: {build_dir}")
    print(f"  Dist: {dist_dir}")
    
    # Limpiar builds anteriores - CON TOLERANCIA A ERRORES
    print("\nLimpiando builds anteriores...")
    
    # Forzar eliminacion de dist si existe
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir, ignore_errors=True)
            print(f"  Eliminado: {dist_dir}")
        except Exception as e:
            print(f"  Advertencia: No se pudo eliminar dist ({e})")
            # Intentar eliminar solo los archivos .exe
            for exe_file in dist_dir.glob("*.exe"):
                try:
                    exe_file.unlink()
                except:
                    pass
    
    # Limpiar build
    if build_dir.exists():
        try:
            shutil.rmtree(build_dir, ignore_errors=True)
            print(f"  Eliminado: {build_dir}")
        except:
            pass
    
    # Limpiar spec antiguo
    if spec_file.exists():
        try:
            spec_file.unlink()
            print(f"  Eliminado: {spec_file}")
        except:
            pass
    
    # Crear carpeta dist si no existe
    dist_dir.mkdir(exist_ok=True)
    build_dir.mkdir(exist_ok=True)
    
    # Comando de PyInstaller
    import subprocess
    
    print("\nCompilando...")
    print("   Esto puede tomar unos minutos...\n")
    
    cmd = [
        "pyinstaller",
        str(project_dir / "main.py"),
        "--onefile",
        "--windowed",
        "--name=FerreteriaPOS",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        "--noconfirm",
        "--hidden-import=bcrypt",
        "--hidden-import=openpyxl",
        f"--add-data={project_dir / 'data_storage'}{os.pathsep}data_storage"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            # Mostrar solo lineas importantes
            for line in result.stdout.split('\n'):
                if 'INFO' in line and any(x in line for x in ['built', 'completed']):
                    print(f"  {line[-80:]}")
    except subprocess.CalledProcessError as e:
        print("ERROR durante la compilacion:")
        print(e.stderr[-500:] if len(e.stderr) > 500 else e.stderr)
        return False
    
    # Verificar que se creo el ejecutable
    exe_path = dist_dir / "FerreteriaPOS.exe"
    if not exe_path.exists():
        print("\nERROR: El archivo ejecutable no se creo")
        return False
    
    print("\n" + "=" * 60)
    print("COMPILACION EXITOSA")
    print("=" * 60)
    print(f"\nEjecutable creado: {exe_path}")
    print(f"Tamaño: {exe_path.stat().st_size / (1024*1024):.2f} MB")
    
    print("\nInstrucciones de distribucion:")
    print("  1. Copie el archivo 'FerreteriaPOS.exe' a los clientes")
    print("  2. No se necesitan dependencias externas")
    print("  3. El programa creara las carpetas de datos automaticamente")
    
    print("\nPara ejecutar:")
    print(f"  Haga doble clic en: {exe_path.name}")
    print(f"  O ejecute: {exe_path}")
    
    return True


if __name__ == "__main__":
    try:
        success = build_executable()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
