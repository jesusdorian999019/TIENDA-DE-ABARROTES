# Gestión de Ferretería - Sistema Desktop

Sistema profesional de gestión para ferreterías desarrollado en Python. Incluye interfaz gráfica desktop, gestión de inventario, registro de ventas, reportes analíticos y exportación a Excel.

## Descarga Rápida

### Para Usuarios Finales (Opción Recomendada)

**Metodo 1: Script Automático (Lo más fácil)**

1. Descargar toda la carpeta del proyecto
2. En la carpeta raíz, hacer DOBLE CLIC en: `Ejecutar.bat`
3. La aplicación se abrirá automáticamente
4. Ingresar: `admin / admin123`

El script crea automáticamente la carpeta de datos y ejecuta el programa.

**Metodo 2: Solo el ejecutable**

1. Navegar a: `ferreteria_app/dist/`
2. Hacer DOBLE CLIC en: `Ejecutar.bat` (si está disponible)
3. O directamente en: `FerreteriaPOS.exe`
4. Ingresar: `admin / admin123`

**Método 3: Desde PowerShell o CMD**

```bash
cd ferreteria_app\dist
FerreteriaPOS.exe
```

**Requisitos:**
- Windows 10 o 11
- RAM: 512 MB mínimo
- Disco: 100 MB disponible
- No requiere Python instalado
- No requiere conexión a Internet

**Nota:** La carpeta de almacenamiento se crea automáticamente al primer uso.

## Características Principales

- Gestión integral de inventario con alertas de stock bajo
- Registro de ventas en tiempo real con cálculo automático
- Reportes y análisis de desempeño con indicadores clave
- Exportación de datos a Excel con formatos profesionales
- Sistema de autenticación de usuarios con contraseñas hasheadas
- Almacenamiento local seguro en JSON
- Interfaz gráfica profesional con Tkinter
- Búsqueda y filtrado en tiempo real
- Historial de transacciones con análisis por período

## Instalación para Desarrolladores

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes)
- Git (opcional)

### Pasos de Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/usuario/TIENDA-DE-ABARROTES.git
cd TIENDA-DE-ABARROTES
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r ferreteria_app/requirements.txt
```

5. Ejecutar aplicación:
```bash
python ferreteria_app/main.py
```

## Compilación a Ejecutable

Para crear una nueva versión del archivo .exe:

```bash
cd ferreteria_app
pip install pyinstaller
python build_exe.py
```

El ejecutable compilado se generará en: `ferreteria_app/dist/FerreteriaPOS.exe`

## Estructura del Proyecto

```
TIENDA-DE-ABARROTES/
├── ferreteria_app/
│   ├── dist/
│   │   └── FerreteriaPOS.exe          (Ejecutable compilado)
│   ├── build/                         (Generado por PyInstaller)
│   │
│   ├── main.py                        (Punto de entrada)
│   ├── requirements.txt               (Dependencias)
│   ├── build_exe.py                   (Script de compilación)
│   ├── tests.py                       (Suite de tests)
│   ├── load_demo_data.py              (Generador de datos demo)
│   │
│   ├── README.md                      (Documentación detallada)
│   ├── ARQUITECTURA.md                (Diseño técnico)
│   ├── INICIO_RAPIDO.md               (Guía rápida)
│   ├── JSON_FORMAT_SPEC.md            (Especificación de datos)
│   ├── DOCUMENTACION_INDEX.md         (Índice de documentación)
│   ├── INSTALL_INSTRUCTIONS.txt       (Instalación paso a paso)
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py                (Configuración global)
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── models.py                  (Modelos de datos)
│   │   ├── data_manager.py            (Interfaz abstracta)
│   │   └── json_manager.py            (Implementación JSON)
│   │
│   ├── business/
│   │   ├── __init__.py
│   │   ├── user_service.py            (Gestión de usuarios)
│   │   ├── inventory_service.py       (Lógica de inventario)
│   │   ├── sales_service.py           (Lógica de ventas)
│   │   └── reports_service.py         (Generación de reportes)
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_window.py            (Ventana de autenticación)
│   │   ├── main_window.py             (Ventana principal)
│   │   ├── inventory_tab.py           (Tab de inventario)
│   │   ├── sales_tab.py               (Tab de ventas)
│   │   └── reports_tab.py             (Tab de reportes)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py                (Hash bcrypt)
│   │   ├── validators.py              (Validación de datos)
│   │   └── excel_exporter.py          (Exportación a Excel)
│   │
│   └── data_storage/                 (Creado automáticamente)
│       ├── users.json
│       ├── products.json
│       └── sales.json
│
└── README.md                          (Este archivo)
```

## Guía de Uso

### Inicio de Sesión

Credenciales por defecto:
- Usuario: `admin`
- Contraseña: `admin123`

Después del primer acceso, puede crear usuarios adicionales.

### Funcionalidades

#### Inventario
- Visualizar todos los productos registrados
- Agregar nuevos productos con información completa
- Modificar datos de productos existentes
- Eliminar productos del sistema
- Buscar productos por nombre o código
- Alertas visuales de stock bajo

#### Ventas
- Seleccionar productos del inventario
- Ingresar cantidad vendida
- Cálculo automático de totales
- Descuento automático de stock
- Historial de transacciones
- Filtrado por período

#### Reportes
- Dashboard con indicadores clave de desempeño
- Reporte detallado de inventario
- Análisis de ventas por período
- Identificación de productos de mayor demanda
- Análisis por categoría de productos

#### Exportación
- Generar reportes en formato Excel
- Múltiples hojas de datos
- Formatos profesionales con estilos
- Cálculos y gráficos automáticos

## Arquitectura de Software

### Patrón de Capas

La aplicación implementa una arquitectura de 3 capas separadas:

1. **Capa de Presentación (UI)**: Interfaz gráfica con Tkinter
2. **Capa de Lógica de Negocio**: Services (InventoryService, SalesService, etc.)
3. **Capa de Acceso a Datos**: DataManager (interfaz abstracta)

### Beneficios del Diseño

- Separación clara de responsabilidades
- Código mantenible y extensible
- Fácil de testear y depurar
- Preparada para migración a base de datos SQL
- Escalable sin refactorización mayor
- Reutilizable para otras interfaces (web, móvil)

### Migración a SQL

La arquitectura está diseñada para permitir migración a SQLite o MySQL sin cambios en:
- Interfaz gráfica (UI)
- Lógica de negocio (Business Layer)
- Tests

Para migrar:
1. Crear archivo `data/sqlite_manager.py`
2. Implementar interfaz `DataManager`
3. Cambiar en `main.py`: `JsonManager()` por `SqliteManager()`

## Seguridad

### Almacenamiento de Contraseñas

Las contraseñas se almacenan usando hash bcrypt:
- Algoritmo: bcrypt
- Rounds: 12
- Fallback: SHA256 (para compatibilidad)

### Validación de Datos

Todos los datos ingresados se validan en la capa de negocio antes de procesarse.

### Almacenamiento Local

Los datos se guardan en JSON local sin conexión remota requerida.

## Almacenamiento de Datos

### Estructura de Archivos

Los datos se almacenan en `ferreteria_app/data_storage/`:

- `users.json`: Usuarios y credenciales
- `products.json`: Catálogo de productos
- `sales.json`: Historial de ventas

Estos archivos se crean automáticamente al primer uso.

### Backup de Datos

Se recomienda realizar backups periódicos:

```bash
# Windows
xcopy data_storage data_storage_backup /E /I

