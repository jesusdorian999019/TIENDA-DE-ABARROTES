# Ferretería Management System

Sistema de punto de venta desktop profesional para ferreterías.

## Instalación y Uso

### Para usuarios sin conocimientos técnicos
1. Descargar `Ferreteria.exe` desde Releases (GitHub)
2. Hacer doble clic para ejecutar
3. Usuario inicial: `admin` / `admin123`

### Para desarrolladores
```bash
pip install -r requirements.txt
python main.py
```

## Características
- Gestión completa de inventario (CRUD)
- Ventas en tiempo real con sincronización de stock
- Reportes y dashboard (exportación Excel)
- Alto rendimiento con paginación
- Interfaz auto-actualizable

## Estructura del Proyecto
```
ferreteria_app/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── business/               # Lógica de negocio
├── ui/                     # Interfaz Tkinter
├── data/                   # Persistencia JSON
├── config/                 # Configuración
├── utils/                  # Utilidades
└── data_storage/           # Datos (creados automáticamente)
```

## Documentación
- INSTALL_INSTRUCTIONS.txt - Instalación detallada
- ARQUITECTURA.md - Diseño del sistema
- INICIO_RAPIDO.md - Guía rápida
- JSON_FORMAT_SPEC.md - Formato de datos

## Generar Ejecutable
```bash
pip install pyinstaller
python build_exe.py
```
Resultado: `dist/Ferreteria.exe`

## Soporte Técnico
- Archivos de datos en `data_storage/`
- Usuario administrador: admin / admin123
- Backup: Copiar carpeta `data_storage/`
