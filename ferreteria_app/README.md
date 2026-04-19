# Gestión de Ferretería - Aplicación Desktop

Aplicación profesional de escritorio para la gestión integral de pequeñas y medianas ferreterías. Desarrollada en Python con interfaz gráfica Tkinter, almacenamiento JSON y exportación a Excel.

## Inicio Rápido (Usuarios Finales)

### Requisitos del Sistema

- Sistema Operativo: Windows 10 o superior
- RAM mínima: 512 MB
- Espacio en disco: 100 MB
- Conexión a Internet: No requerida

### Instalación

1. Descargar el archivo ejecutable `FerreteriaPOS.exe` desde la carpeta `/dist`
2. Hacer doble clic en `FerreteriaPOS.exe`
3. La aplicación se iniciará automáticamente

**Nota:** No requiere instalación previa de Python ni dependencias externas.

### Inicio de Sesión

Credenciales por defecto:
```
Usuario:     admin
Contraseña:  admin123
```

Después del primer acceso, puede crear usuarios adicionales desde la aplicación.

## Características Principales

### Gestión de Inventario
- Crear, editar y eliminar productos
- Búsqueda y filtrado en tiempo real
- Alertas visuales de stock bajo
- Seguimiento de categorías de productos
- Información de proveedores y códigos de producto

### Registro de Ventas
- Entrada rápida de transacciones
- Cálculo automático de totales
- Descuento automático de inventario
- Historial de ventas con filtrado por fecha
- Resumen diario y mensual

### Reportes y Análisis
- Dashboard con indicadores clave de desempeño
- Reporte de inventario detallado
- Análisis de ventas por período
- Productos más vendidos
- Análisis por categoría

### Exportación de Datos
- Generación de reportes en formato Excel (.xlsx)
- Múltiples hojas de datos
- Formatos profesionales con estilos
- Gráficos automáticos

## Guía de Uso

### Primer Acceso

1. Inicie sesión con las credenciales por defecto
2. Navegue entre las pestañas: Inventario, Ventas y Reportes
3. Configure sus productos en la pestaña de Inventario
4. Registre ventas en la pestaña de Ventas
5. Consulte análisis en la pestaña de Reportes

### Pestañas Principales

#### Inventario
- Visualice todos los productos registrados
- Agregue nuevos productos con detalles completos
- Modifique información de productos existentes
- Elimine productos del sistema
- Busque productos por nombre o código

#### Ventas
- Seleccione un producto de la lista
- Ingrese la cantidad vendida
- El precio y total se calculan automáticamente
- Confirme la venta
- Consulte el historial de transacciones

#### Reportes
- Visualice métricas de desempeño
- Consulte estado del inventario
- Analice ventas por período
- Identifique productos de mayor demanda

## Configuración Avanzada (Desarrolladores)

### Requisitos de Desarrollo

- Python 3.8 o superior
- pip (gestor de paquetes)

### Instalación del Entorno de Desarrollo

1. Clonar o descargar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activar el entorno:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución desde Código Fuente

```bash
python main.py
```

### Estructura del Proyecto

```
ferreteria_app/
├── main.py                      # Punto de entrada
├── requirements.txt             # Dependencias
├── build_exe.py                 # Script para compilación
│
├── config/
│   └── settings.py              # Configuración global
│
├── data/
│   ├── models.py                # Modelos de datos
│   ├── data_manager.py          # Interfaz de acceso a datos
│   └── json_manager.py          # Implementación JSON
│
├── business/
│   ├── user_service.py          # Gestión de usuarios
│   ├── inventory_service.py     # Lógica de inventario
│   ├── sales_service.py         # Lógica de ventas
│   └── reports_service.py       # Generación de reportes
│
├── ui/
│   ├── login_window.py          # Ventana de autenticación
│   ├── main_window.py           # Ventana principal
│   ├── inventory_tab.py         # Interfaz de inventario
│   ├── sales_tab.py             # Interfaz de ventas
│   └── reports_tab.py           # Interfaz de reportes
│
├── utils/
│   ├── security.py              # Seguridad (hash bcrypt)
│   ├── validators.py            # Validación de datos
│   └── excel_exporter.py        # Exportación a Excel
│
└── data_storage/               # Almacenamiento (se crea automáticamente)
    ├── users.json
    ├── products.json
    └── sales.json
```

### Generación del Ejecutable

Para crear una nueva versión del archivo .exe:

```bash
pip install pyinstaller
python build_exe.py
```

El ejecutable se generará en la carpeta `dist/FerreteriaPOS.exe`

### Ejecución de Tests

```bash
pip install pytest
python -m pytest tests.py -v
```

## Arquitectura de Software

### Patrón de Capas

La aplicación implementa una arquitectura de 3 capas:

1. **Capa de Presentación (UI)**: Interfaz gráfica con Tkinter
2. **Capa de Lógica de Negocio**: Services (InventoryService, SalesService, etc.)
3. **Capa de Acceso a Datos**: DataManager (interfaz abstracta)

### Beneficios del Diseño

- Separación de responsabilidades
- Fácil mantenimiento y extensión
- Preparada para migración a base de datos SQL
- Testeable y modular
- Escalable sin refactorización mayor

## Seguridad

### Almacenamiento de Contraseñas

Las contraseñas se almacenan mediante hash bcrypt con la siguiente configuración:
- Algoritmo: bcrypt
- Rounds: 12
- Fallback: SHA256 (en caso de no disponibilidad de bcrypt)

### Validación de Datos

Todos los datos ingresados por el usuario se validan en la capa de negocio antes de procesarse.

## Almacenamiento de Datos

Los datos se almacenan localmente en formato JSON:

- `users.json`: Información de usuarios y contraseñas
- `products.json`: Catálogo de productos
- `sales.json`: Historial de transacciones

Estos archivos se crean automáticamente al primer uso en la carpeta `data_storage/`

### Backup de Datos

Se recomienda realizar backups periódicos de la carpeta `data_storage/`:

```bash
xcopy data_storage data_storage_backup /E /I
```

## Migración a Base de Datos SQL

La arquitectura está preparada para migración a SQLite o MySQL sin cambios en la interfaz o lógica de negocio.

Para migrar:
1. Crear `data/sqlite_manager.py` implementando la interfaz `DataManager`
2. Modificar `main.py`: cambiar `JsonManager()` por `SqliteManager()`
3. Ejecutar migración de datos

## Troubleshooting

### La aplicación no inicia

- Verificar que el sistema sea Windows 10 o superior
- Descargar nuevamente el ejecutable
- Verificar que haya espacio en disco (mínimo 100 MB)

### Error al crear productos

- Verificar que los campos requeridos estén completos
- Verificar que los precios sean números válidos
- Verificar que el stock sea un número entero positivo

### Datos no se guardan

- Verificar permisos de escritura en la carpeta de la aplicación
- Verificar espacio disponible en disco
- Consultar la carpeta `data_storage/` para ver archivos JSON

## Créditos y Licencia

Desarrollado como prototipo funcional para gestión de ferreterías.

## Contacto y Soporte

Para reportar problemas o sugerencias, contacte al equipo de desarrollo.

---

Versión: 1.0.0
Última actualización: Abril 2026
Plataforma: Windows 10/11
