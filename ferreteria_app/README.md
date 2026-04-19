# Gestión de Ferretería

[Ver en GitHub](https://github.com/jesusdorian999019/TIENDA-DE-ABARROTES)

## Para Clientes (Sin Conocimientos Técnicos)

### Opción 1: Descargar y Ejecutar
1. Ir a: https://github.com/jesusdorian999019/TIENDA-DE-ABARROTES/releases
2. Descargar **FerreteriaPOS.exe**
3. Hacer doble clic para ejecutar
4. Usuario: `admin` / Contraseña: `admin123`

**Listo - No necesita instalar nada más.**

### Opción 2: Si no hay Releases
1. Ir a: https://github.com/jesusdorian999019/TIENDA-DE-ABARROTES
2. Hacer clic en botón verde **"Code"** → **"Download ZIP"**
3. Extraer ZIP
4. Abrir carpeta `ferreteria_app`
5. Hacer doble clic en `FerreteriaPOS.exe` (si existe)

## Para Desarrolladores

```bash
git clone https://github.com/jesusdorian999019/TIENDA-DE-ABARROTES.git
cd TIENDA-DE-ABARROTES/ferreteria_app
pip install -r requirements.txt
python main.py
```

## Funcionalidades
- Inventario completo (agregar/editar/eliminar)
- Ventas con stock automático
- Reportes y exportación Excel
- Búsqueda rápida
- Interfaz moderna y rápida

## Crear Ejecutable (.exe)
```bash
pip install pyinstaller
python build_exe.py
```
Archivo: `dist/FerreteriaPOS.exe`

Usuario inicial: admin / admin123

¡Listo para usar!
