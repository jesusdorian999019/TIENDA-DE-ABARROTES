# FerreteriaPOS - Sistema de Gestión para Ferretería

![Version](https://img.shields.io/badge/version-1.0.3-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Python](https://img.shields.io/badge/python-3.13-orange)
![Status](https://img.shields.io/badge/status-activo-success)

---

## Descripción

**FerreteriaPOS** es una aplicación de escritorio profesional diseñada para la administración integral de ferreterías. Gestiona inventarios, registra ventas, genera reportes y exporta datos de manera sencilla y eficiente.

Ya sea que tengas una pequeña ferretería o un negocio establecido, esta herramienta te ayudará a organizar y hacer crecer tu operación.

---

## Características Principales

| Módulo | Funcionalidades |
|--------|-----------------|
| **Inventario** | Registro completo de productos con código, categoría, precios y stock. Edición y eliminación simple. |
| **Ventas** | Registro rápido de ventas con sélection de producto y cantidad. Actualización automática del inventario. |
| **Reportes** | Dashboard en tiempo real, análisis de ventas por período, productos más vendidos, valorisation de inventario. |
| **Alertas** | Notificaciones automáticas cuando productos alcanzan el stock mínimo. |
| **Exportación** | Exportación de todos los datos a formato Excel para respaldo o análisis externo. |
| **Actualizaciones** | Sistema de actualización integrada directamente desde GitHub. |

---

## Requisitos del Sistema

| Requisito | Especificación |
|-----------|----------------|
| Sistema Operativo | Windows 10 o superior |
| Memoria RAM | Mínimo 4 GB |
| Espacio en Disco | 200 MB libres |
| Resolución de Pantalla | 1024x768 o superior |
| Dependencias | No requiere Python ni bases de datos |

---

## Instalación y Ejecución

### Paso 1: Descargar

Descarga el archivo `FerreteriaPOS.exe` directamente desde la raíz del repositorio.

### Paso 2: Ejecutar

```
1. Localiza el archivo FerreteriaPOS.exe
2. Haz doble clic sobre él
3. La aplicación se abrirá automáticamente
```

No requiere instalación. No requiere configuración de base de datos. No requiere conexión a internet (excepto para actualizaciones).

---

## Guía de Uso

### Inicio de Sesión

Al ejecutar la aplicación, ingresa con las credenciales por defecto:

| Campo | Valor |
|-------|-------|
| Usuario | admin |
| Contraseña | admin123 |

**Recomendación**: Cambia la contraseña desde la opción correspondiente después del primer inicio.

---

### Módulo de Inventario

Este módulo permite gestionar todos los productos de tu ferretería.

**Agregar Producto:**

1. Dirígete a la pestaña **Inventario**
2. Haz clic en el botón **Agregar Producto**
3. Completa los campos necesarios:

| Campo | Descripción | Requerido |
|-------|------------|-----------|
| Nombre | Nombre del producto | Obligatorio |
| Categoría | Clasificación (Herramientas, Pinturas, Fijaciones, etc.) | Obligatorio |
| Código | Identificador único o SKU | Opcional |
| Proveedor | Distribuidor o fournisseur | Opcional |
| Precio Compra | Costo de adquisición | Obligatorio |
| Precio Venta | Precio de venta al público | Obligatorio |
| Stock Inicial | Cantidad disponible actualmente | Obligatorio |
| Stock Mínimo | Umbral para alerta de stock bajo | Obligatorio |

4. Confirma con **Guardar**

**Editar Producto:**

1. Selecciona el producto de la lista
2. Haz clic en **Editar**
3. Modifica los campos requeridos
4. Confirma con **Guardar**

**Eliminar Producto:**

1. Selecciona el producto de la lista
2. Haz clic en **Eliminar**
3. Confirma la acción

---

### Módulo de Ventas

Registrar ventas nunca fue tan fácil.

**Pasos para registrar una venta:**

1. Ve a la pestaña **Ventas**
2. Selecciona el producto del listado o busca por nombre/código
3. Ingresa la cantidad vendida
4. Opcionalmente ingresa un descuento
5. Click en **Registrar Venta**

El sistema automáticamente:
- Descuenta la cantidad del inventario
- Registra la transacción con fecha y hora
- Actualiza los reportes en tiempo real

---

### Módulo de Reportes

El sistema ofrece múltiples vistas analíticas:

**Dashboard:**

- Ventas del día actual
- Ingresos del día
- Total de ventas acumuladas
- Ingresos totales
- Cantidad de productos en inventario
- Productos con stock bajo

**Reporte de Inventario:**

- Listado completo de todos los productos
- Valoración total del inventario
- Productos próximos a agotarse

**Reporte de Ventas:**

- Análisis por los últimos 7 días
- Análisis por los últimos 30 días
- Historial completo de ventas
- Gráficos visuales de desempeño

**Productos Más Vendidos:**

- Ranking de los 15 productos más vendidos
- Cantidad total vendida por producto
- Ingresos generados por producto

**Resetear Reportes:**

En la sección de reportes puedes resetear todas las ventas registradas. Esta función requiere autenticación con usuario y contraseña de administrador.

---

### Exportación de Datos

Para exportar todos tus datos a Excel:

1. Desde la ventana principal, haz clic en **Exportar a Excel**
2. Elige la ubicación donde guardar el archivo
3. El sistema generará un archivo con:
   - Hoja de productos
   - Hoja de ventas

---

### Buscar Actualizaciones

El programa incluye un sistema de actualizaciones automático:

1. Haz clic en **Buscar Actualizaciones**
2. El sistema verificará si hay una nueva versión disponible
3. Si existe actualización:
   - Te mostrará la versión nueva y la actual
   - Preguntará si deseas descargar
   - Al aceptar, abrirá el navegador en el repositorio GitHub
4. Si no hay actualización, te informará que ya tienes la última versión

Para actualizar manualmente:
1. Ve al repositorio GitHub
2. Descarga el nuevo archivo FerreteriaPOS.exe
3. Reemplaza el archivo existente

---

## Configuración de Datos

### Ubicación de Archivos

Los datos se almacenan automáticamente en la carpeta `data_storage` junto al ejecutable:

```
FerreteriaPOS.exe
data_storage/
  ├── users.json      (usuarios del sistema)
  ├── products.json  (inventario)
  └── sales.json    (registro de ventas)
```

### Respaldo Recomendado

Para realizar un respaldo:
1. Copia la carpeta `data_storage` completa
2. Guárdala en una ubicación segura

Para restaurar:
1. Cierra la aplicación
2. Reemplaza la carpeta `data_storage` con tu respaldo

---

## Solución de Problemas

### La aplicación no inicia

- Verifica que tienes Windows 10 o superior
- Asegúrate de tener el archivo completo (no corrupto)
- Intenta descargar nuevamente desde el repositorio

### No puedo iniciar sesión

- Usuario por defecto: `admin`
- Contraseña por defecto: `admin123`

### Los productos no aparecen

- Verifica que la carpeta `data_storage` existe
- Confirma que los archivos JSON no están vacíos

### Error al registrar venta

- Verifica que el producto tiene suficiente stock
- Revisa que los datos del producto sean correctos

### Las exportaciones no funcionan

- Verifica tener permisos de escritura en la ubicación elegida
- Intenta guardar en el escritorio o Mis Documentos

---

## Información Técnica

| Aspecto | Detalle |
|---------|---------|
| Tecnología | Python 3.13 + Tkinter |
| Compilador | PyInstaller |
| Almacenamiento | JSON (Sin base de datos) |
| Tipo | Aplicación de escritorio standalone |
| Actualización | Via GitHub (sistema integrado) |

---

## Cómo Contribuir

¿Encontraste un error? ¿Tienes una suggestion? ¡Contribuye al proyecto!

1. Haz fork del repositorio
2. Crea una rama con tu feature (`git checkout -b nueva-funcionalidad`)
3. Commitea tus cambios (`git commit -m 'Agregada nueva funcionalidad'`)
4. Push a la rama (`git push origin nueva-funcionalidad`)
5. Abre un Pull Request

---

## Licencia

Este proyecto está bajo la Licencia MIT.

Copyright © 2026 jesusdorian999019

---

## Contacto y Soporte

**Desarrollado por**: jesusdorian999019

**Plataforma**: GitHub
**Repositorio**: https://github.com/jesusdorian999019/TIENDA-DE-ABARROTES

Para reporte de errores o consultas, Abre un issue en el repositorio.

---

*Última actualización: Abril 2026 | Versión: 1.0.3*