# Linux/Mac
cp -r data_storage data_storage_backup
```

## Dependencias

- openpyxl 3.11.5: Exportación a Excel
- bcrypt 4.0.1: Hash seguro de contraseñas
- tkinter: Interfaz gráfica (incluido con Python)

## Ejecución de Tests

```bash
pip install pytest
python -m pytest ferreteria_app/tests.py -v
```

## Troubleshooting

### La aplicación no inicia

**Problema:** "ModuleNotFoundError"
- Solución: Instalar dependencias con `pip install -r requirements.txt`

**Problema:** Ventana no aparece
- Solución: Verificar que sea Windows 10 o superior

### Datos no se guardan

**Problema:** Carpeta data_storage no se crea
- Solución: Verificar permisos de escritura en la carpeta del proyecto

**Problema:** Error al guardar
- Solución: Verificar espacio disponible en disco (mínimo 100 MB)

### Error al compilar .exe

**Problema:** "PyInstaller not found"
- Solución: `pip install pyinstaller`

**Problema:** El .exe no ejecuta
- Solución: Agregar excepción en antivirus

## Ejecución desde Código Fuente vs Ejecutable

### Desde Código Fuente
- Requiere Python instalado
- Requiere instalar dependencias
- Ideal para desarrollo y debugging
- Más lento en inicio

### Desde Ejecutable
- Sin requisitos previos (solo Windows)
- Inicio rápido
- Ideal para usuarios finales
- Tamaño: 22.81 MB

## Características Técnicas

- Lenguaje: Python 3.8+
- Interfaz: Tkinter
- Almacenamiento: JSON (preparado para SQL)
- Seguridad: bcrypt
- Exportación: openpyxl
- Compilación: PyInstaller

## Requerimientos del Sistema

### Requisitos Mínimos

- Sistema Operativo: Windows 10 o superior (para .exe)
- RAM: 512 MB mínimo
- Disco: 100 MB disponible
- Conexión: No requerida

### Requisitos de Desarrollo

- Python 3.8 o superior
- pip
- 500 MB espacio en disco
- Editor de código (VS Code, PyCharm, etc.)

## Documentación Adicional

Consulte los siguientes archivos para más información:

- `ferreteria_app/README.md` - Documentación completa
- `ferreteria_app/ARQUITECTURA.md` - Explicación técnica detallada
- `ferreteria_app/INICIO_RAPIDO.md` - Guía de inicio rápido
- `ferreteria_app/JSON_FORMAT_SPEC.md` - Especificación de formato de datos
- `ferreteria_app/DOCUMENTACION_INDEX.md` - Índice de documentación
- `ferreteria_app/INSTALL_INSTRUCTIONS.txt` - Instrucciones de instalación

## Soporte y Contacto

Para reportar problemas, sugerencias o consultas, contactar al equipo de desarrollo.

---

Versión: 1.0.0
Última actualización: Abril 2026
Licencia: JESUSD.U
Desarrollador: jesusdorian999019
