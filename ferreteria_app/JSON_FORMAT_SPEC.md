# ESPECIFICACION DE FORMATOS JSON

Este documento explica la estructura exacta de los archivos JSON que utiliza la aplicación.

## 1. users.json

Almacena información de usuarios registrados.

### Estructura Completa

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "password_hash": "$2b$12$XXXXXXXXXXXXXXXXXXXXXu3TK6cPvXXXXXXXXXXXXXXXXXXXXXX",
    "created_at": "2026-04-18T10:30:45.123456"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "username": "vendedor1",
    "password_hash": "$2b$12$YYYYYYYYYYYYYYYYYYYYYY3TK6cPvYYYYYYYYYYYYYYYYYYYYYY",
    "created_at": "2026-04-18T11:00:00.000000"
  }
]
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | string (UUID) | Identificador único del usuario |
| username | string | Nombre de usuario (único) |
| password_hash | string | Contraseña hasheada con bcrypt |
| created_at | string (ISO 8601) | Fecha de creación |

### Reglas

- ID debe ser UUID único
- Username debe ser único y no puede repetirse
- Password_hash es JAMAS la contraseña en texto plano
- Createdm_at es automático (UTC)

---

## 2. products.json

Almacena el inventario de productos.

### Estructura Completa

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Martillo 16 oz",
    "category": "Herramientas",
    "code": "MAR001",
    "provider": "Ferretería Central",
    "purchase_price": 8.50,
    "sale_price": 12.99,
    "stock": 45,
    "min_stock": 10,
    "created_at": "2026-04-18T10:30:45.123456",
    "updated_at": "2026-04-18T14:30:00.000000"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Cable Eléctrico 10m",
    "category": "Electricidad",
    "code": "CAB001",
    "provider": "Cables S.A.",
    "purchase_price": 8.00,
    "sale_price": 12.50,
    "stock": 195,
    "min_stock": 50,
    "created_at": "2026-04-18T10:35:00.000000",
    "updated_at": "2026-04-18T14:35:00.000000"
  }
]
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | string (UUID) | Identificador único del producto |
| name | string | Nombre del producto |
| category | string | Categoría (Herramientas, Electricidad, etc.) |
| code | string | Código interno (único) |
| provider | string | Nombre del proveedor |
| purchase_price | number | Precio de compra (costo) |
| sale_price | number | Precio de venta |
| stock | integer | Cantidad actual disponible |
| min_stock | integer | Cantidad mínima (alerta si cae debajo) |
| created_at | string (ISO 8601) | Fecha de creación |
| updated_at | string (ISO 8601) | Última actualización |

### Reglas

- ID debe ser UUID único
- Code debe ser único (no puede repetirse)
- Precios son decimales (2 decimales)
- Stock es entero positivo
- min_stock se usa para alertas
- updated_at se actualiza cada vez que se modifica

### Ejemplo de Alerta

```
Si stock (45) < min_stock (10): ⚠️ ALERTA
Si stock (195) < min_stock (50): OK ✓
```

---

## 3. sales.json

Registro de todas las ventas realizadas.

### Estructura Completa

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "product_id": "550e8400-e29b-41d4-a716-446655440100",
    "product_name": "Martillo 16 oz",
    "quantity": 2,
    "unit_price": 12.99,
    "total": 25.98,
    "date": "2026-04-18",
    "time": "14:30:45",
    "created_at": "2026-04-18T14:30:45.123456"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "product_id": "550e8400-e29b-41d4-a716-446655440101",
    "product_name": "Cable Eléctrico 10m",
    "quantity": 5,
    "unit_price": 12.50,
    "total": 62.50,
    "date": "2026-04-18",
    "time": "15:45:30",
    "created_at": "2026-04-18T15:45:30.000000"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "product_id": "550e8400-e29b-41d4-a716-446655440100",
    "product_name": "Martillo 16 oz",
    "quantity": 1,
    "unit_price": 12.99,
    "total": 12.99,
    "date": "2026-04-17",
    "time": "10:15:00",
    "created_at": "2026-04-17T10:15:00.000000"
  }
]
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | string (UUID) | Identificador único de la venta |
| product_id | string (UUID) | ID del producto vendido |
| product_name | string | Nombre del producto (para histórico) |
| quantity | integer | Cantidad vendida |
| unit_price | number | Precio unitario en el momento de la venta |
| total | number | Total de la transacción (quantity × unit_price) |
| date | string (YYYY-MM-DD) | Fecha de la venta |
| time | string (HH:MM:SS) | Hora de la venta |
| created_at | string (ISO 8601) | Timestamp completo |

### Reglas

