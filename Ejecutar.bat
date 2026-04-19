@echo off
REM Launcher para Gestión de Ferretería
REM Este script prepara el entorno y ejecuta la aplicación

setlocal enabledelayedexpansion
chcp 65001 >nul

REM Obtener la ruta del script
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Crear carpeta data_storage si no existe
if not exist "ferreteria_app\data_storage" (
    echo Creando carpeta de almacenamiento...
    mkdir "ferreteria_app\data_storage"
)

REM Validar que el ejecutable existe
set EXE_PATH=%SCRIPT_DIR%ferreteria_app\dist\FerreteriaPOS.exe

if not exist "!EXE_PATH!" (
    echo.
    echo ============================================
    echo ERROR: No se encontró el ejecutable
    echo Ruta esperada: !EXE_PATH!
    echo.
    echo Asegúrate de que:
    echo 1. La carpeta dist existe
    echo 2. FerreteriaPOS.exe está en ella
    echo 3. Ejecutaste build_exe.py correctamente
    echo ============================================
    echo.
    pause
    exit /b 1
)

REM Ejecutar el ejecutable
echo.
echo Iniciando FerreteriaPOS...
echo.
start "" "!EXE_PATH!"
timeout /t 2 /nobreak

exit /b 0
