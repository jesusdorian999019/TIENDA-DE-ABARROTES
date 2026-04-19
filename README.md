# Gestión de Ferretería

Aplicación de escritorio para gestión de inventario y ventas de ferretería.

## Instrucciones de Uso

### Opción 1: Archivo Ejecutable (Recomendado)
1. Descargar Ferreteria.exe desde la sección Releases del repositorio
2. Hacer doble clic para ejecutar
3. Usuario inicial: admin / admin123

No requiere instalación de Python.

### Opción 2: Para Desarrolladores
```bash
pip install -r requirements.txt
python main.py
```

## Funcionalidades
- Gestión completa de inventario (crear, editar, eliminar productos)
- Registro de ventas con actualización automática de stock
- Reportes y dashboard con gráficos
- Exportación de datos a Excel
- Búsqueda y filtrado de productos
- Alertas de stock bajo

## Estructura de Archivos
```
ferreteria_app/
├── main.py               - Punto de entrada
├── requirements.txt      - Dependencias
├── business/             - Lógica de negocio
├── ui/                   - Interfaz gráfica
├── data/                 - Gestión de datos JSON
├── config/               - Configuración
├── utils/                - Utilidades
└── data_storage/         - Archivos de datos (users.json, products.json, sales.json)
```

## Generar Ejecutable .exe
```bash
pip install pyinstaller
python build_exe.py
```
Archivo generado: dist/Ferreteria.exe

## Datos de Prueba
```bash
python load_demo_data.py
```
Luego reiniciar la aplicación.

## Soporte Técnico
Datos guardados en data_storage/
- users.json - Usuarios
- products.json - Productos
- sales.json - Ventas

Usuario administrador: admin / admin123

## Documentación Adicional
- ARQUITECTURA.md - Diseño del sistema
- INICIO_RAPIDO.md - Guía de inicio
- INSTALL_INSTRUCTIONS.txt - Instalación detallada
