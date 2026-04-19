# Arquitectura de la Aplicación

## Introducción

La aplicación "Gestión de Ferretería" sigue una arquitectura en capas que separa claramente las responsabilidades del código. Esta arquitectura permite:

✅ **Mantenibilidad:** El código es fácil de entender y modificar  
✅ **Escalabilidad:** Nuevas funciones se pueden añadir sin afectar código existente  
✅ **Testabilidad:** Cada componente puede testearse de forma aislada  
✅ **Flexibilidad:** La lógica de negocio es independiente de la interfaz  
✅ **Portabilidad:** Fácil migración a otras tecnologías (web, móvil, etc.)

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────┐
│           CAPA DE INTERFAZ (UI)             │
│  ┌────────────────────────────────────────┐ │
│  │  main_window.py                        │ │
│  │  ├─ inventory_tab.py                   │ │
│  │  ├─ sales_tab.py                       │ │
│  │  └─ reports_tab.py                     │ │
│  │  login_window.py                       │ │
│  └────────────────────────────────────────┘ │
└────────┬────────────────────────────────────┘
         │ Utiliza
┌────────▼────────────────────────────────────┐
│     CAPA DE LÓGICA DE NEGOCIO (Business)    │
│  ┌────────────────────────────────────────┐ │
│  │  user_service.py                       │ │
│  │  inventory_service.py                  │ │
│  │  sales_service.py                      │ │
│  │  reports_service.py                    │ │
│  └────────────────────────────────────────┘ │
└────────┬────────────────────────────────────┘
         │ Utiliza
┌────────▼────────────────────────────────────┐
│      CAPA DE ACCESO A DATOS (Data)          │
│  ┌────────────────────────────────────────┐ │
│  │  data_manager.py (Interfaz abstracta)  │ │
│  │          ↑                             │ │
│  │          │ Implementada por:           │ │
│  │          ├─ json_manager.py (Actual)   │ │
│  │          └─ sqlite_manager.py (Futuro) │ │
│  │                                        │ │
│  │  models.py (User, Product, Sale)      │ │
│  └────────────────────────────────────────┘ │
└────────┬────────────────────────────────────┘
         │ Lee/Escribe
┌────────▼────────────────────────────────────┐
│     ALMACENAMIENTO DE DATOS                 │
│  ┌────────────────────────────────────────┐ │
│  │  data_storage/                         │ │
│  │  ├─ users.json                         │ │
│  │  ├─ products.json                      │ │
│  │  └─ sales.json                         │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│        CAPAS DE SOPORTE (Utils)             │
│  ├─ security.py (Hash, verificación)        │
│  ├─ validators.py (Validación de datos)     │
│  ├─ excel_exporter.py (Exportación)         │
│  └─ config/settings.py (Configuración)      │
└─────────────────────────────────────────────┘
```

## Descripción Detallada de Capas

### 1. Capa de Interfaz (UI)

**Ubicación:** `ui/`  
**Responsabilidad:** Presentar datos al usuario y capturar entradas

**Componentes:**

- **`login_window.py`**
  - Ventana de autenticación
  - Validación de credenciales
  - Opción de registro de nuevos usuarios
  - Interfaz simple y clara

- **`main_window.py`**
  - Ventana principal
  - Gestiona la navegación entre tabs
  - Controla alertas y actualizaciones
  - Botones de acción global (Exportar, Actualizar, Salir)

- **`inventory_tab.py`**
  - Gestión completa de productos
  - CRUD: Crear, Leer, Actualizar, Eliminar
  - Búsqueda y filtrado
  - Tabla con visualización de datos

- **`sales_tab.py`**
  - Registro de ventas rápido
  - Selección de productos disponibles
  - Cálculo automático de totales
  - Historial de ventas con filtrado

- **`reports_tab.py`**
  - Dashboard con KPIs
  - Múltiples tipos de reportes
  - Visualización de datos en tablas
  - Gráficos simples

**Características:**
- Todas las ventanas usan Tkinter
- Estilos consistentes en toda la aplicación
- Manejo de errores con messagebox
- No contiene lógica de negocio

### 2. Capa de Lógica de Negocio

**Ubicación:** `business/`  
**Responsabilidad:** Implementar las reglas de negocio

**Componentes:**

- **`user_service.py`**
  - Gestión de usuarios
  - Autenticación y validación de credenciales
  - Hash seguro de contraseñas
  - Creación de usuarios

- **`inventory_service.py`**
  - CRUD de productos
  - Búsqueda y filtrado
  - Validación de datos de productos
  - Cálculo de valores de inventario
  - Alertas de stock bajo

- **`sales_service.py`**
  - Registro de ventas
  - Cálculo de totales
  - Gestión de stock durante ventas
  - Reportes de ventas por fecha
  - Resumen diario/mensual

- **`reports_service.py`**
  - Generación de reportes
  - Análisis de datos
  - Cálculos de KPIs
  - Datos para dashboard
  - Productos más vendidos

**Características:**
- No conocen sobre UI (pueden reutilizarse en web, CLI, etc.)
- Utilizan el DataManager abstracto (no dependen de JSON)
- Incluyen validaciones
- Retornan tuplas (éxito, mensaje) para manejo de errores

### 3. Capa de Acceso a Datos

**Ubicación:** `data/`  
**Responsabilidad:** Abstraer el almacenamiento de datos

#### 3.1 Interfaz Abstracta (data_manager.py)

```python
class DataManager(ABC):
    # Métodos abstractos para CRUD
    # - Usuarios
    # - Productos
    # - Ventas
    # - Reportes
