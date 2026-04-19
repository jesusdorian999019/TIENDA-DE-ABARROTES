# Almacenamiento de Datos

Esta carpeta contiene los archivos JSON con los datos de la aplicación.

## Archivos

- **users.json**: Usuarios registrados (id, username, password_hash)
- **products.json**: Inventario de productos
- **sales.json**: Historial de ventas

## Estructura de Datos

### users.json
```json
[
  {
    "id": "uuid-aqui",
    "username": "admin",
    "password_hash": "hash-bcrypt-aqui",
    "created_at": "2026-04-18T10:30:00.123456"
  }
]
```

### products.json
```json
[
  {
    "id": "uuid-aqui",
    "name": "Martillo 16 oz",
    "category": "Herramientas",
    "code": "MAR001",
    "provider": "Proveedor A",
    "purchase_price": 8.50,
    "sale_price": 12.99,
    "stock": 50,
    "min_stock": 10,
    "created_at": "2026-04-18T10:30:00.123456",
    "updated_at": "2026-04-18T10:30:00.123456"
  }
]
```

### sales.json
```json
[
  {
    "id": "uuid-aqui",
    "product_id": "uuid-producto",
    "product_name": "Martillo 16 oz",
    "quantity": 2,
    "unit_price": 12.99,
    "total": 25.98,
    "date": "2026-04-18",
    "time": "14:30:45",
    "created_at": "2026-04-18T14:30:45.123456"
  }
]
```

## Notas

- **Estos archivos se generan automáticamente** al iniciar la aplicación
- No edite estos archivos manualmente a menos que sepa lo que hace
- Para backup, simplemente copie estos archivos a otra ubicación
- Para restore, reemplace estos archivos por los del backup

## Backup y Restore

### Backup
```bash
# Copiar carpeta data_storage a ubicación segura
cp -r data_storage data_storage.backup
```

### Restore
```bash
# Restaurar desde backup
rm -rf data_storage
cp -r data_storage.backup data_storage
```

## Limpieza de Datos

Para limpiar todos los datos (no recomendado):

1. Cierre la aplicación
2. Elimine los archivos JSON en esta carpeta
3. Reinicie la aplicación

Esto recreará los archivos con datos vacíos (excepto el usuario admin).

---

**Última actualización:** 18 de Abril de 2026
