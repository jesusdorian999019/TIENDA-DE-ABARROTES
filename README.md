# Sistema de Gestión para Ferretería

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

Una aplicación de escritorio moderna para administrar tu ferretería de manera fácil, rápida y eficiente.

---

## Características Principales

| Función | Descripción |
|---------|------------|
| **Gestión de Inventario** | Agrega, edita y elimina productos con código y categorización |
| **Registro de Ventas** | Registra ventas de forma instantánea con actualización automática de stock |
| **Reportes Inteligentes** | Visualiza ventas diarias, semanales y análisis de productos más vendidos |
| **Alertas de Stock** | Notificaciones automáticas cuando el inventario alcanza el mínimo |
| **Exportación a Excel** | Descarga tus datos en formatos listos para imprimir o compartir |

---

## Requisitos del Sistema

- Windows 10 o superior
- Sin necesidad de instalación de base de datos
- Sin requerimientos de conexión a internet

---

## Guía de Uso Rápido

### 1. Iniciar la Aplicación
Ejecuta `FerreteriaPOS.exe` con doble clic. La aplicación se abrirá automáticamente.

### 2. Primera Conexión
**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

### 3. Agregar Productos al Inventario

Ve a **Inventario** > **Agregar Producto**

Complete los siguientes campos:

| Campo | Descripción | Obligatorio |
|-------|-------------|-----------|
| Nombre | Denominación del producto | Sí |
| Categoría | Herramientas, Pinturas, Fijaciones, etc. | Sí |
| Código | Identificador único (ej: SKU) | No |
| Proveedor | Nombre del distribuidor | No |
| Precio Compra | Costo de adquisición | Sí |
| Precio Venta | Precio al público | Sí |
| Cantidad en Stock | Unidades disponibles | Sí |
| Stock Mínimo | Umbral para alertas | Sí |

Presione "Guardar" para confirmar.

### 4. Registrar Ventas

Ve a **Ventas** > Selecciona el producto > Ingresa la cantidad > **Registrar Venta**

El sistema descuenta automáticamente del inventario.

### 5. Consultar Reportes

Acceda a la sección **Reportes** para visualizar:

- **Dashboard**: Resumen ejecutivo con ventas del día actual
- **Inventario**: Listado completo de productos y valuaciones
- **Ventas**: Gráficos de desempeño por período
- **Productos**: Ranking de artículos más vendidos

### 6. Exportar Datos

Ve a **Pantalla Principal** > **Exportar a Excel**

Seleccione la ubicación de destino. El archivo se generará automáticamente con todos sus datos.

### 7. Resetear Reportes

Ve a **Reportes** > **Resetear Reportes** > Ingresa credenciales > Confirmar

Esta acción elimina todos los registros de ventas. Requiere autenticación.

---

## Información Importante

- **Guardado automático**: Los datos se guardan en tiempo real sin intervención del usuario
- **Ubicación de datos**: Todos los registros se almacenan en la carpeta `data_storage`
- **Respaldo recomendado**: Realice copias de seguridad periódicamente

---

## Solución de Problemas

### La aplicación no se abre
- Verifique que dispone de Windows 10 o superior
- Descargue nuevamente la aplicación desde la fuente oficial

### Error al iniciar sesión
- Usuario por defecto: `admin`
- Contraseña por defecto: `admin123`

### Los datos no se muestran
- Haga clic en el botón "Actualizar" en la parte superior de la ventana
- Verifique que la carpeta `data_storage` existe y contiene archivos

---

## Especificaciones Técnicas

- **Plataforma**: Aplicación de escritorio Windows
- **Almacenamiento**: JSON embebido (sin instalación requerida)
- **Requisitos de red**: Ninguno

---

## Autor

Desarrollado por: **jesusdorian999019**
Contacto: JESUS.U

---

**Última actualización**: Abril 2026