```

**Ventajas de usar una interfaz abstracta:**
- El resto del código no depende de la implementación específica
- Fácil cambiar de JSON a SQLite sin modificar otra cosa
- Permite testear con Mock objects
- Abre la puerta a múltiples implementaciones simultáneamente

#### 3.2 Modelos (models.py)

Define las estructuras de datos usando dataclasses:

```python
@dataclass
class User:
    id: str
    username: str
    password_hash: str
    created_at: str

@dataclass
class Product:
    id: str
    name: str
    category: str
    code: str
    # ... más campos

@dataclass
class Sale:
    id: str
    product_id: str
    quantity: int
    # ... más campos
```

#### 3.3 Implementación JSON (json_manager.py)

- Implementa todos los métodos de DataManager
- Lee/escribe archivos JSON
- Genera UUIDs para IDs
- Manejo de excepciones

```python
class JsonManager(DataManager):
    def create_product(self, product: Product) -> bool:
        # Leer JSON, añadir producto, guardar
        pass
    
    def get_product(self, product_id: str) -> Optional[Product]:
        # Leer JSON, buscar, retornar
        pass
```

### 4. Modelos de Datos

**Ubicación:** `data/models.py`

Define usando dataclasses para:
- Seguridad de tipos
- Serialización fácil a/desde JSON
- Métodos `to_dict()` y `from_dict()`

### 5. Capas de Soporte

#### 5.1 Seguridad (utils/security.py)

```python
class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        # Hashea con bcrypt (o fallback a sha256)
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        # Verifica contraseña contra hash
```

#### 5.2 Validación (utils/validators.py)

```python
class Validators:
    @staticmethod
    def validate_product_name(name: str) -> Tuple[bool, str]:
        # Retorna (válido, mensaje)
    
    @staticmethod
    def validate_price(price: str) -> Tuple[bool, str]:
        # Validación numérica
```

#### 5.3 Exportación (utils/excel_exporter.py)

```python
class ExcelExporter:
    def add_inventory_sheet(self, products):
        # Crea hoja con productos
    
    def export(self, products, sales) -> str:
        # Genera archivo .xlsx completo
```

#### 5.4 Configuración (config/settings.py)

- Rutas de archivos
- Colores y estilos
- Categorías predeterminadas
- Configuración global

## Flujo de Datos

### Inicio de Sesión

```
Usuario ingresa credenciales
        ↓
login_window.py captura entrada
        ↓
