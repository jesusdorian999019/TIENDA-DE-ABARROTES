@echo off
REM Launcher para Gestión de Ferretería
REM Este script prepara el entorno y ejecuta la aplicación

setlocal enabledelayedexpansion

REM Obtener la ruta del script
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Crear carpeta data_storage si no existe
if not exist "ferreteria_app\data_storage" (
    echo Creando carpeta de almacenamiento...
    mkdir "ferreteria_app\data_storage"
)

REM Ejecutar el ejecutable
echo Iniciando Gestión de Ferretería...
start "" "ferreteria_app\dist\FerreteriaPOS.exe"

REM Si no funciona desde aquí, intentar desde dist
if errorlevel 1 (
    cd /d "%SCRIPT_DIR%ferreteria_app\dist\"
    start "" FerreteriaPOS.exe
)

exit /b 0