- ID debe ser UUID único
- product_id es referencia al producto (para auditoría)
- product_name se guarda para histórico (en caso que producto se elimine)
- unit_price es el precio en el MOMENTO de la venta (puede cambiar después)
- total = quantity × unit_price (calculado y guardado)
- date es YYYY-MM-DD (para búsqueda rápida)
- time es HH:MM:SS (hora local)
- NO se pueden editar ventas (solo crear o eliminar)

### Cálculos

```
Total = quantity × unit_price
Ejemplo: 2 × 12.99 = 25.98
```

---

## INTEGRIDAD DE DATOS

### Relaciones

```
users.json (usuarios)
    ↓
products.json (productos)
    ↓ (referencia: product_id)
sales.json (ventas)
```

### Validaciones Automáticas

1. **Código de Producto Único**
   - No puede haber dos productos con el mismo código

2. **Usuario Único**
   - No puede haber dos usuarios con el mismo nombre

3. **Stock Consistente**
   - Cuando se registra una venta, el stock del producto disminuye
   - Al eliminar una venta, el stock se incrementa (si se implementa)

4. **Fechas**
   - Siempre en formato ISO 8601 (UTC)
   - Automáticas al crear/modificar

---

## EJEMPLOS DE CONSULTAS

### Contar Productos

```json
// Antes de venta
products.json: 50 items en stock

// Después de venta (cantidad: 2)
products.json: 48 items en stock

// Venta registrada
sales.json: nuevo registro con quantity: 2
```

### Buscar Ventas de un Día

```json
// Filtrar por date: "2026-04-18"
sales.json: todos los registros con esa fecha

// Resultado
3 ventas encontradas en 2026-04-18
Total: 100.47
```

### Top 5 Productos Vendidos

```
Agrupar sales.json por product_id
Contar cantidad total vendida
Ordenar descendente
Mostrar top 5
```

---

## MIGRACION A SQL

### Equivalencia de Tablas

#### users.json → tabla users

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
```

#### products.json → tabla products

```sql
CREATE TABLE products (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    provider VARCHAR(100) NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    sale_price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    min_stock INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

#### sales.json → tabla sales

```sql
CREATE TABLE sales (
    id VARCHAR(36) PRIMARY KEY,
    product_id VARCHAR(36) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

---

## BACKUP Y RESTAURACION

### Archivo de Backup Ejemplo

```
Fecha: 2026-04-18_14-30-45
Contenido:
- data_storage_backup_2026-04-18_14-30-45/
  ├── users.json (1 KB)
  ├── products.json (50 KB)
  └── sales.json (200 KB)
Total: 251 KB
```

### Restaurar

1. Cerrar aplicación
2. Reemplazar data_storage/ con data_storage_backup/
3. Reiniciar aplicación

---

## TAMAÑO ESPERADO DE ARCHIVOS

| Archivo | Registros | Tamaño Aprox |
|---------|-----------|-------------|
| users.json | 10-100 | 5-50 KB |
| products.json | 100-1000 | 50-500 KB |
| sales.json | 1000-10000 | 100-1000 KB |
| **Total** | - | **200-1500 KB** |

### Con 30 Días de Datos

```
Supuestos:
- 500 productos
- 100 ventas/día
- 3000 ventas totales

Tamaño total: ~500 KB (muy manejable)
```

---

## NOTAS IMPORTANTES

1. **Los archivos se crean automáticamente** la primera vez que ejecuta la aplicación

2. **No edite manualmente a menos que sepa lo que hace** - Puede corromper los datos

3. **Para backup, simplemente copie la carpeta data_storage/**

4. **Los archivos son texto plano** - Puede abrirlos con cualquier editor de texto

5. **UUIDs garantizan unicidad** - Incluso si se ejecuta en múltiples máquinas

6. **Las fechas están en UTC** - Independiente de la zona horaria

7. **Para producción, considere migrar a SQLite** - Mejor rendimiento con muchos datos

---

## VALIDACION DE INTEGRIDAD

### Script de Validación (Python)

```python
import json

def validar_json():
    # Validar users.json
    with open('data_storage/users.json') as f:
        users = json.load(f)
        assert all('id' in u and 'username' in u for u in users)
    
    # Validar products.json
    with open('data_storage/products.json') as f:
        products = json.load(f)
        assert all('id' in p and 'code' in p for p in products)
    
    # Validar sales.json
    with open('data_storage/sales.json') as f:
        sales = json.load(f)
        assert all('id' in s and 'product_id' in s for s in sales)
    
    print("✓ Todos los archivos JSON son válidos")

validar_json()
```

---

**Última actualización:** 18 de Abril de 2026

Versión: 1.0.0