user_service.authenticate()
        ↓
data_manager.get_user_by_username()
        ↓
JsonManager lee users.json
        ↓
security.verify_password()
        ↓
Retorna (éxito, mensaje)
        ↓
Si éxito: Abrir main_window
Si error: Mostrar mensaje
```

### Crear Producto

```
Usuario hace clic "Nuevo Producto"
        ↓
Abre diálogo con formulario
        ↓
Usuario ingresa datos y haga clic "Guardar"
        ↓
inventory_tab.py captura datos
        ↓
inventory_service.create_product()
        ↓
Validadores verifican cada campo
        ↓
data_manager.create_product(product)
        ↓
JsonManager genera UUID y escribe JSON
        ↓
Retorna éxito
        ↓
inventory_tab.refresh() actualiza tabla
```

### Registrar Venta

```
Usuario selecciona producto y cantidad
        ↓
Precio se calcula automáticamente
        ↓
Usuario haga clic "Confirmar Venta"
        ↓
sales_tab.py captura datos
        ↓
sales_service.register_sale()
        ↓
Crea objeto Sale con datos
        ↓
data_manager.create_sale()
        ↓
JsonManager escribe en sales.json
        ↓
sales_service actualiza stock
        ↓
inventory_service.update_stock()
        ↓
data_manager.update_product_stock()
        ↓
JsonManager actualiza products.json
        ↓
Retorna éxito
        ↓
Mostrar confirmación
```

## Ventajas de Esta Arquitectura

### Para Desarrollo

1. **Separación de Responsabilidades**
   - Cada módulo tiene un propósito claro
   - Fácil localizar dónde hacer cambios

2. **Reutilización de Código**
   - Services pueden usarse en múltiples UIs
   - No hay duplicación de lógica

3. **Testabilidad**
   - Cada capa puede probarse independientemente
   - Fácil crear mocks

### Para Mantenimiento

1. **Cambios en UI sin afectar lógica**
   - Migrar de Tkinter a Qt sin cambiar business/data
   
2. **Optimizaciones de BD sin UI changes**
   - Cambiar JsonManager por SqliteManager
   - Sin modificar inventory_service.py

3. **Corrección de bugs localizados**
   - Si hay bug en búsqueda, está en inventory_service.py
   - No en 10 lugares diferentes

### Para Escalabilidad

1. **Añadir nuevas funcionalidades**
   - Nuevo tab en UI
   - Nuevo service en business
   - Nuevos métodos en data

2. **Migración a Web**
   - Reutilizar business/ y data/
   - Crear nueva capa UI con Flask/Django

3. **Exportación a Móvil**
   - Mismo business/ y data/
   - UI con Flutter/React Native

## Migración Futura: JSON → SQLite

### Paso 1: Crear SqliteManager

```python
# data/sqlite_manager.py
class SqliteManager(DataManager):
    def __init__(self, db_path='ferreteria.db'):
        self.db_path = db_path
        self._init_database()
    
    def create_product(self, product: Product) -> bool:
        # Implementar con SQL en lugar de JSON
        pass
```

### Paso 2: Cambiar en main.py

```python
# Antes
from data.json_manager import JsonManager
inventory_service = InventoryService(JsonManager())

# Después
from data.sqlite_manager import SqliteManager
inventory_service = InventoryService(SqliteManager())
```

### Paso 3: Cero cambios en

- `ui/` ← Sigue funcionando igual
- `business/` ← Sigue funcionando igual
- Tests ← Siguen funcionando igual

## Conclusión

Esta arquitectura en capas proporciona:
- ✅ Flexibilidad para cambios futuros
- ✅ Claridad en la estructura del código
- ✅ Facilidad de mantenimiento
- ✅ Escalabilidad sin sacrificar rendimiento
- ✅ Profesionalismo en el desarrollo

El sistema está listo para crecer desde un prototipo JSON a una aplicación SQL enterprise sin rehacer el proyecto.

---

**Versión:** 1.0.0  
**Última actualización:** 18 de Abril de 2026
