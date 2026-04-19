#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para compilar la aplicación a un ejecutable .exe usando PyInstaller."""

import os
import sys
import shutil
from pathlib import Path
import subprocess


def build_executable():
    """Construye el archivo ejecutable."""

    print('=' * 60)
    print('COMPILACION - Gestion de Ferreteria')
    print('=' * 60)

    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
    except ImportError:
        print('\\nERROR: PyInstaller no esta instalado')
        print('Instalelo con: pip install pyinstaller')
        return False

    # Rutas
    project_dir = Path(__file__).parent
    build_dir = project_dir / 'build'
    dist_dir = project_dir / 'dist'
    spec_file = project_dir / 'FerreteriaPOS.spec'

    print('\\nRutas:')
    print(f'  Proyecto: {project_dir}')
    print(f'  Build: {build_dir}')
    print(f'  Dist: {dist_dir}')

    # Limpiar builds anteriores
    print('\\nLimpiando builds anteriores...')
    if dist_dir.exists():
        shutil.rmtree(dist_dir, ignore_errors=True)
        print(f'  Eliminado: {dist_dir}')
    if build_dir.exists():
        shutil.rmtree(build_dir, ignore_errors=True)
        print(f'  Eliminado: {build_dir}')
    if spec_file.exists():
        spec_file.unlink()
        print(f'  Eliminado: {spec_file}')

    # Crear carpetas
    dist_dir.mkdir(exist_ok=True)
    build_dir.mkdir(exist_ok=True)

    print('\\nCompilando... (puede tomar minutos)')

    cmd = [
        'pyinstaller',
        str(project_dir / 'main.py'),
        '--onefile',
        '--windowed',
        '--name=FerreteriaPOS',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        '--noconfirm',
        '--hidden-import=bcrypt',
        '--hidden-import=openpyxl',
        f'--add-data={project_dir / "data_storage"}{os.pathsep}data_storage'
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print('Compilacion completada.')
    except subprocess.CalledProcessError as e:
        print('ERROR en compilacion:')
        print(e.stderr[-1000:])
        return False

    # Verificar EXE
    exe_path = dist_dir / 'FerreteriaPOS.exe'
    if exe_path.exists():
        print('\\n' + '=' * 60)
        print('✅ COMPILACION EXITOSA')
        print(f'Ejecutable: {exe_path}')
        print(f'Tamaño: {exe_path.stat().st_size / (1024*1024):.1f} MB')
        return True
    return False


if __name__ == '__main__':
    try:
        success = build_executable()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f'\\nERROR: {e}')
        sys.exit(1)

